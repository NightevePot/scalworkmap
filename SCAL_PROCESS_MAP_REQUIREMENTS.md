# SCAL End-to-End Process Map

## Goal

Create a business-oriented HTML process map that explains the end-to-end SCAL workflow across the MES, PDA, client, and database codebases. The map must make each process step traceable to its implementation and, where available, to a working business-page demo.

## Main Flow

The initial top-level workflow is a seven-stage linear chain:

```text
Procurement -> Receiving -> Quality Inspection -> Material Loading -> Weighing -> Formula Output -> Case Closure
```

Each stage contains multiple subprocesses. A subprocess at the end of one stage connects to the starting subprocess of the next stage. For example:

```text
Procurement
  -> Barcode application
  -> Label distribution
  -> Scan receiving
  -> Sampling label (Quality Inspection)
```

The exact subprocesses and connections will be confirmed from the source repositories and documentation rather than inferred from names alone.

## Intended Experience

The first screen presents the seven main stages as a compact, left-to-right process chain. Small, low-emphasis subprocess blocks remain visible to indicate depth without overwhelming the overview.

Selecting a main stage or local hotspot transitions the viewport into that area and expands its subprocesses and connectors. A subprocess can expose evidence and links, including:

- Owning system: web MES (BS), desktop MES client (CS), PDA, backend API, or database.
- Relevant source modules, interfaces, database tables, and stored procedures.
- Linked business demo page, such as the procurement barcode-application page.

The visual direction is restrained and business-focused: clear system swimlanes, stable typography, directional connectors, and high information density without decorative visual noise.

## Research Sources

| Source | Location | Planned Use |
| --- | --- | --- |
| Database snapshot | `E:\code\xxaedatabase` | Tables, fields, stored procedures, database-side business rules. |
| Web MES (BS) | `E:\code\scal-mes` | Browser-side MES entry points, APIs, and business/data-access layers. |
| Desktop MES (CS) | `E:\code\scal-mes-client` | Windows client-side manufacturing workflows and service calls. |
| PDA frontend | `E:\code\scal-pda-f` | PDA page flows and API calls. |
| PDA backend | `E:\code\scal-pda-b` | PDA endpoints and business services. |
| Documentation and demos | `E:\code\scal-mes（副本）\TEMPS\DOC` | `main` and `tables`: schema/field relationships. `business`: demo pages for process-step examples. |

## Working Method

1. Inventory the six sources and identify business modules, APIs, database artifacts, documentation, and demos.
2. Establish the verified subprocesses for each of the seven main stages.
3. For every subprocess, record its predecessor and successor, participating systems, implementation evidence, data entities, and optional demo target.
4. Model the result as structured process data so the HTML map is generated from verified relationships rather than hand-drawn coordinates alone.
5. Build the interactive HTML overview and stage-detail views, then attach source evidence and demo links.
6. Review gaps, ambiguous transitions, and cross-system handoffs with the process owner before treating the map as complete.

## Initial Deliverables

- A researched process inventory with evidence links.
- A structured flow definition covering main stages, subprocesses, systems, and transitions.
- An interactive HTML process map with overview, zoomed stage detail, and demo navigation.
- A research log of assumptions, unresolved links, and validation decisions.

## Items To Validate

- The definitive subprocess list and ordering for each of the seven stages.
- Which MES workflows are implemented in BS versus CS, and where they overlap.
- The source of truth for each cross-system status change and identifier.
- Mapping of each business-demo page to its real process step and implementation.
- Whether a demo link should open inside the map, in a detail drawer, or in a separate browser tab.
