# ReusePass

**Reclaimed Material Compatibility Verifier**

ReusePass compares reclaimed timber batches with locked buyer requirements and records documented matches, conflicts, and missing evidence through a GenLayer Intelligent Contract.

A community workshop needs ten usable boards with specific minimum dimensions, untreated history and documented recovery provenance. A supplier offers recovered warehouse timber and an inspection report. ReusePass checks whether that report actually covers the offered batch, whether its claims meet the buyer's rules, and whether the precise dimensions and quantity work.

## Project links

- **Intelligent Contract:** [0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC](https://explorer-studio.genlayer.com/address/0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC)
- **Studio:** [Open the deployed contract](https://studio.genlayer.com/contracts?import-contract=0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC)
- **Network:** GenLayer Studionet, chain ID `61999`, RPC `https://studio.genlayer.com/api`
- **Design and trust model:** [Architecture](docs/ARCHITECTURE.md)
- **Reproducible checks:** [Testing](docs/TESTING.md)
- **Submission copy:** [Project Explorer details](docs/PROJECT_EXPLORER.md)
- **Machine-readable evidence:** [Live verification record](evidence/verification.json)

## What GenLayer does

GenLayer is central to the decision, not an optional text generator. Validators independently interpret document scope, treatment statements, exclusions, origin and custody, and whether inspection records actually confirm the batch manifest. They compare substantive decisions and document references. Deterministic code separately checks every dimension lot, eligible quantity, dates and tolerance boundaries.

| Result                 | Meaning                                                                                                               |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `DOCUMENTED_MATCH`     | All required documentary properties are supported and numerical checks pass. Eligible for further procurement review. |
| `REQUIREMENT_CONFLICT` | Offered dimensions/quantity fail or covered evidence explicitly contradicts a mandatory requirement.                  |
| `MORE_EVIDENCE_NEEDED` | Exact batch coverage or a required property is not documented. Unknown treatment history remains unknown.             |

A document content hash establishes which exact text was used. It does **not** authenticate the issuer or prove a physical property is true.

## Use the app

1. Create a requirement and lock minimum usable dimensions, quantity, permitted dimensional shortfall, earliest inspection date, treatment and provenance rules.
2. Register a batch with a unique version ID, the reference used in its documents, and one or more dimension lots.
3. Attach inspection/provenance text snapshots as the supplier account that registered that batch. Only that account can append evidence.
4. Select the requirement, open a batch, and prepare `assess_batch()`.
5. Open Studio, choose the method under Write Methods, and use each field’s copy button to paste its raw value into the matching named Studio input. Submit using **Normal (Full Consensus)** and Studio's built-in account.
6. Return to ReusePass, track the transaction hash, and refresh finalized records. Review numerical conflicts and exact supporting excerpts, read previous evidence revisions, or export the record as JSON.

Studio's account is on a separate origin and has no supported cross-site signing bridge. ReusePass deliberately uses an explicit Studio signing handoff, followed by direct contract reads and receipt tracking. No private key leaves Studio, no MetaMask installation is needed, and the app does not imply it can sign with Studio's account inside its own page.

### Demonstration

`seed_demo("your-unique-prefix")` atomically creates one requirement and three batches. Every demo label/document clearly states it is synthetic. No compatibility result is preloaded. Run assessments through Studio to create actual consensus-backed findings.

The featured `review-workshop` requirement and `review-a`, `review-b`, `review-c` batches demonstrate documented support, incompatible short boards, and incomplete treatment records. Consult the live verification record for the actually observed outcomes and transaction hashes.

### Public evidence adapter

Directly attached text remains labelled supplier-submitted. An optional public source must be an HTTPS raw GitHub URL pinned to a full commit. The frontend computes the SHA-256 of the exact supplied text. During assessment each validator fetches the source, checks HTTP success and exact digest, then interprets it. Changed/unavailable sources cannot yield a match.

For a real supplier, use records that supplier/inspector is authorized to publish. Private or sensitive inspection files should not be uploaded: contract data is public. Supporting arbitrary authenticated document repositories is future work.

## Run locally

Requires Node.js 22+ and Python 3.12+.

```sh
npm ci
npm test
npm run dev
```

`npm run build` creates the static production app in `dist/`. Network/address settings are in `src/config.js`. No signing secrets or environment keys are required. Build and unit checks also run in GitHub Actions.

For fresh on-chain verification, run:

```sh
node scripts/verify-chain.mjs
```

This reads the configured contract and existing receipts. It never deploys or submits transactions. It records check time, chain ID, source comparison, statuses, execution outcomes, validator votes and stored findings under `evidence/`. Allow time for public RPC responses/rate limits; do not poll repeatedly or treat missing data as proof of success.

## Contract interface

| Function                                                       | Purpose                                                                |
| -------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `create_requirement(requirement_id, requirement_json)`         | Lock a buyer requirement and content digest.                           |
| `register_batch(batch_id, batch_json)`                         | Register an immutable supplier manifest/version.                       |
| `attach_evidence(batch_id, evidence_json)`                     | Append a supplier-owned immutable text snapshot; increment revision.   |
| `assess_batch(requirement_id, batch_id)`                       | Independently reconcile documents and persist that revision's finding. |
| `get_requirement_findings(requirement_id, batch_id, revision)` | Read an exact historical finding.                                      |
| `get_requirement(requirement_id)`                              | Read the locked criteria.                                              |
| `get_batch(batch_id)`                                          | Read manifest, evidence and current revision.                          |
| `list_records()`                                               | Read registry IDs.                                                     |
| `seed_demo(prefix)`                                            | Create explicitly synthetic demonstration inputs.                      |

The standalone source is [contracts/reusepass.py](contracts/reusepass.py). Load this file in Studio; constructor takes no arguments. The pinned Python runner dependency is in its first line. Use the matching Studio network, verify finalized execution and read state before changing the frontend address. Do not redeploy unchanged code.

## Limitations

- Nonstructural workshop timber only. No structural grading, engineering suitability, safety certification, contamination testing or purchasing automation.
- Physical inspection and issuer authenticity checks remain separate. Supplier-created documents may be fraudulent even when internally consistent.
- Model errors and correlated validators remain possible. Exact quotations and independent assessment reduce risk without removing it.
- Minimum dimensions plus permitted shortfall are supported. This MVP does not implement arbitrary symmetric target intervals or automatically approve a subset of a mixed offer. Any below-minimum offered lot is a conflict.
- Requirements and manifests cannot be edited; evidence is append-only. Corrected records use a new version ID. Expired documents remain visible but are excluded from assessment.
- Studionet is a development network. External availability, resets, finality delays and model-provider limitations are outside the app's control.
- UI signing uses two pages. There is no embedded Studio account provider; the app cannot silently sign or automatically recover an unrecorded transaction hash.

## Continued development

A practical next stage is a pilot with a reclamation yard and community workshop: authenticated inspector identities, issuer-signed manifests, withdrawal/correction notices, private document access, independently measured condition reports and a supported signing bridge. Extend source adapters only with explicit provenance and versioning rules.

MIT licensed. See [LICENSE](LICENSE).
