```mermaid
flowchart TD
  A[Başla] --> B[p ve q seç<br/>(p%4=3, q%4=3)]
  B --> C[n = p*q]
  C --> D[seed x seç<br/>(gcd(x,n)=1)]
  D --> E{L bit üretildi mi?}
  E -- Hayır --> F[x = x^2 mod n]
  F --> G[bit = LSB(x)]
  G --> H[bitleri anahtara ekle]
  H --> E
  E -- Evet --> I[Anahtarı çıktıya yaz]
  I --> J[Bitiş]