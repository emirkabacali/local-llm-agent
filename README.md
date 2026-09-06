# Yerel LLM ile Kodlama Ajanı

Ollama üzerinde çalışan yerel bir dil modelini (Qwen2.5-Coder) kullanarak
basit görevleri yerine getiren, araç çağırma (tool-calling) mantığıyla
çalışan bir yapay zeka ajanı.

## Nasıl Çalışır?

1. Kullanıcı doğal dilde bir istek girer (örn: "23 ile 47'yi topla" veya
   "1'den 10'a kadar çift sayıları toplayan bir script yaz")
2. Model isteği analiz eder ve hangi aracı kullanması gerektiğine
   JSON formatında karar verir
3. Python, bu JSON'u okuyup ilgili gerçek fonksiyonu çalıştırır
4. Sonuç kullanıcıya döndürülür

Bu proje, LangChain/CrewAI gibi framework'lerin arka planda kullandığı
temel tool-calling mimarisini sıfırdan, framework kullanmadan göstermek
amacıyla geliştirilmiştir.

## Kullanılan Araçlar (Tools)

| Araç | Açıklama |
|------|----------|
| `topla(a, b)` | İki sayıyı toplar |
| `carp(a, b)` | İki sayıyı çarpar |
| `dosya_yaz(dosya_adi, icerik)` | Modelin ürettiği kodu bir dosyaya kaydeder |

## Teknolojiler

- **Python 3**
- **Ollama** – yerel LLM çalıştırma
- **Qwen2.5-Coder:7b** – kodlama görevleri için optimize edilmiş açık kaynak model
- **requests** – Ollama API ile iletişim

## Kurulum

1. [Ollama](https://ollama.com) kurun
2. Modeli indirin:
ollama pull qwen2.5-coder:7b

3. Sanal ortam oluşturup bağımlılıkları kurun:

python -m venv venv
venv\Scripts\activate
pip install requests

4. Ajanı çalıştırın:

python ajan.py


## Örnek Kullanım

Sen: 23 ile 47'yi topla
Ajan: Sonuç: 70

Sen: 1'den 10'a kadar çift sayıları toplayan bir script yaz, cift.py olarak kaydet
Ajan: cift.py dosyası oluşturuldu.


## Gelecek Planları

- [ ] Dosya okuma aracı
- [ ] Ajanın kendi ürettiği kodu otomatik test etmesi ve hataları düzeltmesi
- [ ] Web arama aracı
- [ ] Çoklu ajan (multi-agent) mimarisine geçiş

## Yazar

Emir Kabacalı – Bilgisayar Mühendisliği Öğrencisi