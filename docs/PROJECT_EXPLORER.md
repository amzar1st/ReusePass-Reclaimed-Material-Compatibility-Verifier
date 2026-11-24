# Project Explorer submission

## Identity

**Project name:** ReusePass

**Short description:** GenLayer-powered verification of reclaimed timber compatibility using batch-specific evidence, immutable document versions and precise dimension checks.

**Category suggestion:** Sustainability / supply chain / procurement, using the closest tags available in the submission form.

**Logo:** `public/reusepass-logo.png` (512 × 512 PNG); vector original at `public/logo.svg`.

## Project summary

ReusePass helps workshops and community buyers evaluate reclaimed timber without treating vague supplier descriptions as proof. Buyers lock minimum dimensions, quantity, allowed shortfall, treatment-history requirements and provenance criteria. Suppliers register batches and attach exact document snapshots. GenLayer validators independently determine whether those documents cover the offered material and substantiate the required properties. Deterministic code checks numerical limits and eligible quantities. Each stored result identifies the exact requirement, batch manifest and evidence revision.

The result is DOCUMENTED_MATCH, REQUIREMENT_CONFLICT or MORE_EVIDENCE_NEEDED. A documented match supports further procurement review; it does not certify physical condition, structural safety or document authenticity.

## The trust problem

Reclaimed material is often advertised with inconsistent dimensions, vague treatment descriptions or inspection records covering different batches. A buyer needs an auditable explanation of which mandatory criteria are supported, contradicted or undocumented. ReusePass preserves missing evidence as missing and prevents later document changes from silently rewriting earlier findings.

## Why GenLayer is essential

Meaning depends on context: a certificate can exclude some boards, a treatment statement can be ambiguous, or a recovery manifest can apply to a different batch. A keyword checker cannot reliably determine those relationships. GenLayer validators independently interpret the same evidence and must agree on coverage, treatment, provenance and manifest support plus cited document indices. Exact-quote validation and deterministic numerical checks constrain the accepted result. A format-only check cannot authorize an assessment.

## What is implemented

- Standalone Intelligent Contract with locked requirements/manifests, supplier-only evidence attachment and revision-specific findings.
- Responsive material workspace with live finalized contract reads, batch filters/search, evidence inspection, history and JSON export.
- Explicit signing with GenLayer Studio's built-in account; no MetaMask or frontend private keys.
- Named-argument preparation, Studio contract handoff, hash tracking, pending polling and explicit finalized execution checks.
- Optional immutable public evidence retrieval with HTTP and SHA-256 verification during validator execution.
- Three clearly labelled synthetic demonstration batches covering documented support, incompatible dimensions and missing treatment history.
- Unit checks, production build, verification script and published audit evidence.

## Contract and network

**Network:** GenLayer Studionet, chain ID 61999.

**Contract:** `0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC`

**Explorer:** https://explorer-studio.genlayer.com/address/0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC

**Studio:** https://studio.genlayer.com/contracts?import-contract=0xeda7e44331EB2dF78ABC320656752FE4f05DC4EC

**GitHub:** https://github.com/amzar1st/ReusePass-Reclaimed-Material-Compatibility-Verifier

Current observed transaction evidence and actual outcome labels are in `evidence/verification.json`. Publication details and release checks are in `docs/RELEASE.md`.

## Reviewer walkthrough

1. Open the public website and select the synthetic workshop requirement.
2. Review the warehouse-board batch: read exact cited evidence and manifest traceability.
3. Review the short-board batch: inspect its numerical conflicts and quantity findings.
4. Review the incomplete-history batch: confirm unavailable treatment history does not become a documented match.
5. Open Transactions and inspect finalized success plus execution outcome. The original failed assessment is retained separately as honest development evidence.
6. Create a unique new requirement or batch in the UI, prepare named field values and submit in Studio with Full Consensus. Track the returned hash in ReusePass and refresh finalized state.

## Scope and future work

This MVP covers nonstructural workshop timber and public documents. Fictional fixtures demonstrate the decision process, not adoption by a real supplier. Next steps are a pilot with a reclamation yard, authenticated inspector identities, issuer-signed manifests, correction/withdrawal notices, additional versioned document sources and a supported cross-site signing bridge. Physical inspection remains a separate step.
