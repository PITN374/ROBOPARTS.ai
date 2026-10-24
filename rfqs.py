"""ROBOPARTS.ai RFQ submission endpoint for Vercel.

Route: POST /api/rfqs
Email delivery: Microsoft Graph
Recipient: powerinthenumbers@pitn.ai

Required environment variables:
  AZURE_TENANT_ID
  AZURE_CLIENT_ID
  AZURE_CLIENT_SECRET
  RFQ_FROM_EMAIL

Optional:
  RFQ_TO_EMAIL
  RFQ_ALLOWED_ORIGINS
"""

import html
import json
import logging
import os
import re
import time
from http.server import BaseHTTPRequestHandler
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("roboparts-rfq")

RECIPIENT = os.getenv(
    "RFQ_TO_EMAIL", "powerinthenumbers@pitn.ai"
).strip()

MAX_BODY_BYTES = 30_000
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def json_response(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


def allowed_origin(handler):
    origin = handler.headers.get("Origin", "")
    if not origin:
        return ""

    allowed = {
        item.strip().rstrip("/")
        for item in os.getenv("RFQ_ALLOWED_ORIGINS", "").split(",")
        if item.strip()
    }

    # Same-origin requests need no cross-origin permission.
    host = handler.headers.get("Host", "")
    if origin.rstrip("/").split("://")[-1].lower() == host.lower():
        return origin

    if origin.rstrip("/") in allowed:
        return origin

    return None


def graph_send_email(subject, body_html, reply_to=None):
    tenant = os.getenv("AZURE_TENANT_ID", "").strip()
    client_id = os.getenv("AZURE_CLIENT_ID", "").strip()
    client_secret = os.getenv("AZURE_CLIENT_SECRET", "")
    sender = os.getenv("RFQ_FROM_EMAIL", "").strip()

    if not all([tenant, client_id, client_secret, sender]):
        raise RuntimeError("Microsoft 365 email configuration is incomplete")

    token_url = (
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
    )
    token_data = urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
        "grant_type": "client_credentials",
    }).encode()

    token_request = Request(
        token_url,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(token_request, timeout=12) as response:
        token = json.loads(response.read())["access_token"]

    message = {
        "message": {
            "subject": subject,
            "body": {"contentType": "HTML", "content": body_html},
            "toRecipients": [
                {"emailAddress": {"address": RECIPIENT}}
            ],
        },
        "saveToSentItems": True,
    }

    if reply_to and EMAIL_RE.fullmatch(reply_to):
        message["message"]["replyTo"] = [
            {"emailAddress": {"address": reply_to}}
        ]

    send_url = (
        "https://graph.microsoft.com/v1.0/users/"
        + sender
        + "/sendMail"
    )

    send_request = Request(
        send_url,
        data=json.dumps(message).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urlopen(send_request, timeout=15) as response:
        if response.status not in (200, 202):
            raise RuntimeError("Microsoft Graph did not accept the email")


class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        origin = allowed_origin(self)
        if origin is None:
            json_response(self, 403, {"error": "Origin not allowed"})
            return

        self.send_response(204)
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        json_response(self, 405, {
            "error": "Use POST to submit an RFQ."
        })

    def do_POST(self):
        origin = allowed_origin(self)
        if origin is None:
            json_response(self, 403, {"error": "Origin not allowed"})
            return

        content_type = self.headers.get("Content-Type", "")
        if "application/json" not in content_type.lower():
            json_response(self, 415, {
                "error": "Content-Type must be application/json."
            })
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0

        if length < 2 or length > MAX_BODY_BYTES:
            json_response(self, 413, {
                "error": "Request body is missing or too large."
            })
            return

        try:
            data = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            json_response(self, 400, {
                "error": "Invalid JSON request."
            })
            return

        if not isinstance(data, dict):
            json_response(self, 400, {
                "error": "Request must be a JSON object."
            })
            return

        fields = {
            "company_name": "Company",
            "contact_name": "Contact name",
            "contact_email": "Contact email",
            "requirements": "Requirements",
        }

        cleaned = {}
        for key, label in fields.items():
            value = data.get(key, "")
            if not isinstance(value, str):
                json_response(self, 422, {
                    "error": f"{label} must be text."
                })
                return
            value = value.strip()
            if not value or len(value) > 5000:
                json_response(self, 422, {
                    "error": f"{label} is required and must be under 5000 characters."
                })
                return
            cleaned[key] = value

        if not EMAIL_RE.fullmatch(cleaned["contact_email"]):
            json_response(self, 422, {
                "error": "Enter a valid contact email."
            })
            return

        optional_fields = {
            "product_id": "Product ID",
            "part_number": "Part number",
            "quantity": "Quantity",
            "fleet_size": "Fleet size",
        }

        for key, label in optional_fields.items():
            value = data.get(key, "")
            if not isinstance(value, (str, int, float)) or isinstance(value, bool):
                json_response(self, 422, {
                    "error": f"{label} must be text or a number."
                })
                return
            cleaned[key] = str(value).strip()[:500]

        # Escape all user input before inserting it into HTML.
        rows = "".join(
            "<tr><th align='left' style='padding:8px'>"
            + html.escape(label)
            + "</th><td style='padding:8px'>"
            + html.escape(cleaned[key])
            + "</td></tr>"
            for key, label in {
                "company_name": "Company",
                "contact_name": "Contact",
                "contact_email": "Email",
                "product_id": "Product ID",
                "part_number": "Part number",
                "quantity": "Quantity",
                "fleet_size": "Fleet size",
                "requirements": "Requirements",
            }.items()
        )

        subject = (
            "[ROBOPARTS RFQ] "
            + cleaned["company_name"][:120]
        )
        body_html = (
            "<h2>New ROBOPARTS.ai Request for Quotation</h2>"
            "<table border='1' cellspacing='0' "
            "style='border-collapse:collapse'>"
            + rows
            + "</table><p>Submitted through ROBOPARTS.ai.</p>"
        )

        try:
            graph_send_email(
                subject,
                body_html,
                cleaned["contact_email"],
            )
        except (HTTPError, URLError, TimeoutError, OSError):
            logger.exception("RFQ email delivery failed")
            json_response(self, 502, {
                "error": (
                    "We could not deliver your RFQ right now. "
                    "Please try again later or contact us directly."
                )
            })
            return
        except Exception:
            logger.exception("RFQ email processing failed")
            json_response(self, 500, {
                "error": "RFQ email service is not configured correctly."
            })
            return

        # Do not log the customer's submitted information.
        logger.info("RFQ email accepted by Microsoft Graph")
        json_response(self, 200, {
            "success": True,
            "message": "Your RFQ has been submitted successfully."
        })

    def log_message(self, format_string, *args):
        # Avoid logging request bodies or personal information.
        logger.info("HTTP request received")
