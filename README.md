# ZERO_NAZ

**Sourced moderation lexicons for public forums. First collection: white nationalism and neo-Nazism, English and German.**

A SecLists-style starting collection for moderator review queues, research, and filter development. Contains explicit slogans, names, organizations, publications, coded numbers, acronyms, antisemitic dogwhistles, and symbol references. See the [browsable catalog](CATALOG.md), [structured entries](data/entries.json), and [source registry](data/sources.json).

This is an initial researched release, not a complete or independently reviewed dictionary. A match identifies a term to inspect; it does not establish extremist intent, a person's ideology, or a policy violation. Numeric codes, names, runes, historical discussion, counterspeech, and reclaimed symbols are especially ambiguous. Every entry recommends human review.

## Files

| Path | Use |
| --- | --- |
| `data/entries.json` | Canonical entries, aliases, context notes, dates, provenance |
| `data/sources.json` | Publishers, exact URLs, evidence-access limitations |
| `data/entries.csv` | Spreadsheet-friendly export; array cells contain JSON |
| `lists/strong_signal.txt` | More distinctive literal terms; still review-only |
| `lists/ambiguous.txt` | Opt-in numbers, names, and context-dependent terms |
| `lists/en.txt`, `lists/de.txt` | Language-relevant literal terms across both tiers |
| `zero_naz.py` | Dependency-free Python reference matcher |
| `docs/MODERATION.md` | Interpretation, normalization, and limitations |

Language tags indicate relevant moderation languages, not that every alias is a translation. Symbol names and Unicode approximations are text references, not image detectors. `(((echo)))` is handled structurally by the matcher and excluded from literal exports. Visual-only gestures are excluded from text matching. Ordinary emoji are not assigned extremist meaning without evidence for a specific usage.

## Quick start

Requires Python 3.10 or later, with no third-party dependencies.

```sh
python zero_naz.py "text to review"
python zero_naz.py --include-ambiguous "text containing numbers or symbol references"
python tools/build.py
python -m unittest discover -s tests -v
```

The default matcher uses only `strong_signal` entries. `--include-ambiguous` enables all text-compatible entries and can generate substantial noise. JSON output contains entry IDs and source IDs for auditability. No hit means only that this small literal matcher found nothing; it does not establish that content is safe.

## Evidence and scope

Entries cite ADL, AJC, German state extremism information services, the United States Holocaust Memorial Museum, and the Unwort des Jahres jury. Definitions are short project-authored summaries; source material remains owned by its publishers. Some pages were available only as search-index excerpts, including AJC pages that returned HTTP 403 when fetched directly. Those limits are recorded in `evidence_access`; a date records research activity, not a guarantee of current availability or independent validation.

Independent source corroboration and bilingual moderator review remain priorities. Antisemitic language overlaps this collection but is not exclusive to neo-Nazism. Inclusion describes a documented association, never exclusive ownership. Threats require assessment of the surrounding message.

Do not treat the TXT files as automatic ban lists. Generic identity words, religious terms, political criticism, common German words, arbitrary emoji combinations, and unsupported speculative codes are not automatically included.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Edit JSON, regenerate exports, and run checks. Stable IDs let consumers track changes. Source dates and context notes must be maintained as terminology changes.

Project code: MIT. Original dataset structure and project-authored annotations: CC0-1.0, to the extent the contributor can waive rights. Referenced websites, images, trademarks, and external text retain their own rights. See [LICENSE](LICENSE) and [data/LICENSE](data/LICENSE).

## Canadian audit and spreadsheet exports

See [Canadian coverage](docs/CANADA.md), [Canadian LTE catalog](CANADA_LTE_CATALOG.md), [audit findings](docs/AUDIT.md), and [Excel usage](docs/EXCEL.md). Read [plain-text terms](lists/terms_readable.txt), import [Excel TSV](lists/terms_excel.tsv), or use [Boolean OR](lists/terms_or.txt) / [pipe-separated](lists/terms_pipe.txt) exports. Context is required for every flag.
