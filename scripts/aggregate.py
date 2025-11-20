"""Aggregate per-run JSON reports into a single CSV + pivot."""
import argparse, csv, glob, json, os
from collections import defaultdict


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="reports/")
    ap.add_argument("--out", default="reports/all.csv")
    ap.add_argument("--pivot", default="reports/pivot.csv")
    args = ap.parse_args()

    rows = []
    for path in glob.glob(os.path.join(args.dir, "*.json")):
        with open(path) as f:
            data = json.load(f)
        if "accuracy" not in data:
            continue
        rows.append({"model": data["model"], "probe": data["probe"],
                     "accuracy": data["accuracy"]})

    if not rows:
        print("no reports found")
        return

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "probe", "accuracy"])
        w.writeheader()
        w.writerows(rows)

    table = defaultdict(dict)
    probes = set()
    for r in rows:
        table[r["model"]][r["probe"]] = r["accuracy"]
        probes.add(r["probe"])
    probes = sorted(probes)
    with open(args.pivot, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model"] + probes)
        for m, by_probe in sorted(table.items()):
            w.writerow([m] + [f"{by_probe.get(p, ''):.3f}" if p in by_probe else "" for p in probes])
    print(f"wrote {len(rows)} rows -> {args.out}")
    print(f"pivot -> {args.pivot}")


if __name__ == "__main__":
    main()
