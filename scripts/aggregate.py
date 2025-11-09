"""Aggregate per-run JSON reports into a single CSV."""
import argparse, csv, glob, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="reports/")
    ap.add_argument("--out", default="reports/all.csv")
    args = ap.parse_args()

    rows = []
    for path in glob.glob(os.path.join(args.dir, "*.json")):
        with open(path) as f:
            data = json.load(f)
        rows.append({"model": data["model"], "probe": data["probe"],
                     "accuracy": data["accuracy"]})

    if not rows:
        print("no reports found")
        return
    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["model", "probe", "accuracy"])
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {len(rows)} rows -> {args.out}")


if __name__ == "__main__":
    main()
