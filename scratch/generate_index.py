import re
import os

# Original hand-curated rows 1 to 56
original_rows = [
    ("| [`IMG_0001.md`](transcriptions/IMG_0001.md)", "✅ Done", "Binder Cover", "1816 to 1825", "Outer folder cover: Research Documentation on Djogjakarta (1816–1825); British retrocession"),
    ("| [`IMG_0002.md`](transcriptions/IMG_0002.md)", "✅ Done", "Binder Inside Cover", "N/A", "Camilla Ring File manufacture details (Guidex British Made)"),
    ("| [`IMG_0003.md`](transcriptions/IMG_0003.md)", "✅ Done", "Section 1 Tab Divider", "N/A", "Section 1 tab: `de Kock Letters / de Kock No. 197`"),
    ("| [`IMG_0004.md`](transcriptions/IMG_0004.md)", "✅ Done", "Section 1 Tab Verso", "N/A", "Folder classification marking (`sm1407 05-3`)"),
    ("| [`IMG_0005.md`](transcriptions/IMG_0005.md)", "✅ Done", "De Kock Coll. No. 197", "1825-07-27 to 1825-07-29", "De Kock to Van der Capellen; Kumsius' convoy wiped out near Magelang; reports from Bandung, Semarang, Kedu"),
    ("| [`IMG_0006.md`](transcriptions/IMG_0006.md)", "✅ Done", "De Kock Coll. No. 197", "1825-07-28", "Letter heading: incoming correspondence from Kedu / Magelang"),
    ("| [`IMG_0007.md`](transcriptions/IMG_0007.md)", "✅ Done", "De Kock Coll. No. 197", "1825-08-09 to 1825-08-12", "Col. Cochius relief column; Smissaert; letter torn up by DP; Pasar Gede; reconnaissance of Selarong"),
    ("| [`IMG_0008.md`](transcriptions/IMG_0008.md)", "✅ Done", "De Kock Coll. No. 197", "1825-08-03 to 1825-10-08", "Gen. Van Geen operations against Selarong; Veltman attacked by white-robed priests; Pajang; Progo River"),
    ("| [`IMG_0009.md`](transcriptions/IMG_0009.md)", "✅ Done", "De Kock Coll. No. 197", "1825-10-07 to 1825-10-09", "Van Geen artillery on Progo; Mangkubumi to Siguluh; Diponegoro resolve; Pangeran Adinagara defection overtures"),
    ("| *IMG_0010*", "—", "*(Omitted in original scan numbering)*", "—", "*(File skipped in archival scan sequence)*"),
    ("| [`IMG_0011.md`](transcriptions/IMG_0011.md)", "✅ Done", "ARA De Kock Coll. No. 18", "1825-08-01", "De Kock's official Surakarta Proclamation to Inhabitants of Java/Djogja on rebellion of DP & MB"),
    ("| [`IMG_0012.md`](transcriptions/IMG_0012.md)", "✅ Done", "Section 2 Tab Divider", "N/A", "Section 2 tab: `Diary of Chevallier / N van B Port 9 No. 2`"),
    ("| [`IMG_0013.md`](transcriptions/IMG_0013.md)", "✅ Done", "Section 2 Tab Verso", "N/A", "Section 2 tab verso annotation referencing Raffles"),
    ("| [`IMG_0014.md`](transcriptions/IMG_0014.md)", "✅ Done", "Chevallier Diary (BPL 616)", "1825-07-16 to 1825-07-17", "Diponegoro gathers armed forces at Tegalrejo; tensions with Smissaert, Danureja IV, and Mangkubumi"),
    ("| [`IMG_0015.md`](transcriptions/IMG_0015.md)", "✅ Done", "Chevallier Diary (BPL 616)", "1825-07-19 to 1825-07-22", "Evacuation of DP family to Selarong; Mangkubumi joins DP; drinking party at Kraton; DP & MB declared outlaws"),
    ("| [`IMG_0016.md`](transcriptions/IMG_0016.md)", "✅ Done", "Chevallier Diary (BPL 616)", "1825-07-22 to 1825-07-25", "Arrival of Mangkunagaran Legion; cash transport ambushed (28,000 guilders); drunk fort commander; civil collapse"),
    ("| [`IMG_0017.md`](transcriptions/IMG_0017.md)", "✅ Done", "Chevallier Diary (BPL 616)", "1825-07-26 to 1825-08-01", "Mass princely desertions; suicide of Lt. Thierry; communications severed; Col. Cochius column arrives; pillagers hanged"),
    ("| [`IMG_0018.md`](transcriptions/IMG_0018.md)", "✅ Done", "Chevallier Diary (BPL 616)", "1825-08-02 to 1825-08-11", "Kraton / Mosque pillagers; Prince Abubakar defects; end of Chevallier's 1st Register signed 11 Aug 1825"),
    ("| [`IMG_0019.md`](transcriptions/IMG_0019.md)", "✅ Done", "Section 3 Tab Divider", "1825-01-01 to 1825-07-16", "Section 3 tab divider: `1825 to July 16th` (pre-war documentation)"),
    ("| [`IMG_0020.md`](transcriptions/IMG_0020.md)", "✅ Done", "Section 3 Financial Ledger", "1825-01", "Debts of Pangeran Purbaya (Pakubuwana VII) to Dezentjé, Stavers, MacGillavry (93,000+ guilders)"),
    ("| [`IMG_0021.md`](transcriptions/IMG_0021.md)", "✅ Done", "Nahuys Coll. No. 22", "1824-05-01 to 1825", "Tranjasan contract: Sasradiningrat II to Boutet (14 jonks, 400,000 coffee trees, 198,000 guilders debt)"),
    ("| [`IMG_0022.md`](transcriptions/IMG_0022.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-01-03 to 1825-01-08", "Tan Tan Lok land restitution; toll-gate keeper Tan Buntjut arrested; Pacitan road plans; clerks Dietzten & de Meijer"),
    ("| [`IMG_0023.md`](transcriptions/IMG_0023.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-01-08 to 1825-01-12", "Gunungkidul road; Karangbolong demands; Cholera behind Salatiga; Pacitan coffee/pepper (Wormser); toll resistance"),
    ("| [`IMG_0024.md`](transcriptions/IMG_0024.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-01-13 to 1825-01-19", "Yogya sarong exports to Semarang; Gunung Tawang toll arrears; Pacitan coffee; Chevallier on tour; Dietrée pension"),
    ("| [`IMG_0025.md`](transcriptions/IMG_0025.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-01-21 to 1825-02-04", "Bantul & Jatinom pasar toll surges (San Hiang Sing); Ex-Sultan HB II in Surabaya; Cholera epidemic in Yogya"),
    ("| [`IMG_0026.md`](transcriptions/IMG_0026.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-02-13 to 1825-02-28", "Guardians send 5000g to HB II; Mangkudiningrat buried Imogiri; Ratu Kencana keris stabbing incident in Kraton"),
    ("| [`IMG_0027.md`](transcriptions/IMG_0027.md)", "✅ Done", "AN Djogja Geheim No. 53", "1824-12-16 to 1825-03-15", "Majapahit keris lineage (Danureja I); Chevallier Jabarangkah Commission; envoys to Surabaya; Pekalongan unrest"),
    ("| [`IMG_0028.md`](transcriptions/IMG_0028.md)", "✅ Done", "AN Djogja Geheim No. 53", "1825-04-02 to 1825-04-05", "Klaten robbery bands; Pakualam retainer cross-border raid; Cirebon agitator in Banyumas; brandy for cholera"),
    ("| [`IMG_0029.md`](transcriptions/IMG_0029.md)", "✅ Done", "ARA No. 2787", "1822-02-08 to 1825-02-22", "G.G. Council Besluit annexing Jabarangkah / Karangkobar enclaves; coffee corvée; Landhuur abolition precedents"),
    ("| [`IMG_0030.md`](transcriptions/IMG_0030.md)", "✅ Done", "ARA No. 2787", "1824-01-31", "Expulsion order: Europeans and Chinese holding land after 31 Jan 1824 refused residence and expelled"),
    ("| [`IMG_0031.md`](transcriptions/IMG_0031.md)", "✅ Done", "Van Alphen-Engelhard XXIIc No. 283", "1825-01-07 to 1825-01-28", "Salt crisis in Vorstenlanden; Chinese toll extortion; Tan Tian Hok debt claim on Gladhag mantri; Chinese travel pass rules"),
    ("| [`IMG_0032.md`](transcriptions/IMG_0032.md)", "✅ Done", "Van Alphen-Engelhard XXIIc No. 283", "1825-03-25 to 1825-05-01", "Agrarian clashes on govt land; Thomas Davison; Kembang Arum takeover; North vs South coast salt economy"),
    ("| [`IMG_0033.md`](transcriptions/IMG_0033.md)", "✅ Done", "Van Alphen-Engelhard XXIIc No. 283", "1825-05-01", "Western vs Eastern Mancanagara hydrology; Cilacap harbor proposal; warning against banning southern salt; toll relief urged"),
    ("| [`IMG_0034.md`](transcriptions/IMG_0034.md)", "✅ Done", "Van Alphen-Engelhard XXIIc No. 283", "1825-06-29", "Judicial division in Vorstenlanden; colonial Landraden; Wiranagara report on 37 members of Surambi Islamic Court"),
    ("| [`IMG_0035.md`](transcriptions/IMG_0035.md)", "✅ Done", "Van Alphen-Engelhard XXIIc No. 283", "1825-06", "Anatomy of Yogya judiciary: Surambi (Mas Pengulu), Pradata (Nitipraja), Mancanagara Bupatis, and Balé Mangu (Kepatihan)"),
    ("| [`IMG_0036.md`](transcriptions/IMG_0036.md)", "✅ Done", "Section 4 Tab Divider", "N/A", "Section 4 tab: `Yogya Letters / de Kock No. 181`"),
    ("| [`IMG_0037.md`](transcriptions/IMG_0037.md)", "✅ Done", "Section 4 Tab Verso", "N/A", "Blank verso of Section 4 divider"),
    ("| [`IMG_0038.md`](transcriptions/IMG_0038.md)", "✅ Done", "Scholarly Research Inset (BKI 1951)", "1951 [1811–1830]", "Drewes on Indonesian autobiographies: Abdullah Munshi, Raffles, Diponegoro's Babad, Louw, Palmer van den Broek"),
    ("| [`IMG_0039.md`](transcriptions/IMG_0039.md)", "✅ Done", "Scholarly Research Inset (BKI 1951)", "1951 [1825–1830]", "Drewes on Majapahit descent; Smissaert's dismissal of Diponegoro's piety as \"madness\"; Du Bus de Gisignies"),
    ("| [`IMG_0040.md`](transcriptions/IMG_0040.md)", "✅ Done", "Scholarly Research Inset (BKI 1951)", "1951 [1825–1830]", "Drewes & Carey on Diponegoro as Erucakra / Ratu Adil; critique of Van der Kemp's Hamlet analogy; Jayabaya prophecies"),
    ("| [`IMG_0041.md`](transcriptions/IMG_0041.md)", "✅ Done", "Nahuys van Burgst (1835) pp. 10–11", "1825-08-03", "Deposition of RM Alip (part 1): Nahuys on Dipanagara's early conduct, De Kock interrogation, incitement of HB IV to retake Kedu"),
    ("| [`IMG_0042.md`](transcriptions/IMG_0042.md)", "✅ Done", "Nahuys van Burgst (1835) pp. 12–13", "1825-08-03", "Deposition of RM Alip (part 2): \"God dank\" on HB IV death, princely recruitment, targeted officials (Chevallier, Van den Berg, Bouwens), inner council (Demang Buro Resso, Sheikh Achmat, Moedo)"),
    ("| [`IMG_0043.md`](transcriptions/IMG_0043.md)", "✅ Done", "Nahuys van Burgst (1835) p. 14", "1825-08-03", "Deposition of RM Alip (conclusion): Ratu Ageng's letter, Dipanagara tears letter (\"a chicken has more fight in him\"); Nahuys critique on Alip's instability"),
    ("| [`IMG_0044.md`](transcriptions/IMG_0044.md)", "✅ Done", "Nahuys van Burgst (1835) p. 15", "1825 [1816–1825]", "Nahuys commentary on Dipanagara's co-guardianship of HB V, self-interest (*eigenbelang*) driving Javanese politics, Mangkubumi and Mas Said precedents"),
    ("| [`IMG_0045.md`](transcriptions/IMG_0045.md)", "✅ Done", "B.L.P. 616 / Port. 9 No. 2 pt 2", "1825-08-03", "Carey notes on Procès-Verbal of RM Alip: Grievances v. Dutch, Kedu demands, reaction to HB IV death, targeted officials, 2 Arab advisers, Pajang demang"),
    ("| [`IMG_0046.md`](transcriptions/IMG_0046.md)", "✅ Done", "B.L.P. 616 / Port. 9 No. 2 pt 2", "1825-08-03", "Carey notes on Procès-Verbal of RM Alip: Moedo warning, Pajang levies, Alip at Ratu Ageng's house, tearing of conciliation letter"),
    ("| [`IMG_0047.md`](transcriptions/IMG_0047.md)", "✅ Done", "Geheim en Kabinetsarchief (Causes of War .1.)", "1825-08", "Anonymous courtier's letter: Van der Capellen dispatch in Puasa Bé, Chevallier's humiliation of Dipanagara at Residency ball, Tegalrejo road markers pulled"),
    ("| [`IMG_0048.md`](transcriptions/IMG_0048.md)", "✅ Done", "Geheim en Kabinetsarchief (Causes of War)", "1825-07-15 to 1825-07-20", "Anonymous letter cont.: Road to Pasar Gede, Danureja recalled from Pajang, 4 Besar summons to Fort refused, Mangkubumi joins Dipanagara, demand to dismiss Patih"),
    ("| [`IMG_0049.md`](transcriptions/IMG_0049.md)", "✅ Done", "Geheim en Kabinetsarchief (Causes of War .2.)", "1825-07-20 to 1825-08", "Anonymous letter cont.: Assault on Tegalrejo by Chevallier & Major Wiranagara, burning of estate, retreat to Selarong, proclamation of Holy War (*Prang Sabil*)"),
    ("| [`IMG_0050.md`](transcriptions/IMG_0050.md)", "✅ Done", "Geheim en Kabinetsarchief (Causes of War)", "1825-08", "Intercepted letter from Queen Mothers (Ratu Ageng & Ratu Kencono): Fear of Sultan exiled to outer islands, anger at European oppression & collaborators, endorsement of Dipanagara as Sultan"),
    ("| [`IMG_0051.md`](transcriptions/IMG_0051.md)", "✅ Done", "Collectie Smissaert (ARA 4132)", "1823-01-04 to 1825-07-24", "Smissaert letters: Dipanagara piety dismissed as \"insanity\", Dipanagara letter of 19 July, Magelang treasury ambush (28,600 Dfl), Van der Capellen appointment letter"),
    ("| [`IMG_0052.md`](transcriptions/IMG_0052.md)", "✅ Done", "Collectie Smissaert (ARA 4132)", "1824-12-14 to 1825-01-29", "Van Sevenhoven correspondence: Jabarangkah lands (Wadas Wari, Kertanegara), Yogya territorial grievances, peasant destitution warning, Makassar expedition delay"),
    ("| [`IMG_0053.md`](transcriptions/IMG_0053.md)", "✅ Done", "Collectie Smissaert (ARA 4132)", "1823 to 1825", "Confidential personnel evaluations: Chevallier condemned for wickedness & corrupt heart, Van den Berg linguistic defects, J. Roos suitability"),
    ("| [`IMG_0054.md`](transcriptions/IMG_0054.md)", "✅ Done", "KITLV H 698 b / AvJ 1825", "1824-12-16 to 1825-07", "P. Mangkudiningrat repatriation, Ratu Kencono keris stabbing, flight of Ratu Ageng & HB V with Kris Pendawa Gajah, pawned jonks table to Danureja IV"),
    ("| [`IMG_0055.md`](transcriptions/IMG_0055.md)", "✅ Done", "KITLV H 698 b / AvJ 1825", "1825-07-15 to 1825-08", "Translaat Brieven: Hermits (Tyagaragas) at Mt. Majasta, Semarawijaya mobilizing Tembayat, Dipanagara at Téligong, MacGillavry orders to Banyumas bupatis, Karangkajen & Kojoran"),
    ("| [`IMG_0056.md`](transcriptions/IMG_0056.md)", "✅ Done", "KITLV H 698 b / AvJ 1825", "1825-05-14 to 1825-08-27", "Translaat Brieven: Order of Dipanagara for 2 soldiers per jonk, first mention of Kyai Maja of Boyolali, sigillography of Danureja IV, Major Wiranagara, and Paku Alam I")
]

def clean_source_v2(src, text, i):
    if i in [95, 96]:
        return "Archival Tab Divider (Smissaert)" if i == 95 else "Archival Tab Divider Verso"
    if i in [109, 110]:
        return "Archival Tab Divider (Surakarta)" if i == 109 else "Archival Tab Divider Verso"
    if i in [131, 132]:
        return "Archival Tab Divider (Biroe Binder)" if i == 131 else "Archival Tab Divider Verso"
    if i in [151, 152, 153]:
        return "Archival Tab Divider (Kedu Letters)" if i == 151 else "Archival Tab Divider Verso"
    if i in [161, 162]:
        return "Archival Tab Divider (Van der Capellen)" if i == 161 else "Archival Tab Divider Verso"

    if i >= 163 or "Van der Capellen" in src and "Diary" in src or "Tijdschrift voor Neêrland" in src:
        return "Van der Capellen Diary (TNI 1860)"
    if "Collectie De Kock No. 182" in src or "Kedu Letters" in src:
        return "ARA De Kock Coll. No. 182 (Kedu Letters)"
    if "Collectie De Kock No. 180" in src or "Semarang Letters" in src:
        return "ARA De Kock Coll. No. 180 (Semarang Letters)"
    if "Collectie De Kock No. 179" in src or "Surakarta Letters" in src:
        return "ARA De Kock Coll. No. 179 (Surakarta Letters)"
    if "Collectie De Kock No. 181" in src:
        return "ARA De Kock Coll. No. 181"
    if "Collectie De Kock No. 183" in src:
        return "ARA De Kock Coll. No. 183"
    if "Collectie De Kock" in src and "No. 18" in src:
        return "ARA De Kock Coll. No. 18"
    if "ANRI Djokjo Brieven Bundel 81" in src or "Dj. Br. 81" in src:
        return "ANRI Djokjo Brieven Bundel 81"
    if "Collectie Smissaert" in src or "ARA 4132" in src:
        return "ARA 4132 / Collectie Smissaert"
    if "Nahuys van Burgst" in src or "BPL 616" in src:
        return "Leiden BPL 616 / Nahuys Coll."
    if "Algemeen Verslag" in src:
        return "ANRI / ARA Algemeen Verslag No. 54"
    if "KITLV H 698" in src or "AvJ 1825" in src:
        return "KITLV H 698 b / AvJ 1825"
    if "Cornets de Groot" in src:
        return "Surakarta Dispatches (Cornets de Groot)"
    if "ARA 2789" in src:
        return "ARA 2789 / Besluit GG in Rade"

    m = re.search(r'\(([^)]+)\)', src)
    if m:
        res = m.group(1).strip()
        res = res.replace("Nationaal Archief, The Hague", "").strip("; ")
        if len(res) > 38:
            res = res[:35] + "..."
        return res
    return src[:35]

def summarize_key_events(ke, i):
    # Specialized or refined summaries for high clarity
    if not ke:
        return "Archival research notes on Java War operations and colonial governance"
    
    # Clean whitespace
    ke = re.sub(r'\s+', ' ', ke).strip()

    # Split into sentences or clauses
    clauses = [c.strip() for c in re.split(r'[;.]\s+', ke) if c.strip()]
    condensed = ""
    for c in clauses:
        # avoid broken endings or abbreviations
        if len(condensed) + len(c) < 165:
            condensed += ("; " if condensed else "") + c
        else:
            if not condensed:
                condensed = c[:155] + "..."
            break
    
    # If ends with abbreviation or period
    condensed = condensed.rstrip(";., ")
    return condensed

new_rows = []
# Add original 56 rows
for f, st, sec, dt, desc in original_rows:
    new_rows.append(f"{f} | {st} | {sec} | {dt} | {desc} |")

# Process 57 to 179
for i in range(57, 180):
    fn = f"transcriptions/IMG_{i:04d}.md"
    if not os.path.exists(fn):
        continue
    with open(fn, "r", encoding="utf-8") as f:
        text = f.read()

    # Source
    src_m = re.search(r'-\s+\*\*Source:\*\*\s*(.+)', text)
    src_raw = src_m.group(1).strip() if src_m else "Archival Notes"
    src_clean = clean_source_v2(src_raw, text, i)

    # Date
    date_m = re.search(r'-\s+\*\*Date Range:\*\*\s*`?([^`\r\n]+)`?', text)
    date = date_m.group(1).strip() if date_m else "N/A"

    # Key events
    ke_m = re.search(r'-\s+\*\*Key Events:\*\*\s*(.+?)(?=-\s+\*\*Key Entities|\Z)', text, re.S)
    ke = ke_m.group(1).strip() if ke_m else ""
    ke_clean = summarize_key_events(ke, i)

    new_rows.append(f"| [`IMG_{i:04d}.md`](transcriptions/IMG_{i:04d}.md) | ✅ Done | {src_clean} | {date} | {ke_clean} |")

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

full_content = index_header + "\n".join(new_rows) + "\n"

with open("INDEX.md", "w", encoding="utf-8") as f:
    f.write(full_content)

print(f"Re-generated INDEX.md successfully with {len(new_rows)} rows!")
