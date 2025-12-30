#!/usr/bin/env python3
"""
Blum Blum Shub (BBS) Key Generator - Educational implementation.

Usage:
  python src/rng.py --bits 128
  python src/rng.py --bits 64 --seed 123456
  python src/rng.py --bits 64 --p 1000003 --q 1000039 --seed 12345
"""

from __future__ import annotations

import argparse
import os
import secrets
from datetime import datetime
from math import gcd
from typing import Tuple


def write_sample_output(bits: int, p: int, q: int, seed: int, hex_key: str) -> None:
    """Append run info into examples/sample_output.txt"""
    os.makedirs("examples", exist_ok=True)
    path = os.path.join("examples", "sample_output.txt")

    with open(path, "a", encoding="utf-8") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"Tarih: {datetime.now().isoformat()}\n")
        f.write("Komut:\n")
        f.write(f"python src/rng.py --bits {bits} --p {p} --q {q} --seed {seed}\n\n")
        f.write("Çıktı (Hex):\n")
        f.write(hex_key + "\n")
        f.write("=" * 50 + "\n")


def is_probable_prime(n: int) -> bool:
    """Deterministic-ish primality test for demo-scale integers."""
    if n < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    i = 31
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def generate_demo_prime(mod4_eq_3: bool = True, bits: int = 20) -> int:
    """Generate a small prime for demonstration. Not cryptographically secure."""
    while True:
        candidate = secrets.randbits(bits) | 1 | (1 << (bits - 1))
        if mod4_eq_3:
            candidate |= 3  # force %4==3
        if is_probable_prime(candidate) and (candidate % 4 == 3 if mod4_eq_3 else True):
            return candidate


def pick_seed(n: int, user_seed: int | None = None) -> int:
    """Pick seed x with gcd(x, n) == 1."""
    if user_seed is not None:
        x = abs(int(user_seed)) % n
        if x in (0, 1):
            x = (x + 2) % n
        if gcd(x, n) != 1:
            for k in range(2, 5000):
                y = (x + k) % n
                if y not in (0, 1) and gcd(y, n) == 1:
                    return y
            raise ValueError("Provided seed cannot be adjusted to be coprime with n.")
        return x

    while True:
        x = secrets.randbelow(n - 2) + 2
        if gcd(x, n) == 1:
            return x


def bbs_generate_bits(p: int, q: int, seed: int, bit_len: int) -> Tuple[str, int, int, int, int]:
    """Generate bit_len bits using BBS and return (bitstring, n, p, q, seed_used)."""
    if p == q:
        raise ValueError("p and q must be different primes.")
    if p % 4 != 3 or q % 4 != 3:
        raise ValueError("p and q must satisfy p % 4 == 3 and q % 4 == 3.")
    if not is_probable_prime(p) or not is_probable_prime(q):
        raise ValueError("p and q must be prime (demo primality check failed).")

    n = p * q
    x = pick_seed(n, seed)
    seed_used = x

    bits = []
    for _ in range(bit_len):
        x = (x * x) % n
        bits.append(str(x & 1))
    return "".join(bits), n, p, q, seed_used


def bits_to_hex(bitstring: str) -> str:
    value = int(bitstring, 2) if bitstring else 0
    hex_len = (len(bitstring) + 3) // 4
    return f"{value:0{hex_len}x}"


def main() -> None:
    parser = argparse.ArgumentParser(description="BBS Key Generator (Educational)")
    parser.add_argument("--bits", type=int, required=True)
    parser.add_argument("--p", type=int, default=None)
    parser.add_argument("--q", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--show-params", action="store_true")
    parser.add_argument("--no-log", action="store_true", help="Do not write examples/sample_output.txt")
    args = parser.parse_args()

    if args.bits <= 0:
        raise ValueError("--bits must be > 0")

    p = args.p if args.p is not None else generate_demo_prime(bits=20)
    q = args.q if args.q is not None else generate_demo_prime(bits=20)

    if args.seed is None:
        # random seed
        n_tmp = p * q
        seed = pick_seed(n_tmp, None)
    else:
        seed = args.seed

    bitstring, n, p_used, q_used, seed_used = bbs_generate_bits(p, q, seed, args.bits)
    hex_key = bits_to_hex(bitstring)

    print(hex_key)

    if args.show_params:
        print("\n--- params ---")
        print(f"bits: {args.bits}")
        print(f"p: {p_used}")
        print(f"q: {q_used}")
        print(f"n=p*q: {n}")
        print(f"seed_used: {seed_used}")
        print("-------------")

    if not args.no_log:
        write_sample_output(args.bits, p_used, q_used, seed_used, hex_key)


if __name__ == "__main__":
    main()
