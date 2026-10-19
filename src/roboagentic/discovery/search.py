"""Live robotics supplier discovery for ROBOAGENTIC / ROBOPARTS.ai.

Searches the Brave Search API, records source provenance, generates
preliminary identity assessments, and optionally stores candidates
in the existing ROBOAGENTIC database.

Search results are unverified candidates. This module does not
independently verify legal identity, website ownership, or capability.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import httpx
from dotenv import load_dotenv

from roboagentic.discovery.identity import (
    assess_identity,
    assessment_to_dict,
    normalize_domain,
)

load_dotenv()

logger = logging.getLogger("roboagentic.discovery")

API_URL = "https://api.search.brave.com/res/v1/web/search"

COMPONENT_QUERIES: dict[str, list[str]] = {
    "actuators": [
        '"robotics actuator manufacturer"',
        '"humanoid robot joint actuator manufacturer"',
        '"robot servo motor manufacturer"',
    ],
    "mechanical": [
        '"robotics CNC machining manufacturer"',
        '"robot structural frame manufacturer"',
        '"harmonic drive manufacturer robotics"',
    ],
    "hands": [
        '"robotic hand manufacturer"',
        '"robot gripper manufacturer"',
        '"humanoid robot hand supplier"',
    ],
    "wiring": [
        '"robotics wiring harness manufacturer"',
        '"robotics electrical connector manufacturer"',
    ],
    "sensors": [
        '"robotics force torque sensor manufacturer"',
        '"robotics lidar manufacturer"',
        '"robotics tactile sensor manufacturer"',
    ],
    "electronics": [
        '"robot motor controller manufacturer"',
        '"robotics embedded controller manufacturer"',
        '"robotics PCB assembly manufacturer"',
    ],
}


@dataclass
class SearchResult:
    """A candidate returned by a web search provider."""

    title: str
    url: str
    description: str
    query: str
    category: str
    source_provider: str = "Brave Search API"
    review_status: str = "needs_source_review"


def build_queries(
    categories: list[str] | None = None,
) -> list[tuple[str, str]]:
    """Return configured queries for the requested categories."""
    selected = categories or list(COMPONENT_QUERIES)
    queries: list[tuple[str, str]] = []

    for category in selected:
        if category not in COMPONENT_QUERIES:
            logger.warning(
                "Ignoring unknown component category: %s",
                category,
            )
            continue

        for query in COMPONENT_QUERIES[category]:
            queries.append((category, query))

    return queries


def is_valid_web_url(value: str) -> bool:
    """Check basic HTTP(S) URL syntax without claiming verification."""
    if not isinstance(value, str) or not value.strip():
        return False

    try:
        parsed = urlsplit(value.strip())

        return (
            parsed.scheme.lower() in {"http", "https"}
            and bool(parsed.hostname)
            and not parsed.username
            and not parsed.password
            and bool(normalize_domain(value))
        )
    except (ValueError, AttributeError):
        return False


async def search_web(
    client: httpx.AsyncClient,
    query: str,
    country: str = "US",
    language: str = "en",
    count: int = 10,
) -> list[dict[str, Any]]:
    """Query the Brave Search API and return web result records."""
    api_key = os.getenv("BRAVE_SEARCH_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "BRAVE_SEARCH_API_KEY is missing. "
            "Configure it in your environment before live discovery."
        )

    response = await client.get(
        API_URL,
        headers={
            "Accept": "application/json",
            "X-Subscription-Token": api_key,
        },
        params={
            "q": query,
            "country": country.upper(),
            "search_lang": language.lower(),
            "count": min(max(count, 1), 20),
        },
    )

    response.raise_for_status()
    payload = response.json()

    if not isinstance(payload, dict):
        logger.warning("Search provider returned an unexpected response.")
        return []

    web_data = payload.get("web", {})
    if not isinstance(web_data, dict):
        return []

    items = web_data.get("results", [])
    if not isinstance(items, list):
        return []

    return [
        item for item in items
        if isinstance(item, dict)
    ]


async def discover(
    categories: list[str] | None = None,
    country: str = "US",
    language: str = "en",
    results_per_query: int = 10,
    concurrency: int = 2,
) -> list[SearchResult]:
    """Discover candidate suppliers using bounded asynchronous searches."""
    if not 1 <= results_per_query <= 20:
        raise ValueError(
            "results_per_query must be between 1 and 20."
        )

    if not 1 <= concurrency <= 5:
        raise ValueError("concurrency must be between 1 and 5.")

    queries = build_queries(categories)

    if not queries:
        logger.warning("No valid discovery queries were selected.")
        return []

    semaphore = asyncio.Semaphore(concurrency)
    timeout = httpx.Timeout(20.0, connect=10.0)
    results: list[SearchResult] = []

    async with httpx.AsyncClient(timeout=timeout) as client:

        async def run_query(
            category: str,
            query: str,
        ) -> list[SearchResult]:
            async with semaphore:
                try:
                    items = await search_web(
                        client=client,
                        query=query,
                        country=country,
                        language=language,
                        count=results_per_query,
                    )
                except httpx.HTTPStatusError as exc:
                    logger.warning(
                        "Search provider returned HTTP %s for query %r.",
                        exc.response.status_code,
                        query,
                    )
                    return []
                except httpx.HTTPError as exc:
                    logger.warning(
                        "Search request failed for query %r: %s",
                        query,
                        type(exc).__name__,
                    )
                    return []
                except ValueError:
                    logger.warning(
                        "Search provider returned invalid JSON for %r.",
                        query,
                    )
                    return []

                parsed: list[SearchResult] = []

                for item in items:
                    url = item.get("url", "")
                    title = item.get("title", "")
                    description = item.get("description", "")

                    if not isinstance(url, str):
                        continue

                    if not isinstance(title, str):
                        continue

                    if not isinstance(description, str):
                        description = ""

                    url = url.strip()
                    title = title.strip()
                    description = description.strip()

                    if not is_valid_web_url(url):
                        continue

                    if not title:
                        continue

                    parsed.append(
                        SearchResult(
                            title=title,
                            url=url,
                            description=description,
                            query=query,
                            category=category,
                        )
                    )

                return parsed

        batches = await asyncio.gather(
            *[
                run_query(category, query)
                for category, query in queries
            ]
        )

    for batch in batches:
        results.extend(batch)

    # Deduplicate by normalized URL while retaining the first result.
    unique: dict[str, SearchResult] = {}

    for result in results:
        parsed = urlsplit(result.url)
        hostname = normalize_domain(result.url)

        if not hostname:
            continue

        normalized_url = (
            f"{parsed.scheme.lower()}://{hostname}"
            f"{parsed.path.rstrip('/')}"
        )

        if parsed.query:
            normalized_url += f"?{parsed.query}"

        key = normalized_url.casefold()

        if key not in unique:
            unique[key] = result

    return list(unique.values())


def export_json(
    results: list[SearchResult],
    output_path: str = "reports/discovery_results.json",
) -> Path:
    """Export candidate records and source provenance to JSON."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            [asdict(item) for item in results],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path


def build_identity_assessments(
    results: list[SearchResult],
) -> list[dict[str, Any]]:
    """Build preliminary identity assessments for discovered candidates.

    IMPORTANT: A search result URL is evidence, not proof of an
    official company website. The result title is also only a
    provisional company-name candidate.
    """
    assessments: list[dict[str, Any]] = []

    for result in results:
        assessment = assess_identity(
            company_name=result.title,
            website=result.url,
            title=result.title,
            description=result.description,
            source_url=result.url,
        )

        record = assessment_to_dict(assessment)

        # Preserve discovery provenance alongside the assessment.
        record["source_url"] = result.url
        record["search_query"] = result.query
        record["component_category"] = result.category
        record["source_provider"] = result.source_provider
        record["review_status"] = result.review_status

        assessments.append(record)

    return assessments


def export_identity_assessments(
    results: list[SearchResult],
    output_path: str = "reports/identity_assessments.json",
) -> Path:
    """Write preliminary identity assessments to a separate JSON file."""
    assessments = build_identity_assessments(results)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            assessments,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return path


def save_to_roboagentic_database(
    results: list[SearchResult],
) -> int:
    """Store unverified candidates using the existing application API."""
    from roboagentic.main import add_company

    saved = 0

    for item in results:
        try:
            add_company(
                name=item.title,
                website=item.url,
                country="Unknown",
                company_type="Unverified search candidate",
                description=item.description,
                capabilities=[item.category],
                source_url=item.url,
                source_verified=False,
            )
            saved += 1

        except (ValueError, RuntimeError) as exc:
            logger.warning(
                "Candidate could not be stored (%s).",
                type(exc).__name__,
            )

    return saved


async def async_main(args: argparse.Namespace) -> None:
    """Execute discovery, export results, and optionally save candidates."""
    results = await discover(
        categories=args.categories,
        country=args.country,
        language=args.language,
        results_per_query=args.count,
        concurrency=args.concurrency,
    )

    output = export_json(results, args.output)

    identity_output = export_identity_assessments(
        results,
        args.identity_output,
    )

    print(f"Candidate search results: {len(results)}")
    print(f"Discovery export: {output}")
    print(f"Identity assessment export: {identity_output}")

    if args.save_to_database:
        saved = save_to_roboagentic_database(results)
        print(f"Database records processed: {saved}")

    print(
        "Candidates require independent source review. "
        "Identity assessments are preliminary; no supplier emails "
        "were sent."
    )


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(
        description="ROBOAGENTIC robotics supplier discovery"
    )

    parser.add_argument(
        "--categories",
        nargs="+",
        choices=sorted(COMPONENT_QUERIES),
        help="Categories to search. Defaults to all categories.",
    )
    parser.add_argument("--country", default="US")
    parser.add_argument("--language", default="en")
    parser.add_argument("--count", type=int, default=10)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument(
        "--output",
        default="reports/discovery_results.json",
        help="Path for discovery JSON output.",
    )
    parser.add_argument(
        "--identity-output",
        default="reports/identity_assessments.json",
        help="Path for identity assessment JSON output.",
    )
    parser.add_argument(
        "--save-to-database",
        action="store_true",
        help="Save candidates to the existing application database.",
    )

    args = parser.parse_args()

    if not 1 <= args.count <= 20:
        parser.error("--count must be between 1 and 20.")

    if not 1 <= args.concurrency <= 5:
        parser.error("--concurrency must be between 1 and 5.")

    try:
        asyncio.run(async_main(args))
    except RuntimeError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
