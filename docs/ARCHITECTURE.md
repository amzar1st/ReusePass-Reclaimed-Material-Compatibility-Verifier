# ReusePass architecture

ReusePass records evidence-backed compatibility findings for reclaimed timber intended for nonstructural workshop use. Its trust problem is the gap between an attractive material listing and documents that actually cover that particular batch.

## Contract and evidence model

`requirements`, `batches` and `assessments` are GenLayer persistent `TreeMap[str, str]` collections containing canonical JSON. Registry IDs use a restricted alphabet. Up to 500 requirements and 500 batches are supported in this bounded MVP; each batch contains at most 20 dimension lots and 8 evidence snapshots.

A requirement records minimum usable dimensions, whole board quantity, allowed dimensional shortfall, an earliest acceptable inspection date, acceptable treatment history, and provenance criteria. Registration locks it permanently. Updating requirements means creating a new ID.

A batch manifest records supplier ownership, the document-visible batch reference, description and individual dimension lots. It is immutable. Only its original supplier account can append evidence. Each append increments the evidence revision. An assessment key contains requirement ID, batch ID, and revision, so evidence changes cannot silently overwrite previous findings. Assessment of an unchanged revision is rejected.

Requirement and manifest digests include their original owner. Evidence contains a SHA-256 digest of exact UTF-8 text. A content digest establishes integrity, not issuer authenticity. Evidence cannot be deleted or corrected in place; superseding records require a new batch version where necessary.

## Meaningful GenLayer consensus

For each assessment with eligible evidence, the leader and validators independently run the same interpretation task. The task returns four fields:

| Field        | Substantive question                                                                                       |
| ------------ | ---------------------------------------------------------------------------------------------------------- |
| `coverage`   | Does the document explicitly cover the offered batch reference?                                            |
| `treatment`  | Does explicit treatment history satisfy or contradict the buyer's rule?                                    |
| `provenance` | Does documented origin and custody support the provenance rule?                                            |
| `manifest`   | Does the document confirm all lot dimensions and quantities, and match its submitted issuer/date metadata? |

Each finding contains `SUPPORTED`, `CONFLICT`, or `MISSING`, a document index, and a verbatim excerpt. Missing findings must have no document and no quotation. Substantive findings must cite a real eligible document and a continuous quotation present in that document.

The validator independently re-executes the extraction, validates quotations, and compares all four decision states and document indices with the proposed answer. This checks meaning, not only JSON shape. Wording of excerpts may differ. A disagreement cannot store a successful assessment. The contract uses the official structured JSON response mode, rather than assuming plain model text can be parsed as JSON.

All untrusted text is identified as evidence, never instructions. Exact quote checks, batch coverage gating, independent interpretation and deterministic checks reduce prompt-injection risk. They do not eliminate the risk of correlated model mistakes or fraudulent source documents.

## Deterministic rules

All measurements are positive integer millimetres. Quantities are positive whole boards; booleans and floating point values are rejected. Tolerance is a nonnegative integer smaller than every minimum dimension. It represents permitted shortfall below a minimum, not a symmetric target range. Oversized pieces are allowed because they can be cut.

Every offered lot is checked; any offered dimension below the allowed minimum is a conflict. Only lots meeting all minimum dimensions count toward quantity. A shortage is a conflict. This MVP evaluates the full offered batch and does not silently approve a subset of a mixed offer.

Evidence with submitted inspection date before the locked cutoff is excluded. The model must also reconcile inspection date and issuer metadata with the document itself. Calendar dates are validated. The contract does not invent the current date or silently alter a locked cutoff.

Status precedence:

1. A numerical conflict produces `REQUIREMENT_CONFLICT`.
2. Without supported exact batch coverage, the result is `MORE_EVIDENCE_NEEDED`.
3. With coverage, an explicit treatment, provenance or manifest conflict produces `REQUIREMENT_CONFLICT`.
4. Any remaining missing semantic evidence produces `MORE_EVIDENCE_NEEDED`.
5. Only complete semantic support and passing numerical checks produce `DOCUMENTED_MATCH`.

## Public source retrieval

A supplier can attach a submitted text snapshot directly. This is labelled supplier-submitted evidence, not a verified public source. Alternatively, the supplier may give an HTTPS raw GitHub URL pinned to a full 40-character commit and the SHA-256 of the exact snapshot. During assessment, each participating validator fetches that URL and checks HTTP success and the content digest before interpreting it. Unavailable or changed content prevents an assessment; it cannot create a match. Arbitrary URLs and private-network fetch targets are not accepted.

This narrow source adapter makes the MVP reproducible. A public GitHub fixture is not authoritative proof about real timber. Real adoption needs authenticated inspection/provenance issuers and permission to publish their records. No fictional demo record is presented as a real inspection.

## Frontend integration and signing

The Vite frontend uses the official `genlayer-js` client for finalized contract reads and JSON-RPC for transaction receipts and transaction listings. It checks chain ID before loading records. It has no backend signer, embedded private key, wallet-key import or MetaMask dependency.

Studio holds its built-in account on the Studio origin. Studio currently exposes contract-import links but no supported cross-origin signing bridge. ReusePass therefore prepares exact named JSON arguments, opens the deployed contract in Studio, and instructs the user to select the method and submit with Normal (Full Consensus). The frontend then tracks the returned transaction hash, automatically rechecking a pending receipt every 12 seconds while its dialog is open. It distinguishes acceptance, finality and execution success. Saved hashes survive browser reloads. It never automatically resubmits a write.

This is an explicit two-page signing workflow. ReusePass does not claim a one-click embedded Studio wallet connection. A future supported signing bridge can replace this handoff without changing the compatibility contract.

## Boundaries

The app checks documented compatibility, not physical condition, engineering suitability, structural grading, legal compliance, absence of contamination, or authenticity of a claimed issuer. Physical inspection remains a separate procurement step. It holds no funds and executes no procurement payment. Studionet is a development environment whose availability and state retention are controlled by GenLayer.
