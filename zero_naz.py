"""Dependency-free reference matcher. Hits are review candidates, never verdicts."""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def normalize(text):
    text = unicodedata.normalize('NFKC', text).casefold()
    text = ''.join(c for c in text if unicodedata.category(c) != 'Cf')
    return ' '.join(text.split())

def pattern(term):
    return re.compile(r'(?<![^\W_])' + re.escape(normalize(term)) + r'(?![^\W_])')

def load_entries():
    return json.loads((ROOT / 'data/entries.json').read_text(encoding='utf-8'))

def scan(text, include_ambiguous=False):
    normalized = normalize(text)
    hits = []
    for entry in load_entries():
        if entry['modality'] == 'visual_only':
            continue
        if entry['context'] == 'ambiguous' and not include_ambiguous:
            continue
        terms = [entry['term'], *entry['aliases']]
        matches = []
        if entry['id'] == 'echo':
            matches = [m.group() for m in re.finditer(r'\({3,}[^()\n]{1,100}\){3,}', normalized)]
        else:
            matches = [term for term in terms if pattern(term).search(normalized)]
        if matches:
            hits.append(dict(id=entry['id'], term=entry['term'], matched=matches,
                context=entry['context'], action='human_review',
                source_ids=entry['source_ids'], context_note=entry['context_note']))
    return hits

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('text', nargs='?', help='Text to inspect; stdin if omitted')
    parser.add_argument('--include-ambiguous', action='store_true', help='Include weak signals, names, numbers, runes, and contextual terms')
    args = parser.parse_args()
    import sys
    text = args.text if args.text is not None else sys.stdin.read()
    print(json.dumps(dict(action='human_review', hits=scan(text,args.include_ambiguous)),ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()
