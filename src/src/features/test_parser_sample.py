from __future__ import annotations

import argparse
import os
import random
import re
from pathlib import Path
from typing import Dict, List

try:
    import lizard
    HAS_LIZARD = True
except ImportError:
    HAS_LIZARD = False

def basic_metrics(code: str) -> Dict[str, float]:
    lines = code.splitlines()
    total = len(lines)
    comment = len([l for l in lines if l.strip().startswith("//")])
    blank = len([l for l in lines if not l.strip()])
    return {
        "loc": total,
        "comment_ratio": comment / total if total else 0.0,
        "blank_ratio": blank / total if total else 0.0,
    }

def analyze_file(path: Path) -> Dict[str, float]:
    if HAS_LIZARD:
        res = lizard.analyze_file(str(path))
        funcs = res.function_list or []
        return {
            "loc": res.nloc,
            "token": res.token_count,
            "cyclomatic_avg": (
                sum(f.cyclomatic_complexity for f in funcs) / len(funcs)
                if funcs
                else 0.0
            ),
            "functions": len(funcs),
        }
    return basic_metrics(path.read_text(encoding="utf-8", errors="ignore"))

def collect_source_files(dataset_root: Path) -> List[Path]:
    pattern = re.compile(r"\.(c|cpp)$", re.IGNORECASE)
    return [
        p
        for p in dataset_root.rglob("*")
        if p.is_file() and pattern.search(p.name)
    ]

def main() -> None:
    parser = argparse.ArgumentParser("Parser smoke-test")
    parser.add_argument(
        "--dataset-path",
        default="src/dataset/c",
        help="Root folder containing ai/ and human/",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=5,
        help="Number of random files to inspect",
    )
    args = parser.parse_args()

    root = Path(args.dataset_path)
    if not root.exists():
        raise FileNotFoundError(f"Dataset path not found: {root}")

    files = collect_source_files(root)
    if not files:
        print("❌ No C/C++ files detected.")
        return

    sample_files = random.sample(files, min(args.samples, len(files)))
    print(f"🔍 Analysing {len(sample_files)} sample submissions …\n")

    header_printed = False
    for fp in sample_files:
        metrics = analyze_file(fp)
        if not header_printed:
            # print table header once
            cols = ["file"] + list(metrics.keys())
            print("\t".join(cols))
            header_printed = True

        values = [fp.relative_to(root).as_posix()] + [f"{v:.2f}" if isinstance(v, float) else str(v) for v in metrics.values()]
        print("\t".join(values))


if __name__ == "__main__":
    main()