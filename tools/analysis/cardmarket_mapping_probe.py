#!/usr/bin/env python3
"""Probe how well Cardmarket products can be mapped to TCGdex cards.

Usage:
  python3 tools/analysis/cardmarket_mapping_probe.py \
      price_guide_6.json products_singles_6.json products_nonsingles_6.json path/to/tcgdex/cards-database

Inputs are the public Cardmarket download files (not committed) and a clone of
https://github.com/tcgdex/cards-database (MIT). Prints coverage statistics that
back docs/08-id-mapping.md. Pure stdlib, no side effects.
"""
import collections
import json
import os
import re
import sys


def load(path, key):
    with open(path, encoding="utf-8") as f:
        return json.load(f)[key]


def tcgdex_ids(root):
    """Return ({cardmarket idProduct: card path}, {idExpansion: set path}, {set path: Counter(en names)})."""
    cm_re = re.compile(r"cardmarket:\s*(\d+)")
    name_re = re.compile(r'\b(?:en|ja|de):\s*"((?:[^"\\]|\\.)*)"')
    cards, sets, names = {}, {}, collections.defaultdict(collections.Counter)
    for base in ("data", "data-asia"):
        for dp, _, fn in os.walk(os.path.join(root, base)):
            for f in fn:
                if not f.endswith(".ts"):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, root)
                txt = open(p, encoding="utf-8").read()
                m = cm_re.search(txt)
                if rel.count("/") >= 3:
                    if m:
                        cards[int(m.group(1))] = rel
                    n = name_re.search(txt)
                    if n:
                        names[os.path.dirname(rel)][n.group(1).lower()] += 1
                elif rel.count("/") == 2 and m:
                    sets[int(m.group(1))] = os.path.splitext(rel)[0]
    return cards, sets, names


def number_of(path):
    m = re.match(r"(\d+)", os.path.basename(path)[:-3])
    return int(m.group(1)) if m else None


def main():
    guide, singles, nonsingles, root = sys.argv[1:5]
    P = {r["idProduct"]: r for r in load(guide, "priceGuides")}
    S = load(singles, "products")
    N = load(nonsingles, "products")
    cards, sets, tnames = tcgdex_ids(root)

    covered = [r for r in S if r["idProduct"] in cards]
    print(f"singles: {len(S)} | mapped via TCGdex thirdParty: {len(covered)} ({100*len(covered)/len(S):.1f}%)")
    trend = lambda i: (P.get(i) or {}).get("trend") or 0
    tot = sum(trend(r["idProduct"]) for r in S)
    cov = sum(trend(r["idProduct"]) for r in covered)
    print(f"trend-weighted coverage: {100*cov/tot:.1f}%")

    exp2set = collections.defaultdict(collections.Counter)
    for r in covered:
        exp2set[r["idExpansion"]][os.path.dirname(cards[r["idProduct"]])] += 1
    exps = {r["idExpansion"] for r in S}
    mapped = set(exp2set) | (exps & set(sets))
    print(f"expansions: {len(exps)} | mapped: {len(mapped)} | 1:1 clean: {sum(1 for c in exp2set.values() if len(c)==1)}")

    dup = collections.defaultdict(list)
    for r in S:
        dup[(r["idExpansion"], r["name"])].append(r["idProduct"])
    groups = [sorted(v) for v in dup.values() if len(v) > 1]
    full = [v for v in groups if all(i in cards for i in v)]
    ordered = sum(1 for v in full if all(
        number_of(cards[a]) is not None and number_of(cards[b]) is not None and number_of(cards[a]) < number_of(cards[b])
        for a, b in zip(v, v[1:])))
    print(f"same-name groups within expansion: {len(groups)} (rows {sum(len(v) for v in groups)}) | "
          f"fully mapped: {len(full)} | idProduct order == number order: {ordered} ({100*ordered/max(1,len(full)):.1f}%)")

    cm = collections.defaultdict(collections.Counter)
    for r in S:
        cm[r["idExpansion"]][re.sub(r"\s*\[.*\]$", "", r["name"]).lower()] += 1
    jac = lambda a, b: len(set(a) & set(b)) / len(set(a) | set(b)) if set(a) | set(b) else 0
    bins = collections.Counter()
    for e in exps - mapped:
        best = max((jac(cm[e], tnames[s]) for s in tnames), default=0)
        bins["jaccard>=0.8" if best >= .8 else "0.6-0.8" if best >= .6 else "0.4-0.6" if best >= .4 else "<0.4"] += sum(cm[e].values())
    print("unmapped expansions, cards by best name-overlap with a TCGdex set:", dict(bins))

    exp_names = collections.defaultdict(list)
    for r in N:
        exp_names[r["idExpansion"]].append(r["name"])
    guess = sum(1 for e in exps if any(n.endswith((" Booster", " Booster Box", " Elite Trainer Box")) for n in exp_names.get(e, [])))
    print(f"expansions with a name derivable from nonsingles: {guess}")


if __name__ == "__main__":
    main()
