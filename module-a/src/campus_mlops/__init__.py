"""Public Module A API. Reusable behavior lives here, not in notebooks."""
__version__ = "0.1.1"
from .pipeline import Config, ingest, preprocess, train, evaluate, validate_ranges, run_pipeline
from .lifecycle import Workspace, register, approve, activate, batch_predict, reproduce, run_matrix, export_runs, verify_summary
