# Hostel Room Allocation REST API (CRUD) with Postman Testing

SW426 Software Quality Engineering: PBL project. A database-connected REST API that
manages hostel rooms (Create, Read, Update, Delete), exchanges JSON, returns proper
HTTP status codes, validates input, and is tested with Postman and automated tests.

## Chosen entity: Room
| Field | Type | Rule |
|---|---|---|
| id | integer | Auto-generated primary key |
| room_no | text | Required, 2-10 letters/digits with optional hyphens (example A-101), **unique**, stored in capitals |
| block | text | Required, one of A, B, C, D, E, F |
| capacity | integer | Required, beds in the room, 1 to 6 |
| occupants | integer | Required, students living there now, 0 up to the capacity |
| monthly_fee | integer | Required, per student in PKR, 500 to 50000 |
| available_beds | integer | Calculated by the API (capacity minus occupants) |
| created_at | text | Set automatically |

## Tools and technologies
Python 3, Flask (REST framework), SQLite (database), Postman (API testing),
unittest (automated tests), Git/GitHub (source code).

## Folder structure
```
hostel-room-api/
  app.py          routes, status codes, error handling
  database.py     all SQL (placeholders only)
  validation.py   input rules for a Room
  schema.sql      database design (with CHECK rules)
  tests/          19 automated tests
  postman/        importable Postman collection (15 requests, 24 checks)
```

## Setup (VS Code terminal, inside this folder, one command at a time)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
The API runs at **http://localhost:3000/api/rooms**. The database file `rooms.db` is
created automatically on the first run.

## Test with Postman
1. Keep `python app.py` running.
2. Postman: **Import** the file `postman/Hostel_Room_API.postman_collection.json`.
3. Open the collection, click **Run**, then **Run Hostel Room Allocation API**.
4. All 15 requests should show green PASS. Take a screenshot of each request (request,
   response body and status code) and of the Runner summary for your report.
5. Run it a second time: it still passes, because TC-13 deletes the room it created.

## Automated tests
```bash
python -m unittest -v
```
19 tests, each on a fresh temporary database.

## API documentation
Base URL: `http://localhost:3000/api/rooms`

| Operation | Method and URL | Success | Errors |
|---|---|---|---|
| Create | POST /api/rooms | 201 Created | 400 invalid data, 409 duplicate room number |
| Read all | GET /api/rooms | 200 OK | - |
| Read rooms with free beds | GET /api/rooms?available=true | 200 OK | 400 if the value is not true/false |
| Read one | GET /api/rooms/{id} | 200 OK | 404 not found |
| Update | PUT /api/rooms/{id} | 200 OK | 400, 404, 409 |
| Delete | DELETE /api/rooms/{id} | 200 OK | 404 not found |

**POST /api/rooms request**
```json
{ "room_no": "c-301", "block": "C", "capacity": 3, "occupants": 1, "monthly_fee": 5500 }
```
**Response 201 Created**
```json
{ "id": 1, "room_no": "C-301", "block": "C", "capacity": 3, "occupants": 1,
  "monthly_fee": 5500, "available_beds": 2, "created_at": "2026-11-08 14:12:13" }
```
**PUT /api/rooms/1**: send all five fields. Response 200 with the updated room.

**DELETE /api/rooms/1 response 200**
```json
{ "message": "Room deleted successfully", "id": 1 }
```
**Error response 400 (invalid data)**
```json
{ "error": "Validation failed",
  "details": { "block": "Must be one of A, B, C, D, E, F",
               "occupants": "Cannot be more than the room capacity (3)" } }
```
**Error response 404**: `{ "error": "Room with id 9999 not found" }`
**Error response 409**: `{ "error": "A room with this room number already exists" }`

## Postman test cases (results of the run)
| ID | Scenario | Request | Expected | Actual | Status |
|---|---|---|---|---|---|
| TC-01 | Add a valid record | POST /api/rooms | 201, created room with id | 201 Created | Pass |
| TC-02 | Get all records | GET /api/rooms | 200, array with the room | 200 OK | Pass |
| TC-03 | Get one record | GET /api/rooms/{id} | 200, same id | 200 OK | Pass |
| TC-04 | Update a record | PUT /api/rooms/{id} | 200, occupants 3, fee 6500 | 200 OK | Pass |
| TC-05 | Verify update saved | GET /api/rooms/{id} | 200, occupants 3, 1 free bed | 200 OK | Pass |
| TC-06 | Rooms with free beds | GET /api/rooms?available=true | 200, only rooms with free beds | 200 OK | Pass |
| TC-07 | Missing required fields | POST /api/rooms | 400, missing fields named | 400 Bad Request | Pass |
| TC-08 | Invalid block, too many occupants | POST /api/rooms | 400, errors for block, occupants | 400 Bad Request | Pass |
| TC-09 | Duplicate room number | POST /api/rooms | 409 Conflict | 409 Conflict | Pass |
| TC-10 | Nonexistent ID | GET /api/rooms/9999 | 404 | 404 Not Found | Pass |
| TC-11 | Update nonexistent ID | PUT /api/rooms/9999 | 404 | 404 Not Found | Pass |
| TC-12 | Malformed JSON | POST /api/rooms | 400 | 400 Bad Request | Pass |
| TC-13 | Delete existing record | DELETE /api/rooms/{id} | 200 | 200 OK | Pass |
| TC-14 | Deleted record cannot be read | GET /api/rooms/{id} | 404 | 404 Not Found | Pass |
| TC-15 | Delete nonexistent ID | DELETE /api/rooms/9999 | 404 | 404 Not Found | Pass |

Run it on your own computer and keep your own screenshots as proof.

## Report checklist (the 11 items on the assignment sheet)
1. Title and student information
2. Problem statement and objectives
3. Chosen entity and attributes (table above)
4. Tools, technologies and database
5. Database design and schema (`schema.sql`)
6. API documentation with JSON examples (section above)
7. Postman test cases with screenshots and status codes
8. Error-handling and validation tests (TC-07 to TC-12, TC-14, TC-15)
9. Results, identified issues and conclusion
10. GitHub repository link
11. Presentation video link

## Upload to GitHub
```bash
git init
git add .
git commit -m "Hostel Room Allocation CRUD API with Postman tests"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/hostel-room-api.git
git push -u origin main
```
Create the empty repository on github.com first and make it **public** so the teacher can open it.

## Video checklist (3 to 5 minutes)
1. Say the purpose and the entity (Room).
2. Show the code folder and `schema.sql`; show the database file or stored records.
3. In Postman: POST, GET all, GET one, PUT, DELETE, then GET the deleted room (404).
4. Show the JSON request and response and the status code each time.
5. Show one error test (for example occupants more than capacity returns 400).
6. Show the GitHub repository and run the automated tests.
