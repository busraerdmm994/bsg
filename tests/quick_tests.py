#!/usr/bin/env python3
"""
Quick (very basic) statistical sanity checks for generated bits.
Not a replacement for real RNG test suites (Dieharder, NIST STS, etc.).
"""

from __future__ import annotations

import argparse
import subprocess
from collections import Counter


def run_generator(bits: int, seed: int | None) -> str:
    cmd = ["python", "src/rng.py", "--bits", str(bits)]
    if seed is not None:
        cmd += ["--seed", str(seed)]
    out = subprocess.check_output(cmd, text=True).strip()
    # hex -> bitstring
    value = int(out, 16) if out else 0
    bitstring = bin(value)[2:].zfill(bits)
    return bitstring


def frequency_test(bitstring: str) -> dict:
    c = Counter(bitstring)
    zeros = c.get("0", 0)
    ones = c.get("1", 0)
    n = len(bitstring)
    return {
        "n": n,
        "zeros": zeros,
        "ones": ones,
        "ones_ratio": ones / n if n else 0.0,
    }


def runs_test(bitstring: str) -> dict:
    if not bitstring:
        return {"runs": 0, "avg_run_len": 0.0}
    runs = 1
    run_lengths = []
    current_len = 1
    for i in range(1, len(bitstring)):
        if bitstring[i] == bitstring[i - 1]:
            current_len += 1
        else:
            runs += 1
            run_lengths.append(current_len)
            current_len = 1
    run_lengths.append(current_len)
    avg_len = sum(run_lengths) / len(run_lengths)
    return {"runs": runs, "avg_run_len": avg_len, "max_run_len": max(run_lengths)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bits", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    bits = run_generator(args.bits, args.seed)

    freq = frequency_test(bits)
    runs = runs_test(bits)

    print("=== Frequency Test ===")
    print(freq)
    print("\n=== Runs Test ===")
    print(runs)
    print("\nNot: Bu sadece kaba bir kontrol. Gerçek değerlendirme için daha kapsamlı test suite gerekir.")


if __name__ == "__main__":
    main()
