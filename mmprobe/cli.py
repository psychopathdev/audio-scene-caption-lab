"""CLI: python -m mmprobe.cli run --probe counting --model ..."""
import argparse, json, sys
from .base import load_probe, list_probes
from .eval import evaluate


def cmd_list(_args):
    for name in list_probes():
        print(name)


def cmd_run(args):
    probe = load_probe(args.probe)
    if args.model.startswith("openai:"):
        from .runners import OpenAIRunner
        runner = OpenAIRunner(args.model.split(":", 1)[1])
    else:
        from .runners import HFModelRunner
        runner = HFModelRunner(args.model, device=args.device)
    report = evaluate(probe, runner, n=args.n, seed=args.seed)
    out = {
        "probe": report.probe,
        "n": report.n,
        "accuracy": report.accuracy,
        "per_bucket": report.per_bucket,
        "model": args.model,
    }
    if args.out:
        with open(args.out, "w") as f:
            json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))


def main():
    ap = argparse.ArgumentParser("mmprobe")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("list")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("run")
    sp.add_argument("--probe", required=True)
    sp.add_argument("--model", required=True)
    sp.add_argument("--n", type=int, default=200)
    sp.add_argument("--seed", type=int, default=0)
    sp.add_argument("--device", default="cuda")
    sp.add_argument("--out", default=None)
    sp.set_defaults(func=cmd_run)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
