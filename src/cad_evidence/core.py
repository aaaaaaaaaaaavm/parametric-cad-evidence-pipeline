"""Content-addressed evidence for files produced by a parametric CAD build."""
from __future__ import annotations
from hashlib import sha256
import json
from pathlib import Path


def _digest(path: Path) -> str:
    h=sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def build_manifest(root: str|Path, sources: list[str], artifacts: list[str], parameters: dict) -> dict:
    root=Path(root).resolve()
    def records(paths: list[str]) -> list[dict]:
        rows=[]
        for relative in sorted(paths):
            path=(root/relative).resolve()
            if root not in path.parents or not path.is_file():
                raise ValueError(f"missing or out-of-root path: {relative}")
            rows.append({"path":relative,"bytes":path.stat().st_size,"sha256":_digest(path)})
        return rows
    canonical=json.dumps(parameters,sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    return {"schema":"cad-evidence/v1","parameter_sha256":sha256(canonical).hexdigest(),"parameters":parameters,"sources":records(sources),"artifacts":records(artifacts)}


def verify_manifest(root: str|Path, manifest: dict) -> list[str]:
    root=Path(root).resolve()
    failures=[]
    if manifest.get("schema") != "cad-evidence/v1":
        failures.append("invalid schema")
    try:
        canonical=json.dumps(manifest["parameters"],sort_keys=True,separators=(",",":"),allow_nan=False).encode()
        if sha256(canonical).hexdigest()!=manifest["parameter_sha256"]:
            failures.append("changed: parameters")
    except (KeyError, TypeError, ValueError):
        failures.append("invalid parameters")
    for section in ("sources","artifacts"):
        if section not in manifest or not isinstance(manifest[section], list):
            failures.append(f"missing or invalid section: {section}")
            continue
        for record in manifest.get(section,[]):
            path=(root/record["path"]).resolve()
            if root not in path.parents:
                failures.append(f"out-of-root path: {record['path']}")
            elif not path.is_file(): failures.append(f"missing: {record['path']}")
            elif _digest(path)!=record["sha256"]: failures.append(f"changed: {record['path']}")
            elif path.stat().st_size!=record.get("bytes"):
                failures.append(f"changed byte count: {record['path']}")
    return failures
