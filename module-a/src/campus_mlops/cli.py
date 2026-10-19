import argparse
import json
from . import Config, Workspace, register, approve, activate, batch_predict, run_matrix, export_runs, reproduce

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["train", "matrix", "bootstrap", "handoff", "reproduce", "ui"])
    parser.add_argument("--state", default="state")
    parser.add_argument("--alpha", type=float, default=1.0)
    parser.add_argument("--range-guard", action="store_true")
    parser.add_argument("--autolog", action="store_true")
    parser.add_argument("--partition", choices=["validation", "final"], default="validation")
    parser.add_argument("--run-id")
    parser.add_argument("--destination", default="state-reproduced")
    args = parser.parse_args()
    ws = Workspace(args.state)
    if args.command == "ui":
        import subprocess
        subprocess.run(["mlflow", "server", "--backend-store-uri", ws.uri, "--host", "127.0.0.1", "--port", "5050"], check=True)
        return
    if args.command == "reproduce":
        if not args.run_id:
            parser.error("--run-id is required")
        result = reproduce(ws, args.run_id, args.destination)
    elif args.command == "matrix":
        result = run_matrix(ws, range_guard=True, autolog=args.autolog)
        selected_ids = [record["run_id"] for record in result]
        (ws.path / "matrix-run-ids.json").write_text(json.dumps(selected_ids, indent=2) + "\n")
        rows = export_runs(ws)
        rows[rows.run_id.isin(selected_ids)].to_csv(ws.path / "runs.csv", index=False)
    else:
        config = Config(args.alpha, args.range_guard or args.command in {"bootstrap", "handoff"}, args.autolog)
        result = ws.run(config, partition=args.partition)
        if args.command in {"bootstrap", "handoff"}:
            version = register(ws, result["run_id"])
            approve(ws, version, "Range contract tests and RMSE <= 5; local teaching acceptance")
            event = activate(ws, version, "Initial baseline" if args.command == "bootstrap" else "Validated handoff")
            _, inference = batch_predict(ws)
            result = {"training": result, "version": version, "audit": event, "inference": inference}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
