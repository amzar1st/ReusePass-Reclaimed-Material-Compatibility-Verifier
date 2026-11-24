# ReusePass release verification

Verified 24 November 2026. The machine-readable chain snapshot was collected at **2026-11-24 02:53:46 UTC (08:23:46 Sri Lanka)**. All findings below were read from finalized contract state.

## Final contract

- Network: GenLayer Studionet, chain ID `61999`.
- Address: `0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC`.
- Source SHA-256: `85b4194ca5fad48a214f17bc0f04c97e191da2c7fd9403bfce7e673cdde63f3d`.
- The deployed source bytes matched `contracts/reusepass.py` exactly.
- All release writes below used Studio's built-in account `0xd410A16A05022918E5F8FBC0f4aCBA41AD86F00C`, execution mode `NORMAL` and a five-validator selection. The receipts record actual quorum votes, including idle validators; this is not a claim that every selected validator voted.

## Verified transactions

| Action | Finalized execution | Transaction |
| --- | --- | --- |
| Deploy corrected contract | FINISHED_WITH_RETURN | [dcad66e5](https://explorer-studio.genlayer.com/tx/0xdcad66e543b854f32c99de6d6720e5a13f1a0715d09fb53697956566ae1cc5e8) |
| Register demo requirement, three batches and initial evidence | FINISHED_WITH_RETURN | [05563517](https://explorer-studio.genlayer.com/tx/0x05563517f6b0a44ac0e7b7fa3c0d534cf77c741ab62978285568660be61e3ec5) |
| Assess documented batch | FINISHED_WITH_RETURN | [d4ee08dd](https://explorer-studio.genlayer.com/tx/0xd4ee08dde04692eb823b0293e76c1b72f1f3a61caa2d7c869c4a259717754e64) |
| Assess short-board batch | FINISHED_WITH_RETURN | [cc5bb6dd](https://explorer-studio.genlayer.com/tx/0xcc5bb6dda8281b202a4a341abf9c7cb0868e8af3829beddd540c779483f0341b) |
| Attach immutable public evidence for incomplete history | FINISHED_WITH_RETURN | [51be6fe3](https://explorer-studio.genlayer.com/tx/0x51be6fe37ef72f3c26aadb6caae04b7e061590a81aab01ed76a09dcb67c79251) |
| Assess public source and missing treatment | FINISHED_WITH_RETURN | [dc6e9356](https://explorer-studio.genlayer.com/tx/0xdc6e935682b91f0dbbbaa934f96f280c2054318a58e00f4814be4a039d9f74aa) |

| Batch | Requirement | Evidence revision | Stored outcome |
| --- | --- | --- | --- |
| `review-a` | `review-workshop` | 1 | DOCUMENTED_MATCH |
| `review-b` | `review-workshop` | 1 | REQUIREMENT_CONFLICT |
| `review-c` | `review-workshop` | 1 | MORE_EVIDENCE_NEEDED |

For `review-c`, coverage, manifest and provenance were supported while treatment remained MISSING. Its public source was fetched and its digest checked inside the assessment. The source is a clearly synthetic fixture pinned to commit `7635a68625b525eb80a077c9bbe970abb8bcbece`; it is not an authoritative real-world inspection.

## Checks completed

- 22 contract unit tests and 5 JavaScript lifecycle tests passed.
- Production build passed.
- Successful deployment, registry setup, supplier evidence attachment and all three outcome cases verified from chain receipts and state.
- Browser review passed for live finalized registry loading, status counts, filtering, search, batch details, exact supporting quotations, missing treatment display, evidence library, transaction list, requirement/batch/evidence call preparation, raw field clipboard copying, malformed JSON handling, invalid tolerance handling and public-source URL restrictions.
- Successful receipt rendering verified against an actual finalized assessment. A receipt from the superseded contract was correctly rejected as targeting a different contract.
- JSON export downloaded and parsed successfully; contract address and finding matched the displayed review.
- Historical revision lookup correctly displayed that no assessment existed for revision zero. An asynchronous dialog-close issue found during review was fixed and retested.
- Desktop screenshots captured in `evidence/dashboard.jpg` and `evidence/results.jpg`.

## Honest verification limits

- Browser review used desktop Chrome. Responsive CSS is implemented; no separate physical mobile-device test is claimed.
- Unit tests use a mocked host and do not substitute for live consensus. LLM/provider outage, validator disagreement and prolonged pending states are not guaranteed to be reproducible on demand. Lifecycle classification of error, pending and unverified receipts is covered by automated tests.
- A first-version assessment finalized with execution failure due to unstructured model text. Its compact receipt is retained in `evidence/assessment-first-attempt.json`; superseded deployment summaries are in `evidence/legacy/`. It is not presented as a successful release assessment. The corrected version requests structured JSON and all three final cases succeeded.
- A duplicate setup attempt produced no new observed transaction hash and is excluded from the release evidence. The release transaction list contains only observed hashes; no failed release hash is invented.
- Signing occurs in Studio through an explicit handoff. There is no embedded cross-origin Studio wallet connection.
- No real reclaimed material, inspector authenticity, procurement purchase or structural suitability was certified.
- Public website publication is recorded separately in `evidence/website-deployment.json` after the hosting service confirms its result.

## Official implementation references

- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/developers/intelligent-contracts/features/calling-llms
- https://docs.genlayer.com/developers/intelligent-contracts/deploying
- https://docs.genlayer.com/developers/intelligent-contracts/tools/genlayer-studio

## Public website and CI

- Public URL: https://reusepass.wirymink515.chatgpt.site/
- Hosting service confirmed successful publication on 24 November 2026, 03:01:49 UTC (08:31:49 Sri Lanka). Access is public.
- Published source commit: `744d223191f8fa951e795a859677bbdbe66fd1a4`. Subsequent documentation/evidence commits do not alter the deployed frontend or contract source.
- [GitHub Actions run 45316439291](https://github.com/amzar1st/ReusePass-Reclaimed-Material-Compatibility-Verifier/actions/runs/45316439291) completed successfully for that exact published source commit.
- Public-browser check loaded the hosted app without a sign-in wall and displayed all three finalized findings (one match, one conflict, one evidence gap). A separate unauthenticated HTTP request returned status 200.
