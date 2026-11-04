"""One-time provenance-preserving initial dataset construction."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-11-03'
sources = {}
entries = []

def source(key, publisher, title, url, access='web_page'):
    sources[key] = dict(id=key, publisher=publisher, title=title, url=url,
                        checked_at=DATE, evidence_access=access)
    return key

def adl(key, slug):
    return source(key, 'Anti-Defamation League', slug.replace('-', ' ').title(),
                  'https://www.adl.org/resources/hate-symbol/' + slug)

def add(id, term, aliases, category, languages, meaning, refs, context='ambiguous', note=None, modality='text'):
    entries.append(dict(id=id, term=term, aliases=aliases, category=category,
        languages=languages.split(','), meaning=meaning, source_ids=refs.split(','),
        context=context, action='human_review', modality=modality,
        context_note=note or ('Common numbers, abbreviations, names, historical quotation, and ordinary usage require contextual interpretation.' if context=='ambiguous' else 'Review whether this is endorsement, a threat, reporting, quotation, education, or counterspeech.'),
        reviewed_at=DATE, status='initial_research'))

bige=source('bige', 'Bayerische Informationsstelle gegen Extremismus', 'Rechtsextremistische Zeichen und Symbole', 'https://www.bige.bayern.de/informationen-zu-extremismus/rechtsextremismus/zeichen-und-symbole-rechtsextremismus/')
nds=source('nds', 'Verfassungsschutz Niedersachsen', 'Zahlen- und Buchstabenkombinationen auf Kfz-Kennzeichen', 'https://www.verfassungsschutz.niedersachsen.de/startseite/aktuelles_service/aktuelle_meldungen/rechtsextremisten-nutzen-zahlen-und-buchstabenkombinationen-auf-kfz-kennzeichen-199847.html')
bw=source('bw', 'Landesamt für Verfassungsschutz Baden-Württemberg', 'Zeichen und Symbole', 'https://www.verfassungsschutz-bw.de/%2CLde_DE/Startseite/Arbeitsfelder/Zeichen%2Bund%2BSymbole')
for key,slug in [('adl-crime','1352-1390'),('adl-2316','2316'),('adl-318','318'),('adl-336','336'),('adl-271k','271k')]:
    adl(key,slug)
numeric_sources={'13/52':'adl-crime','13/90':'adl-crime','23/16':'adl-2316','318':'adl-318','33/6':'adl-336','271k':'adl-271k'}
for num,meaning in [('18','Hitler initials.'),('88','Nazi greeting code.'),('28','Blood & Honour code.'),('19/8','Nazi victory greeting code.'),('192','Hitler-return code.'),('444','Ethnonationalist slogan code.'),('168:1','Oklahoma City attack glorification.')]:
    add('code-'+num.replace('/','-').replace(':','-'),num,[], 'numeric_code','en,de',meaning,bige)
for term,aliases,meaning in [('Blut und Ehre',[],'Hitler Youth slogan.'),('Meine Ehre heißt Treue',['Meine Ehre heisst Treue','Meine Ehre heißt Treue!'],'SS motto.'),('Unsere Ehre heißt Treue',['Unsere Ehre heisst Treue'],'SS motto variant.'),('Alles für Deutschland',[],'SA slogan.'),('Frei, sozial und national',[],'Neo-Nazi demonstration slogan.'),('Nationaler Sozialismus jetzt',[],'Neo-Nazi demonstration slogan.')]:
    add('de-'+str(len(entries)+1),term,aliases,'slogan','de',meaning,bige,'strong_signal')
add('combat-18','Combat 18',['C18'],'organization','en,de','Neo-Nazi organization.',bige)
add('blood-honour','Blood & Honour',['Blood and Honour'],'organization','en,de','Racist skinhead network.',bige)
for term,meaning in [('AH','Hitler initials.'),('BH','Blood & Honor initials.'),('HH','Nazi greeting initials.'),('HJ','Hitlerjugend initials.'),('SS','Schutzstaffel initials.'),('SA','Sturmabteilung initials.'),('NS','Nationalsozialismus initials.'),('WP','White Power or White Pride initials.'),('25','Blut & Ehre code.'),('198','Sieg Heil code.'),('204','Hitler birthday code.'),('2004','Hitler birthday code.')]:
    add('short-'+term.lower(),term,[],'numeric_code' if term.isdigit() else 'acronym','en,de',meaning,nds)
add('hitler','Adolf Hitler',[],'person','en,de','Historical Nazi leader.',nds)
for term in ['Heil Hitler','Sieg Heil','Mit deutschem Gruß','Sieg und Heil für Deutschland']:
    add('greeting-'+str(len(entries)+1),term,[],'slogan','de','Historical Nazi greeting.',bw,'strong_signal')
for num,meaning in [('13/52','Racist crime-statistics dogwhistle.'),('13/90','Racist crime-statistics dogwhistle.'),('23/16','White Power code.'),('318','Combat 18-associated code.'),('33/6','Klan-associated code.'),('271k','Holocaust victim-count denial code.')]:
    add('number-'+num.replace('/','-'),num,[],'numeric_code','en,de',meaning,numeric_sources[num])
adl('adl-1488','1488')
add('1488','1488',['14/88','14-88','8814'],'numeric_code','en,de','Combined Fourteen Words and Nazi greeting code.','adl-1488')
add('fourteen','14 Words',['Fourteen Words','14'],'slogan','en','White supremacist slogan reference.','adl-1488')
adl('adl-311','311')
add('311','311',[],'numeric_code','en,de','Klan code: three instances of the eleventh letter.','adl-311',note='Also a non-extremist band name, municipal service number, and ordinary number.')
adl('adl-109','109110')
add('109','109',['110','109/110','1488-110'],'numeric_code','en,de','Antisemitic expulsion myth and calls for another expulsion.','adl-109',note='110 is also a German emergency number; ordinary quantities are not evidence of hate.')
adl('adl-rahowa','rahowa')
add('rahowa','RAHOWA',['Racial Holy War'],'acronym','en','White supremacist rallying cry.','adl-rahowa','strong_signal')
adl('adl-zog','zog')
add('zog','ZOG',['Zionist Occupied Government'],'conspiracy','en','Antisemitic government-control conspiracy code.','adl-zog')
adl('adl-sun','sonnenrad')
add('black-sun','Sonnenrad',['Black Sun','Schwarze Sonne'],'visual_symbol','en,de','Nazi-derived twelve-ray design used by white supremacists.','adl-sun',note='Generic sunwheels and the words black sun have unrelated uses. Text matching cannot identify the specific design.',modality='visual_and_text')
adl('adl-othala','othala-rune')
add('othala','Othala',['Odal rune','Othala rune','Odalrune','ᛟ'],'visual_symbol','en,de','Rune appropriated by Nazis and white supremacists.','adl-othala',note='Runic writing and non-racist pagan uses are common. Unicode glyph does not encode stylistic variants.',modality='visual_and_text')
for term,aliases,meaning in [('Hakenkreuz',['Swastika','卐','卍'],'Nazi appropriation of an older symbol.'),('Doppel-Sigrune',['SS bolts','SS runes','ᛋᛋ'],'SS insignia.'),('SS-Totenkopf',[], 'Specific SS skull insignia.'),('Keltenkreuz',['Celtic cross'],'Cross design with extremist and other uses.')]:
    add('symbol-'+str(len(entries)+1),term,aliases,'visual_symbol','en,de',meaning,bige,modality='visual_and_text',note='Text labels or Unicode approximations cannot establish visual design or intent. Religious, historical, cultural, and educational uses require review.')
source('ajc-echo','American Jewish Committee','(((echo)))','https://www.ajc.org/index.php/translatehate/echo','search_index_excerpt; direct fetch returned 403')
add('echo','(((echo)))',[],'typographic_pattern','en,de','Triple parentheses used to mark Jewish targets.','ajc-echo',note='Also used in solidarity and quotation. Detects structure, not the identity of the enclosed person.')
source('ajc-hoax','American Jewish Committee','Holohoax','https://www.ajc.org/index.php/translatehate/Holohoax','search_index_excerpt; direct fetch returned 403')
add('holohoax','Holohoax',[],'holocaust_denial','en','Holocaust-denial term.','ajc-hoax','strong_signal')
source('adl-anudda','Anti-Defamation League','Anudda Shoah','https://nynj.adl.org/resources/hate-symbol/anudda-shoah','search_index_excerpt')
add('anudda','Anudda Shoah',[],'holocaust_mockery','en','Antisemitic mockery of Jews and Holocaust remembrance.','adl-anudda','strong_signal')
source('adl-gorillion','Anti-Defamation League','Six Gorillion','https://education.adl.org/resources/hate-symbol/six-gorillion','search_index_excerpt')
add('gorillion','Six Gorillion',['Muh Six Gorillion'],'holocaust_mockery','en','Mocks the Holocaust victim count.','adl-gorillion','strong_signal')
source('turner','Anti-Defamation League','The Turner Diaries','https://www.adl.org/resources/backgrounder/turner-diaries','search_index_excerpt')
add('turner','The Turner Diaries',[],'publication','en','White supremacist novel.','turner')
add('rope','Day of the Rope',[],'violent_reference','en','Reference to mass lynching in The Turner Diaries.','turner','strong_signal')
source('adl-wpww','Anti-Defamation League','WPWW','https://notoleranceforantisemitism.adl.org/resources/hate-symbol/wpww','search_index_excerpt')
add('wpww','WPWW',['White Pride World Wide'],'acronym','en','White supremacist slogan acronym.','adl-wpww','strong_signal')
add('stormfront','Stormfront',[],'organization','en','White supremacist website name.','adl-wpww')
source('adl-swp','Anti-Defamation League','SWP','https://www.adl.org/resources/hate-symbol/swp','search_index_excerpt')
add('swp','SWP',['Supreme White Power'],'acronym','en','White supremacist slogan initials.','adl-swp',note='SWP has unrelated political and technical meanings; initials alone are weak evidence.')
source('adl-german','Anti-Defamation League','German Phrases','https://notoleranceforantisemitism.adl.org/resources/hate-symbol/german-phrases','search_index_excerpt')
add('blood-soil','Blut und Boden',['Blood and Soil'],'slogan','en,de','Racial-nationalist slogan used by neo-Nazis.','adl-german','strong_signal')
source('ushmm','United States Holocaust Memorial Museum','Deadly Medicine: Creating the Master Race','https://www.ushmm.org/exhibition/deadly-medicine/overview/','search_index_excerpt')
add('hygiene','Rassenhygiene',['racial hygiene'],'historical_term','en,de','Racist eugenics concept.','ushmm',note='German translation supplied by project. Common in critical history, medicine, and museum discussion.')
source('unwort','Sprachkritische Aktion Unwort des Jahres','2010–2019: Volksverräter','https://www.unwortdesjahres.net/unwort/das-unwort-seit-1991/2010-2019/','search_index_excerpt')
add('traitor','Volksverräter',['Volksverraeter'],'contextual_term','de','Political insult with a history in dictatorships.','unwort',note='Not specific to neo-Nazism. Review target, intimidation, and surrounding rhetoric.')
source('adl-print','Anti-Defamation League','Hate on Display printable database (2023)','https://www.adl.org/sites/default/files/documents/2023-03/hate-on-display-hate-symbols-database.pdf','search_index_excerpt')
add('skrewdriver','Skrewdriver',[],'music','en','White power band.','adl-print')
add('donaldson','Ian Stuart Donaldson',[],'person','en','Skrewdriver leader.','adl-print')
source('adl-zyklon','Anti-Defamation League','Hate on Display printable database: Zyklon B','https://go.adl.org/sites/default/files/ADL%20Hate%20on%20Display%20Printable_0.pdf','search_index_excerpt')
add('zyklon','Zyklon B',[],'historical_term','en,de','Nazi killing agent referenced in antisemitic abuse.','adl-zyklon',note='Historical, scientific, and memorial references are legitimate; do not expand this to every mention of Zyklon.')
source('adl-pepe','Anti-Defamation League','Pepe the Frog','https://www.adl.org/resources/hate-symbol/pepe-frog','search_index_excerpt')
add('pepe','Pepe the Frog',[],'visual_symbol','en','Meme with hateful and non-hateful uses.','adl-pepe',modality='visual_and_text',note='Ordinary Pepe memes and frog emoji are not evidence of extremism. Inspect the specific depiction and surrounding content.')
source('adl-okay','Anti-Defamation League','Okay Hand Gesture','https://midwest.adl.org/resources/hate-symbol/okay-hand-gesture','search_index_excerpt')
add('okay','Okay hand gesture',[],'visual_symbol','en','Common gesture sometimes appropriated by extremists.','adl-okay',modality='visual_only',note='Ordinary gestures and the okay emoji are overwhelmingly ambiguous. Excluded from literal exports and the text matcher.')

# Additional source-attested variants and entity references.
by_id={entry['id']:entry for entry in entries}
by_id['number-13-52']['aliases']=['13/50']
by_id['number-318']['aliases']=['8318']
by_id['number-33-6']['aliases']=['33/5']
by_id['number-271k']['aliases']=['271,000','271']
by_id['combat-18']['aliases']+=['C-18']
by_id['combat-18']['source_ids']+=['adl-318']
add('kkk','Ku Klux Klan',['KKK'],'organization','en,de','White supremacist Klan reference.','adl-311')
add('aryan-terror','Aryan Terror Brigade',[],'organization','en','Racist skinhead group.','adl-318')
add('white-power','White Power',[],'slogan','en','White supremacist slogan.',nds,'strong_signal')
add('fourteen-full','We must secure the existence of our people and a future for white children',[],'slogan','en','Fourteen Words slogan.','adl-1488','strong_signal')

for name,data in [('entries',entries),('sources',list(sources.values()))]:
    path=ROOT/'data'/f'{name}.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Wrote {len(entries)} entries and {len(sources)} sources')
