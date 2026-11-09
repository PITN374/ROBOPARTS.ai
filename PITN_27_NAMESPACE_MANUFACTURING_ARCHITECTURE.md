# PITN_27_NAMESPACE_MANUFACTURING_ARCHITECTURE.md

# PITN — THE 27-NAMESPACE HUMANOID ROBOT MANUFACTURING ARCHITECTURE

**Author:** Aaron Bailot  
**Project:** PITN — Persistent Identity and Traceability Network  
**Website:** https://powerinthenumbers.ai/ ROBOPARTS.ai RFQ pilot details  
**Contact:** powerinthenumbers@pitn.ai

**Core principle:**

CONNECT THE PHYSICAL COMPONENT TO THE INFORMATION THAT ALREADY DESCRIBES IT.

---

## 1. PURPOSE AND ARCHITECTURAL SCOPE

PITN's proposed 27-namespace architecture provides a structured way to identify and organize the physical components and assemblies that make up a humanoid robot.

Each namespace identifies a defined component category. Its associated records can connect that category to:

- Component descriptions and technical specifications
- Manufacturer and product identification
- Manufacturer part numbers and SKUs
- Engineering drawings and revisions
- Bills of Materials and assembly positions
- Required quantities
- Supplier quotations and pricing
- Production and delivery information
- Inspection and testing records
- Physical serial numbers and production lots
- Installation and replacement history
- Maintenance and lifecycle events

The purpose is to reduce fragmented component information and establish persistent relationships between physical hardware and its associated records.

This document addresses only the following 27 PITN-proposed namespace identifiers. It does not establish additional namespace categories.

## 2. THE 27-NAMESPACE REGISTER

| No. | Namespace | Primary classification |
|---:|---|---|
| 1 | `.robotsystem` | Complete humanoid robot |
| 2 | `.roboticarm` | Arm assemblies and their components |
| 3 | `.roboticleg` | Leg assemblies and their components |
| 4 | `.robotichand` | Hand and finger assemblies |
| 5 | `.roboticwrist` | Wrist assemblies and interfaces |
| 6 | `.actuator` | Devices and assemblies producing controlled motion |
| 7 | `.reducer` | Mechanical speed and torque reduction |
| 8 | `.mechanicalinterface` | Mechanical connections and mounting interfaces |
| 9 | `.encoder` | Position, angle, and rotational measurement |
| 10 | `.fastener` | Hardware used to secure physical components |
| 11 | `.robotsensor` | Robot sensing devices |
| 12 | `.sensingmodule` | Integrated sensing assemblies |
| 13 | `.torquesensor` | Torque measurement devices |
| 14 | `.forcesensor` | Force measurement devices |
| 15 | `.forcetorque` | Combined force-and-torque measurement devices |
| 16 | `.safetysensor` | Safety-related sensing devices |
| 17 | `.controlsystem` | Control electronics and distributed control hardware |
| 18 | `.robotcontroller` | Main robot computing and control units |
| 19 | `.batterymodule` | Battery packs and integrated battery assemblies |
| 20 | `.batterycell` | Individual energy-storage cells |
| 21 | `.powerconverter` | Electrical voltage and power conversion devices |
| 22 | `.visionmodule` | Integrated vision assemblies |
| 23 | `.visionsensor` | Devices used to capture visual information |
| 24 | `.cameramodule` | Camera hardware and camera assemblies |
| 25 | `.endeffector` | Hands, grippers, and working interfaces |
| 26 | `.toolchanger` | Mechanisms for changing attached tools |
| 27 | `.cableharness` | Integrated electrical and signal wiring assemblies |

The namespaces classify different parts of the physical robot. Some components may have relationships with multiple categories, but each physical item should have a clearly defined primary classification and a consistent identity.

---

## 3. DETAILED NAMESPACE DEFINITIONS

### 01 — `.robotsystem`

**Purpose:** Identify the complete humanoid robot as a manufactured and configured system.

The robot system is the parent identity connecting the robot's assemblies, components, configuration, and lifecycle.

Relevant information includes:

- Robot model and configuration
- Robot serial number
- Approved system BOM
- Installed arm, leg, hand, and wrist assemblies
- Installed actuation and sensing hardware
- Controller and power configuration
- Software and hardware configuration references
- Manufacturing completion records
- Final inspection and acceptance records
- Maintenance and modification history

**Quantity:** 1 complete robot per physical robot instance.

**Manufacturing relevance:** Provides the top-level reference for determining which components belong to a particular robot and which configuration was manufactured, inspected, delivered, or serviced.

**RFQ relevance:** Supports consolidation of component requirements into a production-level purchasing plan. It is not itself a substitute for the detailed specifications required in individual component quotations.

### 02 — `.roboticarm`

**Purpose:** Classify the physical arm assemblies used for manipulation and movement.

Relevant components include:

- Upper-arm structural links
- Forearm links
- Shoulder and elbow joint housings
- Actuator mounting brackets
- Mechanical connections
- Bearings and shafts
- Arm wiring and sensor connections
- Protective covers

**Quantity:** Determined by the robot's approved configuration. A conventional two-arm humanoid configuration has two arm assemblies.

**Manufacturing relevance:** Connects each arm's structural and mechanical components to its assembly position, component identities, drawings, and revision history.

**RFQ relevance:** Supports quotations for arm structures, machined links, brackets, housings, and associated mechanical assemblies.

### 03 — `.roboticleg`

**Purpose:** Classify the lower-body assemblies responsible for supporting and moving the robot.

Relevant components include:

- Hip and knee structures
- Thigh and lower-leg links
- Joint housings
- Foot structures
- Actuator mounting interfaces
- Bearings and shafts
- Structural brackets
- Protective covers
- Associated wiring and sensing hardware

**Quantity:** Determined by the approved robot configuration. A conventional two-leg humanoid configuration has two leg assemblies.

**Manufacturing relevance:** Connects structural requirements with joint mechanisms, component placement, mechanical interfaces, and the leg assembly's BOM.

**RFQ relevance:** Supports quotation requests for structural members, machined housings, joint components, and foot assemblies.

### 04 — `.robotichand`

**Purpose:** Classify the physical hand assemblies and their subordinate finger structures.

Relevant components include:

- Palm assemblies
- Fingers and thumbs
- Proximal, intermediate, and distal phalanges
- Finger joints
- Finger actuators
- Tendons and linkages
- Pulleys and gears
- Bearings and bushings
- Tactile sensors
- Fingertip contact pads
- Hand fasteners

**Illustrative quantity:**

| Component | Quantity per robot |
|---|---:|
| Palm assemblies | 2 |
| Fingers | 10 |
| Phalanges | 30–50 |
| Finger joints | 30–50 |
| Finger actuators | 10–20 |
| Tendons and linkages | 30–100 |
| Pulleys and gears | 30–100 |
| Bearings and bushings | 50–150 |
| Tactile sensors | 20–100 |
| Fingertip pads | 10 |
| Fasteners | 100–300 |

**Manufacturing relevance:** Hand assemblies contain multiple small mechanical and sensing components. Their individual identities allow a manufacturer to trace the specific parts installed in each hand.

**RFQ relevance:** Supports separate quotation requirements for hand assemblies, miniature actuators, finger mechanisms, tactile sensors, and precision mechanical parts.

### 05 — `.roboticwrist`

**Purpose:** Classify the mechanical assembly connecting an arm to its hand or end-effector.

Relevant components include:

- Wrist joint housings
- Rotary mechanisms
- Bearings
- Shafts
- Actuators
- Reducers
- Encoders
- Mechanical mounting interfaces
- Electrical connections
- Protective components

**Quantity:** Configuration-dependent. The wrist may be integrated into an arm or hand assembly and should not automatically be counted as a separate manufactured assembly.

**Manufacturing relevance:** Provides a distinct classification for the wrist's mechanical and functional interface, supporting identification of its installed components and configuration.

**RFQ relevance:** Supports quotations for wrist mechanisms, compact actuation hardware, bearings, housings, and interface components.

### 06 — `.actuator`

**Purpose:** Classify the devices and assemblies that generate controlled mechanical movement.

Relevant components include:

- Rotary actuators
- Linear actuators
- Electric actuators
- Servo actuators
- Integrated joint actuator modules
- Electric motors
- Motor housings
- Actuator shafts
- Bearings
- Brakes
- Connectors
- Thermal components

**Illustrative quantity:**

| Component | Quantity per robot |
|---|---:|
| Electric motors and actuators | 30–50 |
| Finger actuators | 10–20 |
| Actuator housings | 80–200 |
| Shafts | 50–120 |
| Bearings | 100–250 |
| Brakes | 0–40 |

**Manufacturing relevance:** Actuators are important functional assemblies whose specifications affect robot movement, joint performance, physical integration, and component purchasing.

**RFQ relevance:** An actuator quotation may require torque, speed, dimensions, electrical requirements, duty cycle, interfaces, material specifications, inspection criteria, unit pricing, tooling charges, and delivery schedules.

### 07 — `.reducer`

**Purpose:** Classify mechanical assemblies that reduce rotational speed and increase available output torque.

Relevant components include:

- Harmonic-type reducers
- Planetary gear reducers
- Cycloidal reducers
- Gear assemblies
- Input and output shafts
- Bearings
- Housing components
- Lubrication-related components
- Mounting interfaces

**Illustrative quantity:** 30–50 reducers per robot in the supplied planning model.

**Manufacturing relevance:** Reducers are frequently associated with individual joints and actuator assemblies. Their product revision, ratio, mechanical interface, and performance requirements must be associated with the correct installation position.

**RFQ relevance:** Supplier quotations should identify reduction ratio, torque capacity, allowable speed, backlash, dimensions, mounting configuration, materials, testing requirements, and delivery lead time.

### 08 — `.mechanicalinterface`

**Purpose:** Classify the physical connection points and mechanical interface components joining assemblies.

Relevant components include:

- Couplings
- Spacers
- Mounting interfaces
- Joint connections
- Actuator interfaces
- Tool mounting interfaces
- Alignment features
- Mechanical adapters
- Interface plates

**Illustrative quantity:** 100–300 couplings and spacers in the supplied planning model.

**Manufacturing relevance:** Interface information connects two otherwise separately identified assemblies. It helps establish which component fits which mounting position and which revision of the interface is required.

**RFQ relevance:** Quotations can specify dimensions, tolerances, materials, surface finishes, fit requirements, and inspection measurements.

### 09 — `.encoder`

**Purpose:** Classify devices that measure position, rotation, or angular movement.

Relevant components include:

- Rotary encoders
- Absolute encoders
- Incremental encoders
- Resolvers
- Encoder housings
- Mounting components
- Signal connections

**Illustrative quantity:** 30–60 encoders per robot.

**Manufacturing relevance:** Encoder identity connects the device to its measurement range, resolution, electrical interface, mounting requirements, and installation location.

**RFQ relevance:** A quotation can specify resolution, accuracy, measurement range, operating speed, communication interface, electrical requirements, and environmental conditions.

**Counting rule:** An encoder already counted as part of an actuator or sensing subsystem must not be counted a second time when calculating the total number of physical parts.

### 10 — `.fastener`

**Purpose:** Classify the hardware used to secure, retain, and assemble robot components.

Relevant components include:

- Bolts
- Screws
- Nuts
- Washers
- Pins
- Rivets
- Threaded inserts
- Retaining hardware

**Illustrative quantity:**

| Fastener application | Quantity per robot |
|---|---:|
| Actuation fasteners | 500–1,500 |
| Structural fasteners | 300–800 |
| Hand fasteners | 100–300 |

These are application-level ranges from the supplied model and may overlap.

**Manufacturing relevance:** Fasteners can have low individual unit costs but significant aggregate purchasing quantities. Correct identification prevents confusion between dimensions, materials, thread specifications, finishes, and strength requirements.

**RFQ relevance:** Quotations should specify dimensions, material, finish, strength requirements, thread form, quantity, packaging, and delivery.

### 11 — `.robotsensor`

**Purpose:** Provide the broad classification for sensing devices used throughout the robot.

Relevant components include:

- Position sensors
- Inertial sensors
- Temperature sensors
- Proximity sensors
- Force sensors
- Torque sensors
- Tactile sensors
- Vision sensing devices

**Illustrative broad sensing quantity:** 150–450 components per robot in the supplied model.

**Manufacturing relevance:** Provides a common classification for robot sensing devices while preserving their more specific identities and functional categories.

**RFQ relevance:** Supports sourcing requirements for sensor performance, measurement range, accuracy, interfaces, environmental requirements, testing, and delivery.

**Counting rule:** This broad sensing quantity overlaps with specific sensor categories. It must not be added to the quantities for encoders, torque sensors, force sensors, and other sensors without deduplication.

### 12 — `.sensingmodule`

**Purpose:** Classify integrated sensing assemblies that combine multiple sensing elements or supporting electronics into one functional unit.

Relevant items may include:

- Integrated sensor assemblies
- Sensor mounting structures
- Sensor interface electronics
- Combined measurement modules
- Sensor housings
- Integrated signal connections

**Quantity:** No independent quantity established in the supplied model.

**Manufacturing relevance:** Distinguishes an integrated sensing assembly from the individual sensors installed within it.

**RFQ relevance:** Allows suppliers to quote a complete sensing assembly while retaining the ability to identify its internal components separately.

### 13 — `.torquesensor`

**Purpose:** Classify devices that measure rotational torque within a joint, actuator, or mechanical transmission.

Relevant components include:

- Joint torque sensors
- Torque transducers
- Sensor mounting components
- Signal interfaces
- Associated electronics

**Illustrative quantity:** 20–40 per robot.

**Manufacturing relevance:** Connects each torque measurement device to its measurement range, mounting position, calibration information, and associated joint.

**RFQ relevance:** Quotations should include measurement range, accuracy, overload capacity, output interface, dimensions, calibration requirements, and delivery.

### 14 — `.forcesensor`

**Purpose:** Classify devices that measure applied physical force.

Relevant applications include:

- Foot contact measurement
- Load measurement
- Interaction force measurement
- Contact detection
- Mechanical loading measurement

**Illustrative quantity:** 10–30 per robot.

**Manufacturing relevance:** Connects the sensor's identity with its physical measurement location, specifications, test results, and replacement history.

**RFQ relevance:** Supplier quotations should define measurement range, sensitivity, accuracy, loading conditions, electrical interface, and inspection requirements.

### 15 — `.forcetorque`

**Purpose:** Classify combined force-and-torque measurement devices.

Relevant components include:

- Multi-axis force-and-torque sensors
- Integrated measurement assemblies
- Sensor mounting interfaces
- Signal conditioning electronics
- Associated connectors

**Quantity:** No separate verified quantity established in the supplied model.

**Manufacturing relevance:** Provides a specific classification when one device measures both applied force and torque.

**RFQ relevance:** Requests should define measurement axes, measurement ranges, accuracy, overload limits, mechanical dimensions, calibration, and electrical interface.

**Counting rule:** A combined force-and-torque device must not be counted again as two separate physical devices simply because it measures two types of force-related values.

### 16 — `.safetysensor`

**Purpose:** Classify sensors used to detect physical conditions relevant to safe robot operation.

Potential components include:

- Contact detection sensors
- Proximity sensing devices
- Protective-area sensing devices
- Safety-related position sensors
- Temperature monitoring devices where used for protection
- Associated sensing interfaces

**Quantity:** Configuration-dependent; no independent verified quantity established in the supplied model.

**Manufacturing relevance:** Connects each device to its intended function, location, technical specification, inspection evidence, and replacement history.

**RFQ relevance:** Supplier requests should identify the intended protective function, operating conditions, detection range, response characteristics, electrical interface, and required verification evidence.

**Important distinction:** A namespace classification does not establish that a sensor or complete robot satisfies any particular safety requirement.

### 17 — `.controlsystem`

**Purpose:** Classify the distributed electronic hardware responsible for processing commands and coordinating robot operation.

Relevant components include:

- Main controller circuit boards
- Motor-control boards
- Power electronics boards
- Sensor-interface boards
- Communication boards
- Servo-control electronics
- Control-related memory and storage modules

**Illustrative quantity:**

| Component | Quantity per robot |
|---|---:|
| Main controller boards | 1–3 |
| Motor-control boards | 20–50 |
| Power electronics boards | 10–30 |
| Communication boards | 5–20 |
| Sensor-interface boards | 10–40 |

**Manufacturing relevance:** Connects individual control boards to their board revisions, installed components, interfaces, manufacturing records, and robot configuration.

**RFQ relevance:** Supports quotation requests for printed circuit board fabrication, assembly, electronic components, testing, programming requirements, and delivery.

### 18 — `.robotcontroller`

**Purpose:** Classify the main computing and control units coordinating robot functions.

Relevant components include:

- Embedded computers
- CPU modules
- GPU modules
- AI computing modules
- Main controller units
- Motion computing hardware
- Controller enclosures
- Memory and storage devices

**Illustrative quantity:** 1–4 main computing units per robot.

**Manufacturing relevance:** Connects the robot's primary computing hardware to its product identity, hardware revision, configuration, installed software references, and service history.

**RFQ relevance:** Supplier quotations may require processor specifications, computing performance, memory capacity, electrical requirements, thermal requirements, physical dimensions, and availability.

**Distinction from `.controlsystem`:** `.robotcontroller` identifies the main computing and control units; `.controlsystem` identifies the broader control electronics and distributed hardware.

### 19 — `.batterymodule`

**Purpose:** Classify complete battery packs and integrated battery assemblies.

Relevant components include:

- Battery packs
- Battery module housings
- Electrical connections
- Module-level monitoring hardware
- Protective components
- Internal support structures

**Illustrative quantity:** 1–10 battery modules per robot.

**Manufacturing relevance:** Connects the battery assembly to its product specifications, configuration, manufacturing records, inspection information, and replacement history.

**RFQ relevance:** Supplier quotations should define capacity, voltage, dimensions, weight, electrical interface, operating limits, protective features, testing requirements, and delivery.

### 20 — `.batterycell`

**Purpose:** Classify individual energy-storage cells within battery modules.

Relevant information includes:

- Cell manufacturer
- Cell model
- Chemistry designation
- Cell capacity
- Voltage characteristics
- Production lot
- Individual serial identification where available
- Inspection and test results
- Module installation position

**Illustrative quantity:** 100–500 cells per robot.

**Manufacturing relevance:** Connects the individual cell or production lot to the battery module in which it is installed.

**RFQ relevance:** Supplier quotations should specify cell model, chemistry, capacity, dimensions, electrical characteristics, lot information, testing, minimum order quantities, and lead time.

**Counting rule:** Battery cells are subordinate physical items within battery modules. They should not be mistaken for additional battery modules.

### 21 — `.powerconverter`

**Purpose:** Classify devices that convert electrical power between required voltage or power conditions.

Relevant components include:

- DC/DC converters
- Inverters
- Voltage conversion devices
- Power conversion modules
- Associated electrical interfaces

**Illustrative quantity:** 5–20 converters per robot.

**Manufacturing relevance:** Connects each converter to its electrical ratings, physical installation, product revision, thermal requirements, and service records.

**RFQ relevance:** Quotations should define input and output voltage, current, power rating, efficiency requirements, operating temperature, physical dimensions, interfaces, and testing.

### 22 — `.visionmodule`

**Purpose:** Classify integrated vision assemblies used to capture and process visual information.

Relevant components may include:

- Integrated camera assemblies
- Stereo vision assemblies
- Depth sensing assemblies
- Mounting hardware
- Supporting electronics
- Integrated optical components

**Quantity:** No separate verified quantity established in the supplied model.

**Manufacturing relevance:** Identifies the complete vision assembly as a functional unit while preserving the identities of its constituent cameras, sensors, and electronic components.

**RFQ relevance:** Supports quotation requests for complete vision assemblies, including field of view, image resolution, depth capabilities, mounting, electrical connections, and environmental requirements.

### 23 — `.visionsensor`

**Purpose:** Classify the individual sensing devices used to obtain visual information.

Relevant devices include:

- RGB cameras
- Stereo cameras
- Depth cameras
- Other visual sensing devices

**Quantity:** Visual devices are included in the supplied camera estimate of 4–12 per robot. No additional independent quantity should be assumed.

**Manufacturing relevance:** Separates the identity of an individual vision sensor from the integrated vision assembly in which it may be installed.

**RFQ relevance:** Supplier quotations should define resolution, frame rate, field of view, interface, sensing range where applicable, physical dimensions, and environmental requirements.

### 24 — `.cameramodule`

**Purpose:** Classify camera hardware and camera assemblies installed on the robot.

Relevant components include:

- RGB camera assemblies
- Stereo camera assemblies
- Depth camera assemblies
- Camera housings
- Optical components
- Mounting interfaces
- Camera connectors

**Illustrative quantity:** 4–12 camera assemblies per robot.

**Manufacturing relevance:** Connects each camera to its model, hardware revision, physical position, technical specifications, and replacement history.

**RFQ relevance:** Supports comparable supplier quotations for image quality, resolution, frame rate, field of view, optical configuration, interface, dimensions, and delivery.

**Counting rule:** A camera may also be represented within a vision module or broad sensing classification. It must not be counted more than once in a physical inventory.

### 25 — `.endeffector`

**Purpose:** Classify the working interface through which the robot interacts with objects and its surroundings.

Relevant items include:

- Robotic hands
- Grippers
- Attached working tools
- Tool mounting interfaces
- Contact surfaces
- End-effector assemblies

**Illustrative quantity:** Two hand/palm working assemblies in the supplied humanoid example. Additional tools depend on configuration.

**Manufacturing relevance:** Establishes the identity of the functional assembly at the point where the robot performs physical work.

**RFQ relevance:** Supports quotations for complete hands, grippers, mechanical interfaces, contact surfaces, and interchangeable working equipment.

**Distinction from `.robotichand`:** `.robotichand` classifies the hand structure and its internal components. `.endeffector` classifies the working interface or tool assembly.

### 26 — `.toolchanger`

**Purpose:** Classify mechanisms that connect, release, or exchange tools and working attachments.

Relevant components include:

- Tool coupling mechanisms
- Mechanical locking components
- Release mechanisms
- Alignment interfaces
- Electrical contacts
- Pneumatic or other utility connections where applicable
- Associated fasteners and housings

**Quantity:** Configuration-dependent; no independent quantity established in the supplied model.

**Manufacturing relevance:** Connects the tool-changing mechanism to the compatible tool, attachment, mounting interface, and robot configuration.

**RFQ relevance:** Supplier quotations should define interface dimensions, locking requirements, load capacity, connection types, operating requirements, and verification procedures.

### 27 — `.cableharness`

**Purpose:** Classify integrated electrical and signal wiring assemblies connecting the robot's systems.

Relevant components include:

- Motor cable assemblies
- Sensor harnesses
- Power harnesses
- Communication harnesses
- Wires
- Connectors
- Terminals
- Cable glands
- Cable carriers
- Shielding components
- Strain-relief hardware

**Illustrative quantity:**

| Component | Quantity per robot |
|---|---:|
| Cable assemblies | 50–150 |
| Individual wire segments | 200–800 |
| Connectors | 100–400 |
| Terminals | 300–1,000 |
| Cable glands | 20–80 |
| Cable carriers | 10–40 |
| Shielding components | 20–100 |

**Manufacturing relevance:** Connects electrical assemblies to their destination, connection type, cable specification, length, routing, connector configuration, and installation position.

**RFQ relevance:** Supplier quotations should specify wire type, conductor size, cable length, connector part numbers, terminal requirements, shielding, labeling, testing, and delivery.

---

## 4. HOW THE 27 NAMESPACES CONNECT TO THE HUMANOID BOM

The namespaces provide classification and relationships across the physical manufacturing hierarchy.

```text
.robotsystem
│
├── .roboticarm
│   ├── .roboticwrist
│   ├── .actuator
│   ├── .reducer
│   ├── .mechanicalinterface
│   ├── .encoder
│   └── .fastener
│
├── .roboticleg
│   ├── .actuator
│   ├── .reducer
│   ├── .mechanicalinterface
│   ├── .encoder
│   └── .fastener
│
├── .robotichand
│   ├── .actuator
│   ├── .mechanicalinterface
│   ├── .robotsensor
│   ├── .torquesensor
│   └── .fastener
│
├── .endeffector
│   └── .toolchanger
│
├── .robotsensor
│   ├── .sensingmodule
│   ├── .encoder
│   ├── .torquesensor
│   ├── .forcesensor
│   ├── .forcetorque
│   ├── .safetysensor
│   └── .visionsensor
│
├── .visionmodule
│   └── .cameramodule
│       └── .visionsensor
│
├── .controlsystem
│   └── .robotcontroller
│
├── .batterymodule
│   └── .batterycell
│
├── .powerconverter
│
└── .cableharness
```

This diagram shows functional relationships, not mandatory physical nesting. Actual relationships must be established from the robot's engineering design and approved BOM.

A component may be associated with several relevant functional categories without receiving duplicate physical inventory counts.

---

## 5. THE MANUFACTURING INFORMATION RECORD

Every identified component can be connected to a consistent set of information.

An illustrative component record may contain:

| Information field | Purpose |
|---|---|
| PITN namespace | Identifies the classification |
| PITN persistent identity | Identifies the registered record or physical instance |
| Component description | Explains what the item is |
| Manufacturer | Identifies the stated source |
| Manufacturer part number | Preserves the manufacturer's product identifier |
| SKU | Identifies the purchasing or inventory item |
| Product revision | Identifies the applicable design version |
| BOM position | Identifies where the item belongs |
| Required quantity | Identifies the quantity needed |
| Production lot | Connects the item to a manufacturing batch |
| Serial number | Distinguishes an individually serialized item |
| Technical specification | Describes required characteristics |
| Drawing reference | Connects the item to engineering documentation |
| Supplier reference | Connects the item to sourcing information |
| RFQ reference | Connects the item to a quotation request |
| Quoted price | Records the supplier's quoted price |
| Quotation validity | Records the period during which the quotation applies |
| Lead time | Records the stated delivery estimate |
| Inspection evidence | Connects the item to inspection records |
| Installation reference | Identifies the installed robot or assembly |
| Lifecycle status | Records the item's documented lifecycle state |

A field may remain unpopulated until verified information is available. Missing information should be identified as missing rather than invented or assumed.

---

## 6. ROBO PARTS, SKU IDENTIFICATION, AND PHYSICAL COUNTS

The distinction between a product identifier and a physical quantity is essential to accurate manufacturing information.

Consider an actuator with the product identifier:

`ACT-HIP-001`

If a robot requires two identical hip actuators:

- Unique product identifiers: 1
- Physical actuator instances: 2

Consider a fastener with the product identifier:

`FST-M6-001`

If the robot requires 600 identical fasteners:

- Unique product identifiers: 1
- Physical fastener instances: 600

The PITN architecture can preserve the product identity while distinguishing the individual physical instances where individual traceability is needed.

This distinction prevents SKU counts, BOM quantities, and physical part counts from being confused.

---

## 7. THE 27 NAMESPACES IN THE RFQ PROCESS

The namespaces can connect engineering requirements to purchasing information without changing the purpose of an RFQ.

An RFQ asks a supplier to quote a defined product, component, or assembly at a specified quantity and against stated requirements.

The PITN namespace provides a consistent classification for the item being quoted.

### RFQ information connected to a namespace

| RFQ information | PITN relationship |
|---|---|
| Component category | Relevant namespace |
| Part description | Component identity |
| Drawing and specifications | Technical information |
| Manufacturer part number | Product identification |
| Required quantity | BOM requirement |
| Material requirements | Component specification |
| Dimensional tolerances | Technical requirement |
| Quality requirements | Inspection criteria |
| Unit price | Supplier quotation |
| Setup and tooling costs | Quotation cost breakdown |
| Delivery schedule | Supplier lead-time information |
| Quote validity | Commercial quotation record |
| Supplier response | Sourcing record |

### Illustrative RFQ examples

| Namespace | Quoted item | Example quantity for 1,000 robots |
|---|---|---:|
| `.actuator` | Joint actuator | 30,000–50,000 |
| `.reducer` | Gear reducer | 30,000–50,000 |
| `.robotichand` | Hand assemblies | 1,000 pairs |
| `.mechanicalinterface` | Couplings and spacers | 100,000–300,000 |
| `.cableharness` | Cable assemblies | 50,000–150,000 |
| `.batterymodule` | Battery modules | 1,000–10,000 |
| `.batterycell` | Battery cells | 100,000–500,000 |
| `.cameramodule` | Camera assemblies | 4,000–12,000 |

These are arithmetic extensions of the supplied per-robot planning ranges to a hypothetical production quantity of 1,000 robots. They are not supplier commitments or confirmed procurement requirements.

Actual purchasing quantities must account for approved configurations, production yield, spares, replacement stock, minimum order quantities, and other documented requirements.

---

## 8. PILOT RFQ AND PRODUCTION VALIDATION

A pilot RFQ allows a manufacturer to obtain supplier quotations for a limited initial production requirement before making a larger purchasing commitment.

The 27 namespaces provide a consistent way to classify the items included in that process.

A pilot can evaluate:

1. Whether the quoted component matches the required identity and revision.
2. Whether the supplier can manufacture the specified quantity.
3. Whether the stated material and dimensional requirements can be met.
4. Whether tooling and setup costs are acceptable.
5. Whether sample production and delivery schedules are achievable.
6. Whether inspection records can be associated with the supplied parts.
7. Whether the component can be integrated into the intended assembly.
8. Whether the quotation remains comparable when production volume increases.

A quotation is not a purchase order. A pilot RFQ is not an obligation to purchase.

The namespace provides the information connection; commercial decisions remain subject to the manufacturer's purchasing process and applicable agreements.

---

## 9. COMPARING SUPPLIER QUOTATIONS

A supplier comparison should distinguish technical suitability from commercial price.

For the same identified component, a manufacturer can compare:

| Comparison field | Supplier A | Supplier B | Supplier C |
|---|---|---|---|
| Product identity | Required | Required | Required |
| Revision | Confirm | Confirm | Confirm |
| Technical compliance | Evaluate | Evaluate | Evaluate |
| Unit price | Quoted | Quoted | Quoted |
| Tooling/setup cost | Quoted | Quoted | Quoted |
| Minimum order quantity | Quoted | Quoted | Quoted |
| Sample lead time | Quoted | Quoted | Quoted |
| Production lead time | Quoted | Quoted | Quoted |
| Inspection evidence | Review | Review | Review |
| Quote validity | Record | Record | Record |

The comparison should use equivalent specifications and quantities.

The lowest quoted price does not automatically establish that a supplier is technically suitable or that the delivery schedule is achievable.

PITN's role is to preserve the identity and information relationships needed to make that comparison consistently.

---

## 10. QUANTITY AND MANUFACTURING COMPLEXITY

The supplied planning model identifies several different levels of humanoid manufacturing complexity.

| Measurement level | Supplied planning range |
|---|---:|
| Major assemblies | Approximately 500–1,500 |
| Manufactured parts | Approximately 4,000–10,000+ |
| Individual electronic components, when counted separately | Approximately 10,000–100,000+ |
| Battery cells | Approximately 100–500+ |

These figures are planning estimates from the supplied model, not verified totals for a particular robot.

The figures must not be added together indiscriminately.

For example:

- A motor may already be included within an actuator assembly.
- An encoder may appear in both an actuation breakdown and a sensing breakdown.
- A camera may be included in a vision assembly.
- A connector may be included within a cable harness.
- A battery cell is contained within a battery module.
- Fasteners may appear in structural, actuation, and hand-level estimates.

A defensible total requires a single reconciled BOM with explicit counting rules.

### Why the 27 namespaces improve quantity management

They make it possible to distinguish:

- Which component category is being counted.
- Which individual product is being purchased.
- Which assembly contains the component.
- How many physical instances are required.
- Which components are included in a supplier quotation.
- Which quantities are already included in a higher-level assembly.
- Which quantities are still estimates and require engineering approval.

This is essential when moving from a prototype to pilot production and then to larger manufacturing volumes.

---

## 11. INFORMATION TRACEABILITY ACROSS THE COMPONENT LIFECYCLE

The namespaces can maintain a continuous relationship between a component's original identification and its documented manufacturing history.

```text
NAMESPACE CLASSIFICATION
          │
          ▼
PERSISTENT COMPONENT IDENTITY
          │
          ▼
PRODUCT / MANUFACTURER INFORMATION
          │
          ▼
ENGINEERING SPECIFICATION
          │
          ▼
APPROVED BOM POSITION
          │
          ▼
RFQ AND SUPPLIER QUOTATION
          │
          ▼
PURCHASE AND RECEIVING RECORD
          │
          ▼
INSPECTION AND TEST INFORMATION
          │
          ▼
ASSEMBLY AND INSTALLATION
          │
          ▼
MAINTENANCE AND REPLACEMENT
          │
          ▼
LIFECYCLE HISTORY
```

Each stage can reference the same persistent component identity.

The original manufacturer's part number and source information remain distinguishable from the PITN identity.

A change in supplier, revision, installation location, or lifecycle status should be represented as a documented relationship or event rather than silently overwriting historical information.

---

## 12. OPTIONAL BLOCKCHAIN EVENT INTEGRITY

A blockchain or append-only ledger can complement the 27-namespace architecture by recording references to component-related events.

An illustrative event may include:

- PITN component identity
- Namespace classification
- Event type
- Event timestamp
- Submitting identity
- Relevant BOM or installation reference
- Supporting document reference
- Cryptographic hash of the referenced record
- Reference to the preceding event

Example:

```text
EVENT: COMPONENT_RECEIVED

NAMESPACE: .actuator

PITN_ID: PITN-ACT-000238

PRODUCT_ID: ACT-4721

SERIAL: SN-100238

ROBOT_REFERENCE: HUM-SN-0001

EVENT_STATUS: RECEIVED

DOCUMENT_REFERENCE: RECEIVING-RECORD-001

TIMESTAMP: RECORDED AT EVENT CREATION
```

This is an illustrative data structure, not a claim of an existing deployed transaction.

The underlying engineering documents, supplier quotations, and confidential records may remain in authorized storage systems.

A ledger can help preserve the history of submitted records and detect subsequent changes to referenced data. It does not independently establish the truth of a submitted claim, the authenticity of a physical component, or the correctness of an inspection.

---

## 13. THE PRACTICAL VALUE OF THE 27-NAMESPACE STRUCTURE

The 27 namespaces address separate but connected information requirements across humanoid manufacturing.

Their practical value can be understood through five manufacturing activities.

**Engineering**

Components can be associated with their descriptions, specifications, revisions, assembly locations, and approved BOM positions.

**Procurement**

Required components can be classified and connected to supplier information, RFQs, quantities, quoted prices, and delivery schedules.

**Manufacturing**

Parts can be associated with the assemblies in which they are installed, along with the relevant production and inspection records.

**Quality and traceability**

Identities can connect individual components or lots to documented inspections, tests, and supporting evidence.

**Maintenance and lifecycle**

Installed parts can be associated with their service history, replacement records, configuration changes, and lifecycle events.

The objective is to reduce the repeated effort required to identify, retrieve, reconcile, and verify manufacturing information.

---

## 14. IMPLEMENTATION REQUIREMENTS

A functional implementation of the 27 namespaces requires consistent rules.

1. Define the meaning and scope of every namespace.
2. Establish assignment and collision-prevention procedures.
3. Define persistent identity formats.
4. Preserve original manufacturer identifiers.
5. Distinguish product records from individual physical instances.
6. Define relationships between assemblies and their components.
7. Establish consistent BOM counting rules.
8. Record technical revisions and configuration changes.
9. Connect component records to RFQs and supplier responses.
10. Preserve source attribution and evidence references.
11. Define permissions for confidential manufacturing information.
12. Establish event and lifecycle record formats.
13. Test identity resolution and duplicate detection.
14. Reconcile quantities against the approved engineering BOM.

The namespace definitions, identifiers, and governance procedures must be maintained as controlled PITN architecture documentation. The existence of a proposed namespace does not itself establish public DNS delegation or exclusive legal rights to a suffix.

---

## 15. DEFINITIVE ARCHITECTURAL STATEMENT

The 27 PITN-proposed namespace identifiers provide a classification structure for connecting the physical components of a humanoid robot to the information required to design, quote, purchase, manufacture, inspect, install, maintain, and replace them.

Each namespace addresses a defined component category.

Together, they provide a consistent framework through which component identities, manufacturer information, SKUs, BOM positions, quantities, supplier quotations, technical records, and lifecycle events can be related.

The architecture connects engineering information to procurement information and manufacturing information without requiring those records to lose their original source attribution.

A component should not have to be repeatedly rediscovered every time it moves from engineering to purchasing, from purchasing to manufacturing, or from manufacturing to maintenance.

Its identity and associated information should remain connected.

**PITN's 27-namespace architecture is designed to make that connection persistent, structured, and reusable.**

---

**PITN — POWER IN THE NUMBERS**

**Persistent Identity and Traceability Network**

**Author:** Aaron Bailot

**Recover the Past. Identify the Present. Engineer the Future.**

**Intelligence with the Ability to Act.**
