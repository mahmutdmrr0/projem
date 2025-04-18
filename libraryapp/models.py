from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="İngilizce İsim")  # API’den gelen İngilizce isim
    translated_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Türkçe İsim", help_text="Türkçe kategori adı")
    icon_class = models.CharField(max_length=100, blank=True, null=True, verbose_name="İkon Sınıfı", help_text="FontAwesome icon class")
    color = models.CharField(max_length=7, blank=True, null=True, verbose_name="Renk", help_text="Hex renk kodu (örneğin, #FF4500)")

    def __str__(self):
        return self.translated_name or self.name
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

class Book(models.Model):
    google_books_id = models.CharField(max_length=100, unique=True, verbose_name="Google Kitap ID")
    title = models.CharField(max_length=255, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    page_count = models.IntegerField(blank=True, null=True, verbose_name="Sayfa Sayısı")
    cover_url = models.URLField(blank=True, null=True, verbose_name="Kapak URL")
    info_link = models.URLField(blank=True, null=True, verbose_name="Bilgi Linki")
    price = models.FloatField(blank=True, null=True, verbose_name="Fiyat")
    publisher = models.CharField(max_length=255, blank=True, null=True, verbose_name="Yayıncı")
    published_date = models.CharField(max_length=50, blank=True, null=True, verbose_name="Yayın Tarihi")
    preview_link = models.URLField(blank=True, null=True, verbose_name="Önizleme Linki")
    created_at = models.DateTimeField(default=timezone.now)  # Yeni alan
    categories = models.ManyToManyField(Category, related_name='books', verbose_name="Kategoriler")
    related_books = models.ManyToManyField('self', blank=True, verbose_name="İlgili Kitaplar")

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        """Kitabın ortalama puanını hesaplayan fonksiyon."""
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return total_rating / len(reviews)
        return 0

    class Meta:
        verbose_name = "Kitap"
        verbose_name_plural = "Kitaplar"

class BookLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book_id = models.CharField(max_length=150, verbose_name="Kitap ID")
    title = models.CharField(max_length=255, verbose_name="Başlık")
    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Yazar")
    image = models.URLField(blank=True, null=True, verbose_name="Resim URL")
    category = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kategori")
    rating = models.IntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name="Puan")
    info_link = models.URLField(blank=True, null=True, verbose_name="Bilgi Linki")
    
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

    class Meta:
        verbose_name = "Kitaplık"
        verbose_name_plural = "Kitaplıklar"

class BookComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(BookLibrary, on_delete=models.CASCADE, related_name='comments', verbose_name="Kitap")
    content = models.TextField(verbose_name="İçerik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return f"{self.user.username} - {self.book.title} Yorum"

    class Meta:
        verbose_name = "Kitap Yorumu"
        verbose_name_plural = "Kitap Yorumları"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Kitap")
    content = models.TextField(verbose_name="İçerik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    rating = models.IntegerField(default=1, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name="Puan")

    def __str__(self):
        return f"{self.user.username} - {self.book.title} Yorum"

    class Meta:
        verbose_name = "İnceleme"
        verbose_name_plural = "İncelemeler"
        constraints = [
            models.UniqueConstraint(fields=['user', 'book'], name='unique_user_book_review')
        ]

class RecommendedBook(models.Model):
    title = models.CharField(max_length=255, verbose_name="Başlık")
    author = models.CharField(max_length=255, verbose_name="Yazar")
    image = models.URLField(verbose_name="Resim URL")
    published_date = models.DateField(null=True, blank=True, verbose_name="Yayın Tarihi")
    info_link = models.URLField(verbose_name="Bilgi Linki")
    user = models.ForeignKey(User, related_name='recommended_books', on_delete=models.CASCADE, verbose_name="Kullanıcı")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, default=1, verbose_name="Gönderen")  # Öneriyi yapan
    rating = models.IntegerField(default=0, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name="Puan")  # Puan alanı

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Önerilen Kitap"
        verbose_name_plural = "Önerilen Kitaplar"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', verbose_name="Kullanıcı")
    bio = models.TextField(null=True, blank=True, verbose_name="Biyografi")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, verbose_name="Profil Resmi")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Son Giriş")

    def __str__(self):
        return f"{self.user.username}'ın Profili"

    class Meta:
        verbose_name = "Kullanıcı Profili"
        verbose_name_plural = "Kullanıcı Profilleri"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):  # Profil varsa kaydet
        instance.userprofile.save()

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests', verbose_name="Gönderen")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', verbose_name="Alıcı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Beklemede'), ('accepted', 'Kabul Edildi'), ('rejected', 'Reddedildi')],
        default='pending',
        verbose_name="Durum"
    )

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

    class Meta:
        verbose_name = "Arkadaşlık İsteği"
        verbose_name_plural = "Arkadaşlık İstekleri"
        unique_together = ('sender', 'receiver')  # Aynı kişiye birden fazla istek olmasın

class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships1', verbose_name="Kullanıcı 1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships2', verbose_name="Kullanıcı 2")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return f"{self.user1.username} & {self.user2.username}"

    class Meta:
        verbose_name = "Arkadaşlık"
        verbose_name_plural = "Arkadaşlıklar"
        unique_together = ('user1', 'user2')  # Aynı arkadaşlık tekrar olmasın

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="Gönderen")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name="Alıcı")
    content = models.TextField(verbose_name="İçerik")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu")
    
    class Meta:
        verbose_name = "Mesaj"
        verbose_name_plural = "Mesajlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints', verbose_name="Kullanıcı")
    subject = models.CharField(max_length=100, verbose_name="Konu")
    description = models.TextField(verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_resolved = models.BooleanField(default=False, verbose_name="Çözüldü mü")

    def __str__(self):
        return f"{self.user.username} - {self.subject}"
    
    class Meta:
        verbose_name = "Şikayet"
        verbose_name_plural = "Şikayetler"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Kullanıcı")
    message = models.CharField(max_length=255, verbose_name="Mesaj")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    is_read = models.BooleanField(default=False, verbose_name="Okundu mu")

    def __str__(self):
        return f"{self.user.username} - {self.message}"
    
    class Meta:
        verbose_name = "Bildirim"
        verbose_name_plural = "Bildirimler"

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_codes', verbose_name="Kullanıcı")
    code = models.CharField(max_length=50, unique=True, verbose_name="Kod")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    expires_at = models.DateTimeField(verbose_name="Son Kullanma Tarihi")
    is_used = models.BooleanField(default=False, verbose_name="Kullanıldı mı")

    def __str__(self):
        return f"{self.user.username} - {self.code}"

    class Meta:
        verbose_name = "Şifre Sıfırlama Kodu"
        verbose_name_plural = "Şifre Sıfırlama Kodları"
        ordering = ['-created_at']