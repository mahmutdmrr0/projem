from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm
from django.forms import widgets
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_recaptcha.fields import ReCaptchaField

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(attrs={"class": "form-control"})
        self.fields["password"].widget = widgets.PasswordInput(attrs={"class": "form-control"})

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username == "admin":
            messages.add_message(self.request,messages.SUCCESS, "Hoş geldin Admin ")

        return username
    # def confirm_login_allowed(self, user):
    #     if user.username.startswith("s"):
    #         raise forms.ValidationError("bu kullanıcı ile login olamazsınınz")

class NewUserForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2", "captcha")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = widgets.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Kullanıcı Adı"
        })
        self.fields["email"].widget = widgets.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "E-posta"
        })
        self.fields["first_name"].widget = widgets.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ad"
        })
        self.fields["last_name"].widget = widgets.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Soyad"
        })
        self.fields["password1"].widget = widgets.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Şifre"
        })
        self.fields["password2"].widget = widgets.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Şifreyi Onayla"
        })
        self.fields["captcha"].widget.attrs.update({
            "placeholder": "Doğrulama Kodu"
        })
        self.fields["email"].required = True
        

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exists():
            self.add_error("email"," bu email daha önce kullanılmış")

        return email    


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Eski Şifre"})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Yeni Şifre"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Yeni Şifreyi Onayla"})
        
class SifreSifirlamaTalepFormu(forms.Form):
    kimlik = forms.CharField(
        label="E-posta veya Kullanıcı Adı",
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E-posta veya kullanıcı adınızı girin'})
    )

class SifreSifirlamaDogrulamaFormu(forms.Form):
    kod = forms.CharField(label="Doğrulama Kodu", max_length=6, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kodu girin'}))
    yeni_sifre = forms.CharField(label="Yeni Şifre", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni şifrenizi girin'}))
    yeni_sifre_tekrar = forms.CharField(label="Yeni Şifre Tekrar", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Yeni şifreyi tekrar girin'}))