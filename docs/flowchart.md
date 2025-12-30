# Blum Blum Shub (BBS) Akış Şeması

```mermaid
flowchart TD
  A[Başla] --> B[p ve q seç (p mod 4 = 3)]
  B --> C[n = p * q]
  C --> D[Seed x seç (gcd(x,n)=1)]
  D --> E{L bit üretildi mi?}
  E --|Hayır|--> F[x = x^2 mod n]
  F --> G[Bit = LSB(x)]
  G --> H[Bitleri anahtara ekle]
  H --> E
  E --|Evet|--> I[Anahtarı çıktıya yaz]
  I --> J[Bitiş]
