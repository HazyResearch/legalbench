# citation_verification

### Given a legal citation and a quoted passage, classify whether the quote matches the cited provision, a different provision, or no real provision at all.

---

**Contributor**: Stephen Murphy (LawEngine)

**License**: CC BY 4.0

**Size (samples)**: 500

**Legal reasoning type**: Rule-recall

**Task type**: 4-way classification

## Task description

This task evaluates whether a system can verify quoted primary-law language
against a cited legal provision. Each example contains a citation and a quoted
passage attributed to that citation. The system must assign exactly one of four
labels: `VERIFIED`, `NOT_FOUND`, `MISATTRIBUTED`, or `CITATION_UNRESOLVED`.

`VERIFIED` means the citation resolves to a real provision and the quoted text
matches that provision under strict quote-matching rules, including ordered
gapped matches with legal ellipsis. `NOT_FOUND` means the citation resolves to
a real provision but the quoted text does not match that provision under the
same rules, including altered, fabricated, or paraphrased text.
`MISATTRIBUTED` means the quoted text matches a different provision, not the
cited one. `CITATION_UNRESOLVED` means the citation is malformed or does not
resolve to a real provision in the benchmark corpus.

The task distinguishes several legal error types that a single binary score
would collapse together: correct support, fabricated or altered support,
wrong-provision support, and unresolved citation structure.

The dataset mixes Illinois and federal primary-law authorities, including
statutes, rules, and constitutional provisions. Negative examples are
structured rather than random: altered quoted language under a real citation,
real quoted language attached to the wrong nearby provision, and malformed or
nonexistent citations.

This is a labeled split derived from the cite-bench benchmark family. The LegalBench
version is for labeled local evaluation; the public cite-bench benchmark is the blind
benchmark surface with remote scoring.

## Files

- `train.tsv`: samples for use as in-context demonstrations
- `test.tsv`: the evaluation set
- `base_prompt.txt`: an example prompt template for this task

## Data column names

- `citation`: the cited legal provision
- `quote`: the quoted passage attributed to that citation
- `answer`: the correct label (`VERIFIED`, `NOT_FOUND`, `MISATTRIBUTED`, `CITATION_UNRESOLVED`)

## Citation

```bibtex
@misc{murphy2026citebench,
  title  = {cite-bench: A Blind Benchmark for Legal Citation Verification},
  author = {Stephen Murphy},
  year   = {2026},
  url    = {https://github.com/LawEngine/cite-bench}
}
```

## Additional resources

- Remote scoring and blind public benchmark: https://www.lawengine.ai/cite-bench
- Source repository: https://github.com/LawEngine/cite-bench
