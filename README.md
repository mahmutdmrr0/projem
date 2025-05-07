<p align="center">
  <img src="screenshots/trans1.png" alt="MADBOOK Logo" width="200"/>
</p>

<h1 align="center">MADBOOK: Kitap Aşıkları ve Sosyal Bağlar 📚</h1>

<p align="center">
  <a href="https://www.djangoproject.com/"><img src="https://img.shields.io/badge/Django-4.2-green.svg" alt="Django"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11-blue.svg" alt="Python"></a>
  <a href="https://railway.app/"><img src="https://img.shields.io/badge/Hosted-Railway-orange.svg" alt="Railway"></a>
  <a href="https://www.postgresql.org/"><img src="https://img.shields.io/badge/Database-PostgreSQL-blue.svg" alt="PostgreSQL"></a>
</p>

<p align="center">
  MADBOOK, kitap tutkunları için bir sosyal cennet! 📖 Django ile geliştirilmiş bu platformda, kitapları okuyup yorum yapabilir, yıldız verebilir, arkadaşlarınızla mesajlaşabilir ve şikayet bildirebilirsiniz. Her 1 dakikada gözlerinizi koruyan dinlenme modalıyla, hem sosyal hem sağlıklı! Railway’de PostgreSQL ile çalışıyor, reCAPTCHA ile güvenli.
</p>

---

## 🚀 Özellikler

- 📖 **Kitap Detayları**: Başlık, yazar, özet ve daha fazlası.
- ⭐ **Yıldız Derecelendirme**: Kitaplara puan ver.
- 💬 **Yorum Sistemi**: Yorum yap, tartışmalara katıl.
- ⏰ **Dinlenme Modalı**: Göz sağlığınız için mola uyarısı.
- 🔒 **reCAPTCHA**: Spam koruması.
- 📩 **Mesajlaşma**: Okunmamış mesaj bildirimleri.
- 🤝 **Arkadaşlık Sistemi**: Yeni kitap dostları edin.
- 🚨 **Şikayet Paneli**: Bildirim ve yönetim ekranı.
- 🛠️ **Admin Panel**: İçerik kontrolü.
- ☁️ **Railway Deployment**: Hızlı ve güvenilir sunum.

---

## 📸 Ekran Görüntüleri

### 🏠 Anasayfa ve Navigasyon

| Anasayfa 1 | Anasayfa 2 | Navbar | Footer |
|------------|------------|--------|--------|
| ![](screenshots/anasayfa-1.jpg) | ![](screenshots/anasayfa-2.jpg) | ![](screenshots/navbar.jpg) | ![](screenshots/footer.jpg) |

---

### 📚 Kitap ve Kategoriler

| Kategori Sayfası | Kitap Listesi | Kitaplık Sayfası | 
|------------------|---------------|------------------|
| ![](screenshots/category-page.jpg) | ![](screenshots/book-list.jpg) | ![](screenshots/bookcase-page.jpg) | 

---

### 📘 Kitap Detay Sayfası

| Detay Sayfası 1 | Detay Sayfası 2 | Detay Sayfası 3 | Detay Sayfası 4 |
|-----------------|-----------------|-----------------|-----------------|
| ![](screenshots/detay-sayfası-1.jpg) | ![](screenshots/detay-sayfası-2.jpg) | ![](screenshots/detay-sayfası-3.jpg) | ![](screenshots/detay-sayfası-4.jpg) |

---

### 🤖 Chatbot ve Arama

| Chatbot 1 | Chatbot 2 | Arama Sayfası |
|-----------|-----------|---------------|
| ![](screenshots/chatbot-1.jpg) | ![](screenshots/chatbot-2.jpg) | ![](screenshots/search-page.jpg) |

---

### 👤 Profil ve Arkadaşlık

| Profil 1 | Profil 2 | Arkadaşlar Sayfası 1 | Arkadaşlar Sayfası 2 |
|----------|----------|---------------------|----------------------|
| ![](screenshots/profil-1.jpg) | ![](screenshots/profil-2.jpg) | ![](screenshots/friends-page-1.jpg) | ![](screenshots/friends-page-2.jpg) |

| Arkadaşlar Sayfası 3 | Arkadaşlar Sayfası 4 | Arkadaşlarla Sohbet |
|----------------------|----------------------|--------------------|
| ![](screenshots/friends-page-3.jpg) | ![](screenshots/friends-page-4.jpg) | ![](screenshots/friends-chat.jpg) |

---

### 🔐 Giriş, Kayıt ve Şifre İşlemleri

| Giriş | Kayıt | Şifre Değiştirme | Şifremi Unuttum |
|-------|-------|------------------|-----------------|
| ![](screenshots/login.jpg) | ![](screenshots/register.jpg) | ![](screenshots/sifre-degistirme.jpg) | ![](screenshots/password-not-remember.jpg) |

---

### ⚙️ Yönetici Paneli ve Şikayetler

| Admin Şikayet Paneli | Kullanıcı Şikayet Sayfası 
|----------------------|---------------------------
| ![](screenshots/admin-sikayet.jpg) | ![](screenshots/report-page.jpg) | 

---

### 🌿 Dinlenme Modülü ve Hakkında

| Dinlenme Modülü | Dinlenme Sayfası | Hakkında Sayfası |
|-----------------|------------------|------------------|
| ![](screenshots/relas-modul.jpg) | ![](screenshots/relax-page.jpg) | ![](screenshots/about-page.jpg) |

---

### 🎞️ Uygulama Animasyonu

<p align="center">
  <img src="screenshots/Animasyon.gif" alt="Animasyon">
</p>

---

## 🔗 Canlı Demo

🎯 **Projeyi canlı inceleyin:**  
👉 [MADBOOK Canlı Site](https://web-production-c8a3.up.railway.app/library/)

---

## 💼 Kullanılan Teknolojiler

- Python 3.11
- Django 4.2
- PostgreSQL
- Railway
- HTML5, CSS3, JavaScript
- Bootstrap ve Tailwind
- Pillow, reCAPTCHA, Django Messages

---

## 🛠️ Kurulum

```bash
git clone https://github.com/mahmutdmrr0/madbook.git
cd madbook
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver