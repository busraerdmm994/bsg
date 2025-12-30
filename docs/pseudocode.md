# Blum Blum Shub (BBS) — Sözde Kod (Pseudocode)

## Amaç
BBS, kriptografide örnek olarak anlatılan bir **pseudo-random bit generator**’dır.
Anahtar üretimi için belirli uzunlukta bit dizisi üretir.

## Parametreler
- Büyük iki asal sayı seç: `p, q` (şart: `p mod 4 = 3` ve `q mod 4 = 3`)
- `n = p * q`
- Seed (başlangıç değeri): `x0` (şart: `gcd(x0, n) = 1`)

## Pseudocode

INPUT: p, q, seed x0, çıktı bit sayısı L
OUTPUT: L bitlik anahtar

1. p ve q seç (p % 4 = 3, q % 4 = 3)
2. n = p * q
3. x = x0
4. Eğer gcd(x, n) != 1 ise yeni seed seç
5. key_bits = empty list
6. while length(key_bits) < L:
7.     x = (x * x) mod n
8.     bit = LSB(x)          // x’in en düşük biti
9.     append bit to key_bits
10. return key_bits

## Notlar
- Aynı (p, q, seed) ile çıktı deterministiktir.
- Seed gizli tutulur; seed sızarsa çıktı tahmin edilebilir.
- Eğitim amaçlı küçük sayılarla demo yapılabilir; gerçek kullanım için çok büyük p,q gerekir.
