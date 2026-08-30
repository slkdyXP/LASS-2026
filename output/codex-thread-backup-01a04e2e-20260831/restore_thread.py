#!/usr/bin/env python3
"""Restore one Codex Desktop thread bundle without replacing other threads."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import sys


ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / "payload" / ".codex"
THREADS_JSON = ROOT / "metadata" / "threads.json"
EDGES_JSON = ROOT / "metadata" / "thread_spawn_edges.json"
PARENT_THREAD_ID = "01a04e2e-68b9-7043-b462-15f9a38273ab"


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def preserve_existing(path: Path, stamp: str) -> None:
    if not path.exists():
        return
    backup = path.with_name(f"{path.name}.pre-thread-restore-{stamp}")
    shutil.copy2(path, backup)
    print(f"Backed up existing file: {backup}")


def copy_session(src: Path, dst: Path, workspace: Path | None, stamp: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if workspace is None:
        if dst.exists() and digest(src) == digest(dst):
            print(f"Already present: {dst}")
            return
        preserve_existing(dst, stamp)
        shutil.copy2(src, dst)
        print(f"Restored: {dst}")
        return

    preserve_existing(dst, stamp)
    temp = dst.with_name(f".{dst.name}.restore-tmp")
    with src.open("rb") as source, temp.open("wb") as target:
        first = source.readline()
        try:
            event = json.loads(first)
            if event.get("type") == "session_meta":
                event.setdefault("payload", {})["cwd"] = str(workspace)
                first = (json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
        target.write(first)
        shutil.copyfileobj(source, target, length=1024 * 1024)
    os.replace(temp, dst)
    print(f"Restored with updated workspace: {dst}")


def copy_payload(codex_home: Path, workspace: Path | None, stamp: str) -> None:
    for src in sorted(path for path in PAYLOAD.rglob("*") if path.is_file()):
        rel = src.relative_to(PAYLOAD)
        dst = codex_home / rel
        if rel.parts and rel.parts[0] == "sessions" and src.suffix == ".jsonl":
            copy_session(src, dst, workspace, stamp)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and digest(src) == digest(dst):
            print(f"Already present: {dst}")
            continue
        preserve_existing(dst, stamp)
        shutil.copy2(src, dst)
        print(f"Restored: {dst}")


def backup_database(db_path: Path, stamp: str) -> Path:
    backup_path = db_path.with_name(f"state_5.sqlite.pre-thread-restore-{stamp}")
    with sqlite3.connect(db_path) as source, sqlite3.connect(backup_path) as target:
        source.backup(target)
    print(f"Backed up Codex thread database: {backup_path}")
    return backup_path


def table_columns(conn: sqlite3.Connection, table: str) -> set[str]:
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}


def restore_database(db_path: Path, codex_home: Path, workspace: Path | None) -> None:
    threads = json.loads(THREADS_JSON.read_text(encoding="utf-8"))
    edges = json.loads(EDGES_JSON.read_text(encoding="utf-8"))

    with sqlite3.connect(db_path) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if "threads" not in tables:
            raise RuntimeError("The target state_5.sqlite has no threads table. Launch Codex once, quit it, and retry.")
        allowed = table_columns(conn, "threads")

        for original in threads:
            item = dict(original)
            rollout_relpath = item.pop("rollout_relpath")
            item["rollout_path"] = str(codex_home / rollout_relpath)
            if workspace is not None:
                item["cwd"] = str(workspace)
            item = {key: value for key, value in item.items() if key in allowed}
            columns = list(item)
            placeholders = ",".join("?" for _ in columns)
            updates = ",".join(
                f'"{column}"=excluded."{column}"' for column in columns if column != "id"
            )
            quoted = ",".join(f'"{column}"' for column in columns)
            sql = (
                f"INSERT INTO threads ({quoted}) VALUES ({placeholders}) "
                f"ON CONFLICT(id) DO UPDATE SET {updates}"
            )
            conn.execute(sql, [item[column] for column in columns])

        if "thread_spawn_edges" in tables:
            for edge in edges:
                conn.execute(
                    """
                    INSERT INTO thread_spawn_edges(parent_thread_id, child_thread_id, status)
                    VALUES(?, ?, ?)
                    ON CONFLICT(child_thread_id) DO UPDATE SET
                      parent_thread_id=excluded.parent_thread_id,
                      status=excluded.status
                    """,
                    (edge["parent_thread_id"], edge["child_thread_id"], edge["status"]),
                )
        conn.commit()

        restored = conn.execute(
            "SELECT id, title, rollout_path, cwd FROM threads WHERE id=?", (PARENT_THREAD_ID,)
        ).fetchone()
        if restored is None:
            raise RuntimeError("Database verification failed: parent thread was not inserted.")
        if not Path(restored[2]).is_file():
            raise RuntimeError(f"Database points to a missing rollout: {restored[2]}")
        print(f"Registered thread: {restored[0]} - {restored[1]}")
        print(f"Workspace: {restored[3]}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge the bundled Codex thread into an existing Codex Desktop installation."
    )
    parser.add_argument(
        "--codex-home",
        default=str(Path.home() / ".codex"),
        help="Target Codex data directory (default: ~/.codex)",
    )
    parser.add_argument(
        "--workspace",
        help="Path to the LASS-2026 checkout on the target computer. If omitted, the original path is retained.",
    )
    args = parser.parse_args()

    codex_home = Path(args.codex_home).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve() if args.workspace else None
    db_path = codex_home / "state_5.sqlite"

    if not PAYLOAD.is_dir() or not THREADS_JSON.is_file():
        raise RuntimeError("The backup bundle is incomplete.")
    if not db_path.is_file():
        raise RuntimeError(
            f"Missing {db_path}. Install and launch Codex Desktop once, quit it completely, then retry."
        )
    if workspace is not None and not workspace.is_dir():
        raise RuntimeError(f"Workspace does not exist: {workspace}")

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    print("Codex Desktop should be fully closed before continuing.")
    backup_database(db_path, stamp)
    copy_payload(codex_home, workspace, stamp)
    restore_database(db_path, codex_home, workspace)
    print("\nRestore complete. Reopen Codex Desktop and look for the task title:")
    print("  这是最新的LASS要投稿的工作；熟悉我们在干什么")
    print(f"Fallback thread ID: {PARENT_THREAD_ID}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Restore failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
