import json, os, sys, re
sys.path.insert(0, "localize")
from apply import find_literals, is_display_context, ROOTS

mapping = {}
for fn in sorted(os.listdir("localize")):
    if fn.startswith("zh_map") and fn.endswith(".json"):
        mapping.update(json.load(open(os.path.join("localize", fn), encoding="utf-8")))

targets = []
for root in ROOTS:
    if os.path.isfile(root):
        targets.append(root); continue
    for dp, _, fs in os.walk(root):
        for f in fs:
            if f.endswith(".swift"):
                targets.append(os.path.join(dp, f))

def has_cjk(s):
    return re.search(r"[\u4e00-\u9fff]", s) is not None

rows = []
for path in targets:
    src = open(path, encoding="utf-8").read()
    for (s, e, lit) in find_literals(src):
        key = lit if lit in mapping else lit.replace('\\"', '"')
        if key in mapping:
            continue
        if not is_display_context(src, s):
            continue
        if not lit.strip() or has_cjk(lit):
            continue
        if re.fullmatch(r"\\\(.*\)", lit):
            continue
        line = src.count("\n", 0, s) + 1
        rows.append((path, line, key))

seen = {}
for p, l, k in rows:
    seen.setdefault(k, []).append(f"{os.path.basename(p)}:{l}")

with open("localize/todo.txt", "w", encoding="utf-8") as fh:
    for k in sorted(seen, key=lambda x: x.lower()):
        fh.write(f"{k}\t{', '.join(seen[k][:3])}\n")
print("untranslated display strings:", len(seen))
