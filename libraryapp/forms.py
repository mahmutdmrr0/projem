from django import forms
from .models import Review, UserProfile
from django.contrib.auth.models import User
from .models import Complaint

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Yorumunuzu buraya yazın...'}),
            'rating': forms.Select(choices=Review._meta.get_field('rating').choices)
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
    
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Biyografi")
    profile_picture = forms.ImageField(required=False, label="Profil Fotoğrafı")

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Sorununuzu tarif edin', 'rows': 5}),
        }
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']
        
    bio = forms.CharField(widget=forms.Textarea, required=False, label="Biyografi")
    profile_picture = forms.ImageField(required=False, label="Profil Fotoğrafı")


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Konu'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Sorununuzu tarif edin', 'rows': 5}),
        }

