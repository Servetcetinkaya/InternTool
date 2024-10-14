import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# E-posta sunucu ayarları
smtp_server = "smtp.gmail.com"  # Gmail için SMTP sunucusu
smtp_port = 587  # SMTP portu
email_kullanici = "senin@gmail.com"  # Kendi e-posta adresin
email_sifre = ""  # Kendi e-posta şifren (Uygulama şifresi kullanmanı öneririm)

# E-posta gönderme fonksiyonu
def mail_gonder(kime, isim, konu, mesaj_sablonu, dosya_yolu):
    # İsim placeholder'ını değiştir
    mesaj = mesaj_sablonu.replace("{isim}", isim)
    
    # E-posta içeriklerini ayarlama
    msg = MIMEMultipart()
    msg['From'] = email_kullanici
    msg['To'] = kime
    msg['Subject'] = konu
    msg.attach(MIMEText(mesaj, 'plain'))

    # Dosya ekleme (CV veya başka bir dosya)
    with open(dosya_yolu, 'rb') as file:
        part = MIMEApplication(file.read(), Name=dosya_yolu.split('/')[-1])
        part['Content-Disposition'] = f'attachment; filename="{dosya_yolu.split("/")[-1]}"'
        msg.attach(part)

    # SMTP server'a bağlanma ve mail gönderme
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_kullanici, email_sifre)
        server.sendmail(email_kullanici, kime, msg.as_string())
        server.quit()
        print(f"{kime} adresine e-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderme hatası: {e}")

# mail.txt dosyasından e-posta adreslerini ve isimleri okuma
with open("mail.txt", "r") as file:
    email_listesi = file.readlines()

# mesaj.txt dosyasından mesaj şablonunu okuma
with open("mesaj.txt", "r") as file:
    mesaj_sablonu = file.read()

# E-posta konusu
konu = "Uzun Dönem İş Yeri Eğitimi"

# CV dosyasının yolu
cv_dosyasi = "servetcv.pdf"  # Buraya CV dosyanın tam yolunu yaz, eğer tool ile aynı dizindeyse gerek yok.

# Tüm e-posta adreslerine mesaj gönderme
for satir in email_listesi:
    # Satırı kontrol et, eğer iki değere bölünmüyorsa atla
    try:
        email, isim = satir.strip().split(',')  # E-posta ve ismi ayır
        mail_gonder(email.strip(), isim.strip(), konu, mesaj_sablonu, cv_dosyasi)
    except ValueError:
        print(f"Satır hatalı formatta: {satir.strip()}")
