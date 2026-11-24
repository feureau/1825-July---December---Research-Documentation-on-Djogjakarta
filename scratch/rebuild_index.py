import os, re, sys

# Map exact archival sections
def get_section(i):
    if 57 <= i <= 58:
        return "KITLV H 698 b / AvJ 1825"
    if 59 <= i <= 73:
        return "ARA 4132 / Collectie Smissaert"
    if i == 74:
        return "ARA 2789 / Besluit GG in Rade"
    if 75 <= i <= 76:
        return "ARA 4132 / Collectie Smissaert"
    if 77 <= i <= 80:
        return "ANRI Djokjo Brieven Bundel 81"
    if 81 <= i <= 82:
        return "ARA 4132 / Collectie Smissaert"
    if 83 <= i <= 85:
        return "Leiden BPL 616 / Nahuys Coll."
    if 86 <= i <= 87:
        return "ARA De Kock Coll. No. 181"
    if 88 <= i <= 96:
        return "ANRI / ARA Algemeen Verslag No. 54"
    if 97 <= i <= 100:
        return "ANRI / ARA Algemeen Verslag No. 54"
    if 101 <= i <= 108:
        return "ARA 4132 / Collectie Smissaert"
    if 109 <= i <= 110:
        return "ANRI / ARA Djogja Letters No. 54"
    if 111 <= i <= 130:
        return "ARA De Kock Coll. No. 179 (Surakarta Letters)"
    if 131 <= i <= 132:
        return "ARA De Kock / Aukes (Mangkunagaran Legion)"
    if 133 <= i <= 150:
        return "ARA De Kock Coll. No. 180 (Semarang Letters)"
    if 151 <= i <= 152:
        return "ARA 2791 / Besluit GG in Rade"
    if i == 153:
        return "Archival Tab Divider Recto"
    if i == 154:
        return "ARA De Kock Coll. No. 180 (Semarang Letters)"
    if 155 <= i <= 160:
        return "ARA De Kock Coll. No. 182 (Kedu Letters)"
    if i == 161:
        return "Archival Tab Divider Recto"
    if i == 162:
        return "Archival Tab Divider Verso"
    if 163 <= i <= 179:
        return "Van der Capellen Diary (TNI 1860)"
    return "Peter Carey Archival Notes"

abbrevs = ['A.D.', 'J.P.', 'H.J.', 'P.F.H.', 'G.A.G.Ph.', 'No.', 'pp.', 'etc.', 'Dr.', 'Col.', 'Gen.', 'Lt.', 'Capt.', 'Res.', 'Bp.', 'AJ.', 'f.', 'Dfl.', 'Dec.', 'Jan.', 'Feb.', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'cont.', 'vs.', 'viz.', 'St.']

def clean_sentence(raw, i):
    # Special handling for tab dividers
    if i == 153:
        return "Archival divider card recto: handwritten label `Kedu Letters` (Collectie De Kock No. 182)"
    if i == 161:
        return "Archival divider card recto: typewritten label `Van der Capellen`, handwritten red notation `42 / No. 2`"
    if i == 162:
        return "Archival divider card verso: blue ballpoint capital letters `PAMEKASAN`"

    s = raw
    for idx, a in enumerate(abbrevs):
        s = s.replace(a, f'__ABBR_{idx}__')
    
    sentences = re.split(r'[;.]\s+(?=[A-Z])', s)
    restored = []
    for sent in sentences:
        for idx, a in enumerate(abbrevs):
            sent = sent.replace(f'__ABBR_{idx}__', a)
        restored.append(sent.strip())
    
    res = restored[0] if restored else ''
    if len(restored) > 1 and len(res) + len(restored[1]) + 2 <= 165:
        res += '; ' + restored[1]
    if len(res) > 165:
        words = res.split()
        cand = ''
        for w in words:
            if len(cand) + len(w) + 1 <= 160:
                cand += (' ' if cand else '') + w
            else:
                break
        res = cand.rstrip(';., ') + '...'
    return res.rstrip(';., ')

# Load original 56 rows
sys.path.append('scratch')
from generate_index import original_rows

all_rows = []
for f, st, sec, dt, desc in original_rows:
    all_rows.append(f"{f} | {st} | {sec} | {dt} | {desc} |")

for i in range(57, 180):
    fn = f"transcriptions/IMG_{i:04d}.md"
    if not os.path.exists(fn):
        continue
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    
    date_m = re.search(r'-\s+\*\*Date Range:\*\*\s*`?([^`\r\n]+)`?', text)
    date = date_m.group(1).strip() if date_m else "N/A"
    
    sec = get_section(i)
    
    ke_m = re.search(r'-\s+\*\*Key Events:\*\*\s*(.+?)(?=-\s+\*\*Key Entities|\Z)', text, re.S)
    ke = ke_m.group(1).strip() if ke_m else ''
    ke = re.sub(r'\s+', ' ', ke)
    
    summary = clean_sentence(ke, i)
    
    all_rows.append(f"| [`IMG_{i:04d}.md`](transcriptions/IMG_{i:04d}.md) | ✅ Done | {sec} | {date} | {summary} |")

index_header = """# Master Index: Archival Research Documentation on Djogjakarta (1825)

This repository contains systematic transcriptions of Peter Carey's working research notes from the Dutch colonial archives (Leiden University Library B.P.L. 616 / Nahuys van Burgst Collection, Algemeen Rijksarchief De Kock Collection, etc.) regarding the outbreak and early months of the **Java War (Diponegoro War, 1825–1830)** in Yogyakarta.

All transcriptions feature:
* **Inline abbreviation expansions** (e.g., `DP [Diponegoro]`, `TR [Tegalrejo]`, `MB [Mangkubumi]`, `v d C [Van der Capellen]`).
* **Preservation of layout and marginalia** (dates, places, colored ink, strikethroughs).
* **Direct cross-referencing and validation** against [`39_Expanded_Keyword_Index.md`](39_Expanded_Keyword_Index.md).

---

## Transcription Progress Tracker

| File | Status | Section / Collection | Date Range (ISO 8601) | Key Events & Entities |
| :--- | :---: | :--- | :--- | :--- |
"""

full_content = index_header + "\n".join(all_rows) + "\n"

with open("INDEX.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Generated perfect INDEX.md with {len(all_rows)} rows!")
