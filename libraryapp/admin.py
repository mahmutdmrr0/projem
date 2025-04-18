from django.contrib import admin
from .models import (
    Category, Book, BookLibrary, BookComment, PasswordResetCode, Review, RecommendedBook, UserProfile,
    FriendRequest, Friendship, Message, Complaint, Notification
)

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'translated_name', 'icon_class', 'color')
    search_fields = ('name', 'translated_name')
    list_filter = ('color',)
    ordering = ('translated_name',)

# Book Admin
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'google_books_id', 'publisher', 'published_date', 'price', 'average_rating')
    search_fields = ('title', 'google_books_id', 'publisher')
    list_filter = ('publisher', 'published_date', 'categories')
    ordering = ('title',)
    filter_horizontal = ('categories', 'related_books')
    readonly_fields = ('google_books_id',)
    list_per_page = 20

# BookLibrary Admin
class BookLibraryAdmin(admin.ModelAdmin):
    list_display = ('user', 'book_id', 'title', 'author', 'category', 'rating')
    search_fields = ('user__username', 'title', 'author', 'book_id')
    list_filter = ('user', 'category', 'rating')
    ordering = ('title',)
    list_per_page = 20

# BookComment Admin
class BookCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'content_preview', 'created_at')
    search_fields = ('user__username', 'book__title', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Yorum Önizlemesi'

# Review Admin
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'created_at', 'content_preview')
    search_fields = ('user__username', 'book__title', 'content')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'İnceleme Önizlemesi'

# RecommendedBook Admin
class RecommendedBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'user', 'sender', 'published_date', 'rating')
    search_fields = ('title', 'author', 'user__username', 'sender__username')
    list_filter = ('rating', 'published_date', 'user')
    ordering = ('title',)

# UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio_preview', 'profile_picture', 'last_login')
    search_fields = ('user__username', 'bio')
    list_filter = ('last_login',)
    ordering = ('user',)
    def bio_preview(self, obj):
        return obj.bio[:50] + ('...' if obj.bio and len(obj.bio) > 50 else '') if obj.bio else 'Yok'
    bio_preview.short_description = 'Biyografi Önizlemesi'

# FriendRequest Admin
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)
    actions = ['accept_requests', 'reject_requests']

    def accept_requests(self, request, queryset):
        for req in queryset.filter(status='pending'):
            req.status = 'accepted'
            req.save()
            Friendship.objects.get_or_create(user1=req.sender, user2=req.receiver)
        self.message_user(request, "Seçilen istekler kabul edildi.")
    accept_requests.short_description = "Seçilen istekleri kabul et"

    def reject_requests(self, request, queryset):
        queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, "Seçilen istekler reddedildi.")
    reject_requests.short_description = "Seçilen istekleri reddet"

# Friendship Admin
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

# Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content_preview', 'created_at', 'is_read')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
    def content_preview(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    content_preview.short_description = 'Mesaj Önizlemesi'

# Complaint Admin
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'created_at', 'is_resolved')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('subject', 'description', 'user__username')
    ordering = ('-created_at',)
    actions = ['mark_as_resolved', 'delete_selected_with_notifications']

    def mark_as_resolved(self, request, queryset):
        queryset.update(is_resolved=True)
        self.message_user(request, "Seçilen şikayetler çözüldü olarak işaretlendi.")
    mark_as_resolved.short_description = "Seçilenleri çözüldü olarak işaretle"

    def delete_selected_with_notifications(self, request, queryset):
        for complaint in queryset:
            Notification.objects.filter(
                message__contains=f"{complaint.user.username} bir şikayet gönderdi: {complaint.subject}"
            ).delete()
            complaint.delete()
        self.message_user(request, "Seçilen şikayetler ve ilgili bildirimler silindi.")
    delete_selected_with_notifications.short_description = "Seçilenleri ve bildirimlerini sil"

# Notification Admin
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('message', 'user__username')
    ordering = ('-created_at',)
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Seçilen bildirimler okundu olarak işaretlendi.")
    mark_as_read.short_description = "Seçilenleri okundu olarak işaretle"

# PasswordResetCode Admin
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')
    search_fields = ('user__username', 'code')
    list_filter = ('is_used', 'created_at', 'expires_at')
    ordering = ('-created_at',)

# Kayıtlar
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookLibrary, BookLibraryAdmin)
admin.site.register(BookComment, BookCommentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(RecommendedBook, RecommendedBookAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(PasswordResetCode, PasswordResetCodeAdmin)

# Admin Paneli Başlıkları
admin.site.site_header = "Kitaplık Yönetim Paneli"
admin.site.site_title = "Kitaplık Admin"
admin.site.index_title = "Admin Paneline Hoş Geldiniz"