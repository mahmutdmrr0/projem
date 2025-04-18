from libraryapp import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('details/<str:id>/', views.details, name='details'),
    path('fetch-book-cover/',views.fetch_book_cover, name='fetch_book_cover'),
    path('category/',views.category, name='category'),
    path('category/<str:category_id>/', views.category_books, name='category_books'),
    path('search/', views.search, name='search'), 
    path('bookcase/', views.kitaplik, name='kitaplik'),
    path('kitap/ekle/<str:kitap_id>/', views.kitap_ekle, name='kitap_ekle'),
    path('kitap/sil/<int:id>/', views.delete_book, name='delete_book'),
    path('profilim/', views.profilim, name='profilim'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    path('friend-request/<int:request_id>/<str:action>/', views.manage_friend_request, name='manage_friend_request'),
    path('message/<str:username>/', views.send_message, name='send_message'),
    path('hakkında/', views.hakkında, name='hakkında'),
    path('sikayet-gonder/', views.sikayet_gonder, name='sikayet_gonder'),
    path('admin-bildirimler/', views.admin_bildirimler, name='admin_bildirimler'),
    path('sikayet-sil/<int:complaint_id>/', views.sikayet_sil, name='sikayet_sil'),
    path('get_notifications/', views.get_notifications, name='get_notifications'),
    path('relax/', views.relax_page, name='relax_page'),
    path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),
    path('şikayet-sayımsı/', views.şikayet_sayısı, name='şikayet_sayısı'),
]

