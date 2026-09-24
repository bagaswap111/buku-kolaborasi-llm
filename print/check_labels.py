import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(
    r"C:\Users\bagas\AppData\Roaming\Open Design\namespaces\release-stable-win"
    r"\data\projects\7edb36e4-0c2f-40a8-a492-052922993752\print\preview"
)

ok = True
for name in ("jilid-1", "jilid-2"):
    t = (ROOT / f"{name}.html").read_text(encoding="utf-8")

    # cari contoh markup label
    i = t.find(">Tabel ")
    print(name, "sample label markup:", repr(t[max(0, i - 40) : i + 50]))

    labels = re.findall(r'>Tabel (\d+)\.(\d+):', t)
    ch = defaultdict(list)
    for a, b in labels:
        ch[int(a)].append(int(b))
    good = True
    for k in sorted(ch):
        seq = ch[k]
        if seq != list(range(1, len(seq) + 1)):
            good = False
            ok = False
            print(f"  BROKEN bab {k}: {seq}")
    print(f"  {len(ch)} bab, {len(labels)} label — sequential 1..N: {good}")

    figs = re.findall(r'Gambar (\d+)\.(\d+)-(\d+)', t)
    fch = defaultdict(lambda: defaultdict(list))
    for a, b, c in figs:
        fch[int(a)][int(b)].append(int(c))
    fok = True
    for a in sorted(fch):
        for b in sorted(fch[a]):
            seq = fch[a][b]
            # bisa ada duplikat label+ref; cek unik terurut minimal
            uniq = sorted(set(seq))
            if uniq != list(range(1, len(uniq) + 1)):
                fok = False
                ok = False
                print(f"  BROKEN Gambar bab{a} sub{b}: {seq}")
    print(f"  Gambar sequential: {fok}")

print("RESULT:", "OK" if ok else "BROKEN")
