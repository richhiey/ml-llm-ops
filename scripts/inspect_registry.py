"""Read the live alias, model versions and recorded local lifecycle events."""

import argparse
import json
from pathlib import Path
from catalog_mlops.registry import audit_status, model_name, registry_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=Path("work/mlflow"))
    parser.add_argument("--name", required=True)
    parser.add_argument("--alias", default="active")
    args = parser.parse_args()
    client = registry_client(args.state)
    name = model_name(args.name)
    report = audit_status(args.state, name, args.alias)
    report["versions"] = [
        dict(version=str(v.version), run_id=v.run_id, source=v.source, tags=v.tags)
        for v in client.search_model_versions(f"name = '{name}'")
    ]
    print(json.dumps(report, indent=2))
