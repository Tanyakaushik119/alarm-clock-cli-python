import argparse
import json
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


# ============================================================
# Domain
# ============================================================

@dataclass
class Alarm:
    id: str
    trigger_time: str  # ISO format datetime
    message: str
    enabled: bool = True

    @property
    def trigger_datetime(self) -> datetime:
        return datetime.fromisoformat(self.trigger_time)
    
    # ============================================================
# Persistence
# ============================================================

class JsonAlarmStore:
    def __init__(self, file_path: str = "alarms.json"):
        self.file_path = Path(file_path)

    def load(self) -> list[Alarm]:
        if not self.file_path.exists():
            return []

        with open(self.file_path, "r") as f:
            data = json.load(f)

        return [Alarm(**item) for item in data]

    def save(self, alarms: list[Alarm]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(
                [asdict(alarm) for alarm in alarms],
                f,
                indent=2
            )
