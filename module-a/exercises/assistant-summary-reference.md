# Saved assistant reference — observed fixture

Provenance: authored by Codex during the Module A build on 19 October 2026 using the actual raw MLflow table in [observed-five-runs.csv](observed-five-runs.csv). This is a saved assistant-generated reference, not a claim of a learner's new external assistant request. The table is a published authoring fixture. Learners validate their own executed runs; it is not a substitute for their actual assistant request.

Prompt used: compare the five controlled runs using validation rmse_kwh, lower is better; name the recommended run ID, alpha and metric; check recorded controls; distinguish diagnostics and unsupported deployment claims.

## Assistant response

Recommend run `ebe7c1966d964a199f9fd9feebafc77e`, alpha `0.01`, validation RMSE `1.434281768493391` kWh. It has the lowest rmse_kwh among the five rows. The rows share data_sha256, code_revision, range_guard=True, validation partition and the declared scaler/solver. MAE is diagnostic; no training metric overrides validation RMSE. This supports a configuration choice under the fixture conditions. It does not prove real-world forecasting quality, valid serving inputs, active-version inference, completion time or clean-environment reproducibility. Those require separate tests.

## Instructor validation record

- Winner and metric: raw fields checked with `verify_summary`; recommendation_matches_metric is true in `planning/verification/recommendation-check.json`.
- Comparability: one source/data/guard/partition group; only alpha changes. Autolog enabled throughout.
- Promotion caution: alpha100 exceeds the helper's 5-kWh gate; a low RMSE alone is still not approval evidence.
- Unsupported-claim challenge: the sentence “therefore it is deployment-ready” would be unsupported; the reference deliberately makes no such recommendation.
- Rounding: display values are illustrative; validate against the raw value and full run ID.
