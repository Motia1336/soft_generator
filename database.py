"""
database.py - SQLite database layer for ProfileManager.
Updated to store the new profile format JSON-like fields since only one text output is fundamentally required.
We will store all raw JSON data as a single blob column for simplicity, 
while extracting searchable fields.
"""

import sqlite3
import json
import os
import sys
from pathlib import Path

# ── Path resolution (works both from .py and from PyInstaller .exe) ──
if getattr(sys, "frozen", False):
    _BASE_DIR = Path(sys.executable).parent
else:
    _BASE_DIR = Path(__file__).parent

DB_PATH    = _BASE_DIR / "profiles.db"
STATS_FILE = _BASE_DIR / "export_stats.json"


CREATE_SQL = """
CREATE TABLE IF NOT EXISTS profiles (
    id          TEXT PRIMARY KEY,
    platform    TEXT NOT NULL,
    model       TEXT NOT NULL,
    user_agent  TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    data        TEXT NOT NULL
);
"""

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db():
    with _connect() as conn:
        conn.executescript(CREATE_SQL)

# ─── Write ────────────────────────────────────

def insert_profile(profile: dict):
    sql = "INSERT OR REPLACE INTO profiles (id, platform, model, user_agent, created_at, data) VALUES (?, ?, ?, ?, ?, ?)"
    with _connect() as conn:
        conn.execute(sql, (
            profile["id"],
            profile["platform"],
            profile["model"],
            profile["user_agent"],
            profile["created_at"],
            json.dumps(profile)
        ))

def insert_profiles(profiles: list[dict]):
    sql = "INSERT OR REPLACE INTO profiles (id, platform, model, user_agent, created_at, data) VALUES (?, ?, ?, ?, ?, ?)"
    rows = [
        (p["id"], p["platform"], p["model"], p["user_agent"], p["created_at"], json.dumps(p)) 
        for p in profiles
    ]
    with _connect() as conn:
        conn.executemany(sql, rows)

# ─── Read ─────────────────────────────────────

def count_profiles(platform: str = "all", search: str = "") -> int:
    sql = "SELECT COUNT(*) FROM profiles WHERE 1=1"
    params = []
    if platform != "all":
        sql += " AND platform = ?"
        params.append(platform)
    if search:
        sql += " AND (model LIKE ? OR user_agent LIKE ?)"
        params += [f"%{search}%"] * 2
    with _connect() as conn:
        return conn.execute(sql, params).fetchone()[0]

def get_profiles(
    platform: str = "all",
    search: str = "",
    limit: int = 100,
    offset: int = 0,
    order_by: str = "created_at DESC",
) -> list[dict]:
    sql = f"SELECT data FROM profiles WHERE 1=1"
    params = []
    if platform != "all":
        sql += " AND platform = ?"
        params.append(platform)
    if search:
        sql += " AND (model LIKE ? OR user_agent LIKE ?)"
        params += [f"%{search}%"] * 2
    sql += f" ORDER BY {order_by} LIMIT ? OFFSET ?"
    params += [limit, offset]
    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [json.loads(r["data"]) for r in rows]

def get_profile_by_id(profile_id: str) -> dict | None:
    with _connect() as conn:
        row = conn.execute("SELECT data FROM profiles WHERE id = ?", (profile_id,)).fetchone()
        return json.loads(row["data"]) if row else None

# ─── Random Fetch ─────────────────────────────
def get_random_profiles(count: int) -> list[dict]:
    """Fetch random profiles from DB for generation"""
    sql = f"SELECT data FROM profiles ORDER BY RANDOM() LIMIT ?"
    with _connect() as conn:
        rows = conn.execute(sql, (count,)).fetchall()
        return [json.loads(r["data"]) for r in rows]

def get_all_profiles(platform: str = "all") -> list[dict]:
    """Fetch ALL profiles from DB, optionally filtered by platform. Used for full export."""
    sql = "SELECT data FROM profiles WHERE 1=1"
    params = []
    if platform != "all":
        sql += " AND platform = ?"
        params.append(platform)
    sql += " ORDER BY created_at ASC"
    with _connect() as conn:
        rows = conn.execute(sql, params).fetchall()
        return [json.loads(r["data"]) for r in rows]

# ─── Delete ───────────────────────────────────

def delete_profiles(ids: list[str]):
    with _connect() as conn:
        conn.executemany("DELETE FROM profiles WHERE id = ?", [(i,) for i in ids])

def delete_all():
    with _connect() as conn:
        conn.execute("DELETE FROM profiles")

# ─── Stats ────────────────────────────────────

def get_stats() -> dict:
    with _connect() as conn:
        total   = conn.execute("SELECT COUNT(*) FROM profiles").fetchone()[0]
        android = conn.execute("SELECT COUNT(*) FROM profiles WHERE platform='Android'").fetchone()[0]
        ios     = conn.execute("SELECT COUNT(*) FROM profiles WHERE platform='iOS'").fetchone()[0]
        
        rows = conn.execute(
            "SELECT model, COUNT(*) as cnt FROM profiles GROUP BY model ORDER BY cnt DESC LIMIT 5"
        ).fetchall()
        top_models = [(r["model"], r["cnt"]) for r in rows]
    return {
        "total": total,
        "android": android,
        "ios": ios,
        "top_models": top_models,
    }

# ─── Cumulative Stats (persist across sessions) ───────────────────────

def _load_cumulative() -> dict:
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "total_generated": 0,
            "total_exported": 0,
            "android_generated": 0,
            "ios_generated": 0,
            "android_exported": 0,
            "ios_exported": 0,
            "export_sessions": [],
        }

def _save_cumulative(data: dict):
    try:
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_cumulative_stats() -> dict:
    return _load_cumulative()

def record_generation(profiles: list):
    """Call after inserting generated profiles — adds to cumulative counters."""
    data = _load_cumulative()
    data["total_generated"] += len(profiles)
    for p in profiles:
        if p.get("platform") == "Android":
            data["android_generated"] += 1
        else:
            data["ios_generated"] += 1
    _save_cumulative(data)

def record_export(profiles: list):
    """Call after exporting profiles — adds to cumulative counters and session log."""
    from datetime import datetime
    data = _load_cumulative()
    count = len(profiles)
    data["total_exported"] += count
    android_cnt = sum(1 for p in profiles if p.get("platform") == "Android")
    ios_cnt = count - android_cnt
    data["android_exported"] += android_cnt
    data["ios_exported"] += ios_cnt
    data["export_sessions"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": count,
        "android": android_cnt,
        "ios": ios_cnt,
    })
    _save_cumulative(data)
