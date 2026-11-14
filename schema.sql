-- Database design: one table for the Room entity (hostel room allocation)
CREATE TABLE IF NOT EXISTS rooms (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    room_no     TEXT    NOT NULL UNIQUE,                                   -- e.g. A-101, no duplicates
    block       TEXT    NOT NULL CHECK (block IN ('A','B','C','D','E','F')),
    capacity    INTEGER NOT NULL CHECK (capacity BETWEEN 1 AND 6),         -- beds in the room
    occupants   INTEGER NOT NULL CHECK (occupants >= 0),                   -- students living there now
    monthly_fee INTEGER NOT NULL CHECK (monthly_fee BETWEEN 500 AND 50000),-- per student, in PKR
    created_at  TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (occupants <= capacity)                                          -- a room can never be over-full
);
