"""Generate the SOC2020 -> NS-SEC (simplified method) recode rules for soc2nssec.ado.

Source: ONS, SOC 2020 Volume 3 (NS-SEC rebased on SOC 2020), derivation
Tables 9-12, file tables912v6.xlsx. The simplified method uses the "ssec"
column (operational category) for each SOC 2020 unit group.

Usage:
    python tools/make_soc2020_recode.py tables912v6.xlsx soc2nssec.ado

Every operational-category sheet (Tables 9 and 11) with an "ssec" column is read;
the SOC code is taken from the first column unless a column is labelled SOC. The
script stops if two sheets disagree for the same unit group, then writes the
recode rules between the BEGIN/END markers in the ado file.
"""
import re
import sys
from collections import defaultdict

import openpyxl

BEGIN = "/* BEGIN SOC2020 RECODE (generated) */ ///"
END = "/* END SOC2020 RECODE (generated) */ ///"


def norm_ssec(v):
    """Turn a cell such as 3.1, '3.1', 'L3.1' or 13 into an operational-category string."""
    if v is None:
        return None
    s = str(v).strip().upper().lstrip("L")
    if not s:
        return None
    if not re.fullmatch(r"\d{1,2}(\.\d)?", s):
        raise ValueError(f"unexpected ssec value: {v!r}")
    if s.endswith(".0"):
        s = s[:-2]
    return s


def read_sheet(ws):
    rows = list(ws.iter_rows(values_only=True))
    # Use only the operational-category tables (Tables 9 and 11), not the
    # analytic-class tables (10 and 12) or the headings key.
    title = " ".join(str(c) for r in rows[:3] for c in r if c is not None).lower()
    if "operational categor" not in title:
        return None
    for i, row in enumerate(rows):
        cells = [str(c).strip().lower() if c is not None else "" for c in row]
        if "ssec" in cells:
            ssec_col = cells.index("ssec")
            soc_col = next(
                (j for j, c in enumerate(cells) if "soc" in c or "unit group" in c), 0
            )
            out = {}
            for r in rows[i + 1:]:
                code = r[soc_col]
                if code is None:
                    continue
                m = re.match(r"^\s*(\d{4})\b", str(code))
                if not m:
                    continue
                val = norm_ssec(r[ssec_col])
                if val is not None:
                    out[int(m.group(1))] = val
            return out
    return None


def main(xlsx, ado):
    wb = openpyxl.load_workbook(xlsx, data_only=True, read_only=True)
    mapping, seen_in = {}, {}
    for ws in wb.worksheets:
        got = read_sheet(ws)
        if not got:
            continue
        print(f"{ws.title}: {len(got)} unit groups with ssec")
        for code, val in got.items():
            if code in mapping and mapping[code] != val:
                sys.exit(f"Conflict for {code}: {mapping[code]} ({seen_in[code]}) vs {val} ({ws.title})")
            mapping[code] = val
            seen_in.setdefault(code, ws.title)
    if not mapping:
        sys.exit("No sheet with a SOC column and an 'ssec' column was found.")
    print(f"Total unit groups mapped: {len(mapping)}")

    # Group codes by operational category, ordered numerically.
    by_val = defaultdict(list)
    for code, val in sorted(mapping.items()):
        by_val[val].append(code)
    lines = []
    for val in sorted(by_val, key=float):
        codes = by_val[val]
        for k in range(0, len(codes), 10):
            chunk = " ".join(map(str, codes[k:k + 10]))
            lines.append(f"\t\t\t\t({chunk} = {val}) ///")
    lines.append("\t\t\t\t(else = .) ///")

    src = open(ado, encoding="utf-8").read()
    pre, rest = src.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    new = pre + BEGIN + "\n" + "\n".join(lines) + "\n\t\t\t\t" + END + post
    open(ado, "w", encoding="utf-8").write(new)

    with open("soc2020_ssec_lookup.csv", "w") as f:
        f.write("soc2020,ssec\n")
        for code, val in sorted(mapping.items()):
            f.write(f"{code},{val}\n")
    print(f"Updated {ado}; wrote soc2020_ssec_lookup.csv")


if __name__ == "__main__":
    main(*sys.argv[1:3])
