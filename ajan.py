import requests
import json


def topla(a, b):
    """İki sayıyı toplar."""
    return a + b


def carp(a, b):
    """İki sayıyı çarpar."""
    return a * b


def dosya_yaz(dosya_adi, icerik):
    """Verilen içeriği belirtilen dosyaya yazar."""
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(icerik)
    return f"{dosya_adi} dosyası oluşturuldu."


def ollama_ile_konus(prompt, model="qwen2.5-coder:7b"):
    """Ollama'nın yerel API'sine istek gönderir ve model cevabını döndürür."""
    url = "http://localhost:11434/api/generate"

    veri = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    cevap = requests.post(url, json=veri)
    sonuc = cevap.json()

    return sonuc["response"]


def ajan_karar_ver(kullanici_sorusu):
    """Kullanıcı sorusunu analiz eder, gerekli aracı JSON formatında seçer."""
    sistem_talimati = """Sen bir kodlama ajanısın. Elinde şu araçlar var:
- topla(a, b): iki sayıyı toplar
- carp(a, b): iki sayıyı çarpar
- dosya_yaz(dosya_adi, icerik): verilen kodu bir dosyaya yazar

Kullanıcı senden bir kod/program/script yazmanı isterse, o kodu kendin üret
ve dosya_yaz aracını kullan. SADECE şu formatlardan birini döndür, başka
hiçbir açıklama ekleme:

{"arac": "topla", "a": <sayı>, "b": <sayı>}
{"arac": "carp", "a": <sayı>, "b": <sayı>}
{"arac": "dosya_yaz", "dosya_adi": "<dosya_adi.py>", "icerik": "<python kodu>"}
{"arac": "yok", "cevap": "<normal cevabın>"}

ÖNEMLİ: icerik alanındaki kod içinde çift tırnak kullanma, tek tırnak kullan.
Kodun içindeki satır sonlarını \\n ile belirt.
"""

    tam_prompt = sistem_talimati + "\n\nKullanıcı isteği: " + kullanici_sorusu

    model_cevabi = ollama_ile_konus(tam_prompt)
    return model_cevabi


def ajan_calistir(kullanici_sorusu):
    """Modelden karar alır, JSON'u parse eder ve doğru fonksiyonu çalıştırır."""
    ham_cevap = ajan_karar_ver(kullanici_sorusu)

    try:
        karar = json.loads(ham_cevap)
    except json.JSONDecodeError:
        return f"Model geçersiz JSON döndürdü:\n{ham_cevap}"

    arac = karar.get("arac")

    if arac == "topla":
        return f"Sonuç: {topla(karar['a'], karar['b'])}"
    elif arac == "carp":
        return f"Sonuç: {carp(karar['a'], karar['b'])}"
    elif arac == "dosya_yaz":
        return dosya_yaz(karar["dosya_adi"], karar["icerik"])
    elif arac == "yok":
        return karar["cevap"]
    else:
        return f"Bilinmeyen araç: {arac}"


if __name__ == "__main__":
    print("=== Kodlama Ajanı ===")
    print("Çıkmak için 'çıkış' yaz.\n")

    while True:
        kullanici_sorusu = input("Sen: ")

        if kullanici_sorusu.lower() in ["çıkış", "exit", "quit"]:
            print("Görüşürüz!")
            break

        sonuc = ajan_calistir(kullanici_sorusu)
        print(f"Ajan: {sonuc}\n")