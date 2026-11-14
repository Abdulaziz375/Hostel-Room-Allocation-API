"""Database layer: all SQL lives here. Every query uses ? placeholders (no SQL injection)."""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SELECT = "SELECT *, capacity - occupants AS available_beds FROM rooms"


def db_path() -> str:
    # read at call time so tests can point to a temporary database
    return os.getenv("DB_PATH") or os.path.join(BASE_DIR, "rooms.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with open(os.path.join(BASE_DIR, "schema.sql"), encoding="utf-8") as f:
        schema = f.read()
    with get_conn() as conn:
        conn.executescript(schema)


def create_room(r: dict) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO rooms (room_no, block, capacity, occupants, monthly_fee) VALUES (?, ?, ?, ?, ?)",
            (r["room_no"], r["block"], r["capacity"], r["occupants"], r["monthly_fee"]),
        )
        return cur.lastrowid


def list_rooms(only_available: bool = False) -> list:
    sql = SELECT + (" WHERE occupants < capacity" if only_available else "") + " ORDER BY id"
    with get_conn() as conn:
        return [dict(row) for row in conn.execute(sql)]


def get_room(room_id: int):
    with get_conn() as conn:
        row = conn.execute(SELECT + " WHERE id = ?", (room_id,)).fetchone()
    return dict(row) if row else None


def update_room(room_id: int, r: dict) -> bool:
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE rooms SET room_no=?, block=?, capacity=?, occupants=?, monthly_fee=? WHERE id=?",
            (r["room_no"], r["block"], r["capacity"], r["occupants"], r["monthly_fee"], room_id),
        )
        return cur.rowcount > 0


def delete_room(room_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
        return cur.rowcount > 0
