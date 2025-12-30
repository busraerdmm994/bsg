# rng-keygen (BBS Key Generator)
230541022 Büşra Erdem
Bu repo, Bilgi Sistemleri Güvenliği dersi kapsamında **anahtar üreteci** olarak kullanılabilecek
bir **rastgele bit üretimi** (CSPRNG örneği) algoritması olan **Blum Blum Shub (BBS)** ile
istenen uzunlukta anahtar (bit dizisi) üretir.

## İçerik
- `docs/pseudocode.md` : Sözde kod
- `docs/flowchart.md`  : Algoritma akış şeması (Mermaid)
- `docs/security_notes.md` : Güvenlik notları + final analiz checklist
- `src/rng.py` : Python implementasyonu (CLI)
- `examples/sample_output.txt` : Örnek çıktılar
- `tests/quick_tests.py` : Basit istatistik testleri (frekans / runs)

## Kurulum
Python 3.10+ önerilir.

```bash
pip install -r requirements.txt
