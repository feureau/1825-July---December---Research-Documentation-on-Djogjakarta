import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT, "INDEX.md")
DATA_JSON_PATH = os.path.join(ROOT, "data.json")


def strip_md_inline(text: str) -> str:
    # Remove backticks and light emphasis while preserving readable text
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def main() -> None:
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = []
    missing = []
    # Match lines like: | [`IMG_0001.md`](transcriptions/IMG_0001.md) | ... | section | dateRange | summary |
    row_re = re.compile(
        r"^\|\s*\[`(IMG_\d{4})\.md`\]\((transcriptions/IMG_\d{4}\.md)\)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|"
    )

    for line in lines:
        m = row_re.match(line.strip())
        if not m:
            continue
        doc_id = m.group(1).strip()
        md_rel = m.group(2).strip()
        section = strip_md_inline(m.group(4))
        date_range = strip_md_inline(m.group(5))
        summary = strip_md_inline(m.group(6))
        jpg_rel = f"jpg/{doc_id}.jpg"

        jpg_abs = os.path.join(ROOT, jpg_rel)
        md_abs = os.path.join(ROOT, md_rel)

        if not os.path.isfile(jpg_abs):
            missing.append(jpg_rel)
        if not os.path.isfile(md_abs):
            missing.append(md_rel)

        entries.append(
            {
                "id": doc_id,
                "image": jpg_rel,
                "text": md_rel,
                "section": section,
                "dateRange": date_range,
                "summary": summary,
            }
        )

    if missing:
        raise RuntimeError(f"Missing files detected: {missing}")

    # Verify against actual jpg/ and transcriptions/ counts
    jpg_files = sorted(f for f in os.listdir(os.path.join(ROOT, "jpg")) if f.lower().endswith(".jpg"))
    md_files = sorted(f for f in os.listdir(os.path.join(ROOT, "transcriptions")) if re.match(r"^IMG_\d{4}\.md$", f))
    if len(entries) != len(jpg_files) or len(entries) != len(md_files):
        raise RuntimeError(
            f"Count mismatch: index={len(entries)}, jpg={len(jpg_files)}, transcriptions={len(md_files)}"
        )

    with open(DATA_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {len(entries)} entries to data.json (0 missing files).")


if __name__ == "__main__":
    main()
