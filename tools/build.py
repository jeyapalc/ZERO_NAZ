"""Validate data and regenerate deterministic CSV/TXT/Markdown exports."""
import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from zero_naz import normalize

def build():
    entries=json.loads((ROOT/'data/entries.json').read_text(encoding='utf-8'))
    sources=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
    source_ids={s['id'] for s in sources}
    assert len(source_ids)==len(sources), 'Duplicate source IDs'
    assert len({e['id'] for e in entries})==len(entries), 'Duplicate entry IDs'
    required={'id','term','aliases','category','languages','meaning','source_ids','context','action','modality','context_note','reviewed_at','status'}
    for s in sources:
        assert s['url'].startswith('https://') and s['publisher'] and s['evidence_access']
    for e in entries:
        assert set(e)==required, e['id']
        assert e['source_ids'] and set(e['source_ids'])<=source_ids, e['id']
        assert e['context'] in {'strong_signal','ambiguous'}
        assert e['modality'] in {'text','visual_and_text','visual_only'}
        assert e['action']=='human_review'
        assert e['status']=='initial_research'
        assert e['languages'] and set(e['languages'])<={'en','de'}
        assert isinstance(e['aliases'],list) and all(isinstance(t,str) and t.strip() for t in [e['term'],*e['aliases']])
        assert re.fullmatch(r'\d{4}-\d{2}-\d{2}',e['reviewed_at'])
    out=ROOT/'lists'
    out.mkdir(exist_ok=True)
    for context in ['strong_signal','ambiguous']:
        terms={normalize(t) for e in entries if e['context']==context and e['modality']!='visual_only' and e['category']!='typographic_pattern' for t in [e['term'],*e['aliases']]}
        (out/f'{context}.txt').write_text('\n'.join(sorted(terms))+'\n',encoding='utf-8',newline='\n')
    for language in ['en','de']:
        terms={normalize(t) for e in entries if language in e['languages'] and e['modality']!='visual_only' and e['category']!='typographic_pattern' for t in [e['term'],*e['aliases']]}
        (out/f'{language}.txt').write_text('\n'.join(sorted(terms))+'\n',encoding='utf-8',newline='\n')
    stream=io.StringIO(newline='')
    fields=list(entries[0])
    writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n')
    writer.writeheader()
    for e in entries:
        writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,list) else v for k,v in e.items()})
    (ROOT/'data/entries.csv').write_text(stream.getvalue(),encoding='utf-8',newline='\n')
    def cell(value):
        return value.replace('|','\\|').replace('\n',' ')
    lines=['# ZERO_NAZ catalog','',f'{len(entries)} entries. All are human-review candidates; initial research has not received independent moderator review.','', '| Term | Aliases | Category | Languages | Context | Meaning | Sources |','| --- | --- | --- | --- | --- | --- | --- |']
    by_source={s['id']:s for s in sources}
    for e in entries:
        refs=', '.join(f"[{s}]({by_source[s]['url']})" for s in e['source_ids'])
        lines.append('| '+' | '.join(cell(v) for v in [e['term'],', '.join(e['aliases']),e['category'],', '.join(e['languages']),e['context'],e['meaning'],refs])+' |')
    (ROOT/'CATALOG.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
    print(f'Validated and exported {len(entries)} entries / {len(sources)} sources')

if __name__=='__main__':
    build()
    from export_review import export
    export(ROOT)

    from export_masterlist import export_masterlist
    export_masterlist(ROOT)
