from datetime import timedelta, timezone
import logging
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from account.forms import LoginUserForm, NewUserForm, UserPasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from libraryapp.models import PasswordResetCode
from .forms import NewUserForm 
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from .forms import SifreSifirlamaTalepFormu, SifreSifirlamaDogrulamaFormu
import random
import string

User = get_user_model()
def user_login(request):
    if request.user.is_authenticated and "next" in request.GET:
        return render(request, "account/login.html", {"error": "Yetkiniz yok!"})
    
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, "Giriş başarılı")
                nextUrl = request.GET.get("next", None)
                if nextUrl is None:
                    return redirect("index")
                else:
                    return redirect(nextUrl)
            else:
                return render(request, "account/login.html", {"form": form})
        else:
            return render(request, "account/login.html", {"form": form})
    else:
        form = LoginUserForm()
        return render(request, "account/login.html", {"form": form})

import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger('account')

def send_welcome_email(user_email):
    subject = 'Madbook - Kütüphane Maceran Başlıyor!'
    message = 'Merhaba, Madbook Kütüphanesine hoş geldiniz! Binlerce kitap ve kaynak seni bekliyor.'
    html_message = """
    <html>
    <head>
        <style>
            /* Genel Stil */
            body {
                font-family: 'Inter', 'Arial', sans-serif;
                background-color: #f4f7fa;
                margin: 0;
                padding: 0;
                color: #1a1a1a;
            }
            .email-container {
                max-width: 700px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 24px;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
                overflow: hidden;
                padding: 60px;
                position: relative;
            }
            /* Hafif doku efekti */
            .email-container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: url('https://www.transparenttextures.com/patterns/subtle-white-feathers.png');
                opacity: 0.05;
                z-index: 0;
            }
            .content {
                position: relative;
                z-index: 1;
            }
            /* Başlık */
            h1 {
                font-size: 36px;
                font-weight: 800;
                color: #1a3c34;
                text-align: center;
                margin: 0 0 20px;
                letter-spacing: -0.5px;
            }
            h1::before {
                content: '\\f02d'; /* Kitap ikonu */
                font-family: 'Font Awesome 6 Free';
                font-weight: 900;
                color: #2ab573;
                margin-right: 12px;
                font-size: 32px;
            }
            /* Paragraf */
            p {
                font-size: 16px;
                line-height: 1.8;
                color: #4a4a4a;
                text-align: center;
                margin: 0 0 30px;
            }
            /* Buton */
            .cta-button {
                display: inline-flex;
                align-items: center;
                background: linear-gradient(135deg, #2ab573, #1a8c5b);
                color: #ffffff;
                font-size: 18px;
                font-weight: 700;
                padding: 16px 40px;
                text-decoration: none;
                border-radius: 12px;
                box-shadow: 0 8px 20px rgba(42, 181, 115, 0.3);
                transition: all 0.3s ease;
            }
            .cta-button i {
                margin-right: 12px;
                font-size: 22px;
            }
            .cta-button:hover {
                background: linear-gradient(135deg, #1a8c5b, #156d46);
                transform: translateY(-4px);
                box-shadow: 0 12px 30px rgba(42, 181, 115, 0.5);
            }
            /* Vurgu Alanı */
            .highlight {
                background: #f1faf6;
                padding: 25px;
                border-radius: 12px;
                margin: 30px 0;
                text-align: center;
                font-size: 16px;
                color: #2a2a2a;
                border-left: 5px solid #2ab573;
            }
            .highlight strong {
                color: #1a3c34;
            }
            /* Footer */
            .footer {
                margin-top: 50px;
                text-align: center;
                font-size: 14px;
                color: #6b7280;
                border-top: 1px solid #e5e7eb;
                padding-top: 25px;
            }
            .footer a {
                color: #2ab573;
                text-decoration: none;
                font-weight: 600;
            }
            .footer a:hover {
                color: #1a8c5b;
                text-decoration: underline;
            }
            /* Mobil Uyumluluk */
            @media (max-width: 600px) {
                .email-container {
                    padding: 30px;
                    margin: 20px;
                }
                h1 {
                    font-size: 28px;
                }
                h1::before {
                    font-size: 26px;
                }
                p {
                    font-size: 14px;
                }
                .cta-button {
                    font-size: 16px;
                    padding: 12px 30px;
                }
                .highlight {
                    font-size: 14px;
                    padding: 20px;
                }
                .footer {
                    font-size: 12px;
                }
            }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    </head>
    <body>
        <div class="email-container">
            <div class="content">
                <h1>Madbook Maceran Başlıyor!</h1>
                <p>Merhaba! Madbook Kütüphanesine hoş geldin. Binlerce kitap, eşsiz hikayeler ve sınırsız bilgi seni bekliyor.</p>
                <div class="highlight">
                    <p><strong>Şimdi başla!</strong> Kütüphanemizin kapıları senin için ardına kadar açık.</p>
                </div>
                <div style="text-align: center; margin: 40px 0;">
                    <a href="http://127.0.0.1:8000" class="cta-button"><i class="fas fa-book-open"></i> Hemen Keşfet</a>
                </div>
                <p>Her sayfa yeni bir dünya. Madbook ile okumanın tadını çıkar!</p>
                <div class="footer">
                    <p><a href="http://127.0.0.1:8000">Madbook Kütüphanesi</a> © 2025</p>
                    <p>Soruların mı var? Bize ulaş: <a href="mailto:mahmut.demir0024@gmail.com">mahmut.demir0024@gmail.com</a></p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    print(f"E-posta deneniyor kanka: Gönderen: {from_email}, Alıcı: {user_email}")
    try:
        response = send_mail(subject, message, from_email, recipient_list, html_message=html_message, fail_silently=False)
        print(f"E-posta gönderildi kanka! Alıcı: {user_email}, Sonuç: {response}")
    except Exception as e:
        print(f"Hata çıktı kanka: {type(e).__name__} - {str(e)}")
        raise

def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            login(request, user)

            print(f"Kayıt başarılı kanka! Kullanıcı: {username}, E-posta: {user.email}")
            try:
                send_welcome_email(user.email)
                messages.success(request, "Madbook'a kayıt işleminiz başarıyla gerçekleşti ve hoş geldin e-postası gönderildi!")
            except Exception as e:
                messages.error(request, f"Kayıt başarılı, ancak e-posta gönderilemedi: {str(e)}")

            return redirect("index")
        else:
            # Form hatalarını mesaj olarak ekle
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}" if field != '__all__' else error)
            print("Form hataları kanka:", form.errors)
            return render(request, "account/register.html", {"form": form})
    else:
        form = NewUserForm()
    return render(request, "account/register.html", {"form": form})
    
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            logout(request)
            messages.success(request, "Parolanız başarıyla güncellendi! Lütfen yeni şifrenizle giriş yapın.")
            return redirect("user_login")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserPasswordChangeForm(request.user)

    return render(request, "account/change-password.html", {"form": form})

def user_logout(request):
    messages.add_message(request, messages.SUCCESS, "çıkış başarılı")
    logout(request) 
    return redirect("index")   

def sifre_sifirlama_talebi(request):
    if request.method == 'POST':
        form = SifreSifirlamaTalepFormu(request.POST)
        if form.is_valid():
            kimlik = form.cleaned_data['kimlik']
            try:
                if '@' in kimlik:
                    kullanici = User.objects.filter(email=kimlik).first()
                else:
                    kullanici = User.objects.filter(username=kimlik).first()
                
                if kullanici:
                    eposta = kullanici.email
                    kod = ''.join(random.choices(string.digits, k=6))
                    expires_at = timezone.now() + timedelta(minutes=10)
                    request.session['sifirlama_kodu'] = kod
                    request.session['sifirlama_eposta'] = eposta
                    PasswordResetCode.objects.create(
                        user=kullanici,
                        code=kod,
                        expires_at=expires_at
                    )
                    send_mail(
                        "Şifre Sıfırlama Kodu",
                        f"Şifrenizi sıfırlamak için kodunuz: {kod}",
                        'mailbotuyum@gmail.com',
                        [eposta],
                        fail_silently=False,
                    )
                    messages.success(request, "Doğrulama kodu e-postanıza gönderildi.")
                    return redirect('sifre_sifirlama_dogrulama')
                else:
                    messages.error(request, "Bu e-posta veya kullanıcı adıyla kayıtlı bir hesap bulunamadı.")
            except Exception as e:
                messages.error(request, f"Bir hata oluştu: {str(e)}")
    else:
        form = SifreSifirlamaTalepFormu()
    return render(request, 'account/sifre_sifirlama_talebi.html', {'form': form})

def sifre_sifirlama_dogrulama(request):
    if request.method == 'POST':
        form = SifreSifirlamaDogrulamaFormu(request.POST)
        if form.is_valid():
            kod = form.cleaned_data['kod']
            yeni_sifre = form.cleaned_data['yeni_sifre']
            yeni_sifre_tekrar = form.cleaned_data['yeni_sifre_tekrar']
            if kod == request.session.get('sifirlama_kodu'):
                if yeni_sifre == yeni_sifre_tekrar:
                    eposta = request.session.get('sifirlama_eposta')
                    kullanici = User.objects.filter(email=eposta).first()
                    if kullanici:
                        kullanici.set_password(yeni_sifre)
                        kullanici.save()
                        # Kodu kullanıldı olarak işaretle
                        PasswordResetCode.objects.filter(user=kullanici, code=kod).update(is_used=True)
                        del request.session['sifirlama_kodu']
                        del request.session['sifirlama_eposta']
                        messages.success(request, "Şifreniz başarıyla sıfırlandı. Giriş yapabilirsiniz.")
                        return redirect('user_login')
                    else:
                        messages.error(request, "Kullanıcı bulunamadı.")
                else:
                    messages.error(request, "Şifreler eşleşmiyor.")
            else:
                messages.error(request, "Geçersiz doğrulama kodu.")
    else:
        form = SifreSifirlamaDogrulamaFormu()
    return render(request, 'account/sifre_sifirlama_dogrulama.html', {'form': form})




