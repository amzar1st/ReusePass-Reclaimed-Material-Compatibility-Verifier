# Verification and testing

## Automated local checks

Run `npm ci`, `npm test`, and `npm run build`.

- Python tests import the actual contract and run its methods against an explicitly mocked in-memory GenLayer host. They cover immutable registration, supplier ownership, missing/expired evidence, conflicting treatment, unrelated batch scope, forged quotations, independent validator disagreement, revision history, duplicate assessments/documents, dimension/tolerance boundaries, mixed-lot quantity, invalid numeric types and dates, and public source URL/digest validation.
- JavaScript tests exercise transaction lifecycle behavior using observed Studio status/execution names. Finality alone is insufficient: `FINISHED_WITH_RETURN` must be present for success. Failed execution remains failed even when the receipt is finalized. Missing results remain unverified.
- Production build validates frontend imports and static asset generation.

These unit tests do not emulate GenVM storage serialization, actual LLM judgment or network consensus. Actual on-chain results are recorded separately under `evidence/`.

## On-chain verification

Deployment and write transactions use Studio's built-in account and **Normal (Full Consensus)**. The check script records finalized execution results and contract state independently of the Studio interface. It compares deployed source bytes from the deployment receipt with `contracts/reusepass.py`.

The first deployment's assessment failed because plain model output was not valid JSON. That receipt is retained as `assessment-first-attempt.json`, and the original deployment is not presented as the final app. The corrected contract requests structured JSON directly from the official SDK. Only changed source was redeployed.

`verification.json` is a timestamped observation, not a promise about perpetual test-network availability. Receipt files retain relevant public RPC status, execution, votes, equivalence outputs and error fields; large redundant code/configuration blobs are omitted. Verify hashes with the configured RPC or explorer. Do not infer execution success merely from an explorer's FINALIZED badge.

## Browser review

The browser review checks the live registry, filtering/search, requirement detail, batch findings/evidence, historical revisions, form validation/preparation, Studio handoff, receipt tracker success/failure rendering and JSON export. See the final release checklist for actual checks completed and any limitations.

Desktop visual review and responsive CSS are separate from device coverage. Do not claim mobile-browser execution unless a mobile viewport was actually inspected. No real-world material or inspection authenticity is established by these tests.
