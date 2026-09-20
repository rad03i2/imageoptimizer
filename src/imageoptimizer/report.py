from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class ProcessResult:
    source: str
    output: str
    input_bytes: int
    output_bytes: int
    input_format: str
    output_format: str
    width: int
    height: int

    @property
    def saved_bytes(self) -> int:
        return self.input_bytes - self.output_bytes

    @property
    def savings_percent(self) -> float:
        if self.input_bytes == 0:
            return 0.0
        return round((self.saved_bytes / self.input_bytes) * 100, 2)

    def to_dict(self) -> dict:
        data = asdict(self)
        data["saved_bytes"] = self.saved_bytes
        data["savings_percent"] = self.savings_percent
        return data


def write_report(path: Path, results: list[ProcessResult]) -> None:
    payload = {
        "files": [item.to_dict() for item in results],
        "summary": {
            "processed": len(results),
            "input_bytes": sum(item.input_bytes for item in results),
            "output_bytes": sum(item.output_bytes for item in results),
            "saved_bytes": sum(item.saved_bytes for item in results),
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
