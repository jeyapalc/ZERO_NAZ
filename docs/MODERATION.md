# Moderation integration

1. Select applicable categories and languages for your forum. Begin with the stronger-signal tier.
2. Keep the original message alongside any normalized representation. The reference matcher performs NFKC, case folding, removal of Unicode format characters, and whitespace collapse. These transforms may change legitimate writing and do not preserve offsets.
3. Queue candidates with entry ID, source, surrounding discussion, and moderator rationale. Review quotation, education, reporting, satire, counterspeech, reclamation, and targeted abuse.
4. Apply your published rules after review. Provide correction and appeal paths. Evaluate false positives and missed abuse on representative English and German samples.

`strong_signal` describes lexical distinctiveness, not certainty about a user's intent. `ambiguous` includes standalone numeric codes, initials, personal names, historical terms, and cultural symbols. Review dates mark the initial research pass; no entries are claimed to have independent expert approval.

## Matcher boundaries

Literal matches require boundaries against adjacent Unicode letters and digits. Underscores count as separators, allowing handles such as `user_1488` in opt-in mode. Numbers embedded directly in alphanumeric handles are not detected. Known aliases are explicit. The matcher does not expand every punctuation variant, transliterate all scripts, map arbitrary confusables, perform OCR, or infer intent. Format-character removal is a project implementation choice, not a sourced extremist spelling variant.

Unicode runes do not capture stylistic differences in historical and extremist insignia. A generic skull, sun, cross, lightning bolt, frog, or okay emoji cannot establish that a Nazi symbol is present. Image-only symbols require a separate visual review process. A source on a hand gesture does not automatically establish the same meaning for its emoji.

Do not sum overlapping aliases or related entries into an assumed probability of extremism. For example, a discussion of the history of numeric codes can trigger several entries legitimately. This matcher reports evidence for review and does not classify messages or people.

## Maintenance

Review sources at least quarterly and after significant new research. Prioritize weak evidence, old reports, changing symbols, and search-only citations for full-page verification. Record source changes, revised interpretation, and removals in CHANGELOG.md. Add community-specific false-positive cases when justified. Do not scrape or republish entire proprietary glossaries.
