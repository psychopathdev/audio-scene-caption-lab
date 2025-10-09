"""Run a sweep from a yaml config."""
import argparse, yaml, json, os
from mmprobe.base import load_probe
from mmprobe.eval import evaluate
from mmprobe.runners import HFModelRunner


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--out-dir", default="reports/")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config))
    os.makedirs(args.out_dir, exist_ok=True)

    for model_id in cfg["models"]:
        print(f"==> loading {model_id}")
        runner = HFModelRunner(model_id, device=cfg.get("device", "cuda"))
        for probe_name in cfg["probes"]:
            probe = load_probe(probe_name)
            print(f"   running probe {probe_name}")
            rep = evaluate(probe, runner, n=cfg.get("n", 200), seed=cfg.get("seed", 0))
            safe = model_id.replace("/", "__")
            out = os.path.join(args.out_dir, f"{safe}__{probe_name}.json")
            with open(out, "w") as f:
                json.dump({"model": model_id, "probe": probe_name,
                           "accuracy": rep.accuracy,
                           "per_bucket": rep.per_bucket}, f, indent=2)
            print(f"      acc={rep.accuracy:.3f}  -> {out}")


if __name__ == "__main__":
    main()
