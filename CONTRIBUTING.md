# Contributing

Edit `data/entries.json` and `data/sources.json`; Canonical JSON is the maintained source.

Each entry needs a stable unique ID, term, explicit aliases, category, relevant languages, concise original meaning, exact source IDs, a context note, evidence date, and human-review action. Use an exact research or glossary page when possible. A general organization homepage does not establish a term's meaning. Document whether evidence came from full page text or only an indexed excerpt. Add independent corroboration where possible; speculative emoji combinations and unsourced labels are insufficient.

Separate source-attested variants from project normalization choices in context notes. Names and shared cultural symbols belong in the ambiguous tier. Never infer the ideology of a person from their name. Avoid copying substantial source passages, propaganda, manifestos, or images.

Run `python tools/build.py` and `python -m unittest discover -s tests -v`; commit generated exports with canonical data. Include meaningful matching and false-positive cases when changing matcher behavior. Explain additions, removals, and source limitations in the pull request and changelog.
