# SCAL Project Research

## Objective

Understand the end-to-end SCAL project by jointly studying its PDA applications, MES applications, and database scripts.

## Repositories in Scope

| Area | Path | Purpose |
| --- | --- | --- |
| PDA frontend | `E:\code\scal-pda-f` | PDA client interface and frontend business logic. |
| PDA backend | `E:\code\scal-pda-b` | PDA APIs and backend business logic. |
| Web MES (BS) | `E:\code\scal-mes` | MES web site, APIs, and business/data-access layers. |
| Manufacturing MES client (CS) | `E:\code\scal-mes-client` | Windows desktop MES client application. |
| Database | `E:\code\xxaedatabase` | Database schema, stored procedures, and change scripts. |
| Documentation and demos | `E:\code\scal-mes（副本）\TEMPS\DOC` | Database table/field relationship documentation and business demo pages. |

## Research Approach

Trace a business workflow across the five repositories:

1. PDA or MES client entry point.
2. Corresponding backend API and service implementation.
3. Database queries, tables, and stored procedures.
4. Data returned to the client and its downstream usage.

Document discovered modules, interfaces, data flows, and unresolved questions in this file as the research progresses.
