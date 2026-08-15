#!/usr/bin/env python3
"""Back up the platform PostgreSQL database via kubectl exec + pg_dump."""

import subprocess
import sys
from datetime import datetime
from pathlib import Path

NAMESPACE = "data"
POD = "postgres-0"
DB_USER = "platform_app"
DB_NAME = "platform"
BACKUP_DIR = Path("backups")


def run_backup() -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = BACKUP_DIR / f"platform-{timestamp}.sql"

    command = [
        "kubectl", "exec", POD, "-n", NAMESPACE, "--",
        "pg_dump", "-U", DB_USER, "-d", DB_NAME,
    ]

    with open(output_file, "wb") as f:
        result = subprocess.run(command, stdout=f, stderr=subprocess.PIPE)

    if result.returncode != 0:
        output_file.unlink(missing_ok=True)
        print(f"Backup failed: {result.stderr.decode()}", file=sys.stderr)
        sys.exit(1)

    print(f"Backup written to {output_file}")
    return output_file


if __name__ == "__main__":
    run_backup()
