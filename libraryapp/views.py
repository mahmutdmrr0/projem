from pyexpat.errors import messages
import re
from django.core.paginator import Paginator 
from django.shortcuts import get_object_or_404, redirect, render
import requests
from libraryapp.forms import ComplaintForm, ReviewForm, UserProfileForm
from libraryapp.models import Book, Category
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Review
from django.contrib import messages
from .models import Book
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone
from .models import UserProfile, BookLibrary, FriendRequest, Friendship, BookComment, RecommendedBook
from datetime import timedelta
from django.db.models import Q
from libraryapp.models import Message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ComplaintForm
from .models import Complaint, Notification
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, reverse
import json
import requests
import random 
from deep_translator import GoogleTranslator 
from django.conf import settings





ALLOWED_CATEGORIES = {
    "Fiction": {"translated_name": "Kurgu", "icon_class": "fas fa-book", "color": "#4682B4"},
    "Mystery": {"translated_name": "Polisiye", "icon_class": "fas fa-user-secret", "color": "#2F4F4F"},
    "Science": {"translated_name": "Bilim", "icon_class": "fas fa-flask", "color": "#32CD32"},
    "History": {"translated_name": "Tarih", "icon_class": "fas fa-scroll", "color": "#8B4513"},
    "Psychology": {"translated_name": "Psikoloji", "icon_class": "fas fa-brain", "color": "#32CD32"},
    "Computers": {"translated_name": "Bilgisayarlar", "icon_class": "fas fa-laptop", "color": "#00BFFF"},
    "Romance": {"translated_name": "Romantik", "icon_class": "fas fa-heart", "color": "#FF1493"},
    "Adventure": {"translated_name": "Macera", "icon_class": "fas fa-running", "color": "#FFD700"},
    "Science Fiction": {"translated_name": "Bilim Kurgu", "icon_class": "fas fa-rocket", "color": "#00BFFF"},
    "Fantasy": {"translated_name": "Fantastik", "icon_class": "fas fa-magic", "color": "#8A2BE2"},
    "Horror": {"translated_name": "Korku", "icon_class": "fas fa-ghost", "color": "#DC143C"},
    "Self-Help": {"translated_name": "Kişisel Gelişim", "icon_class": "fas fa-star", "color": "#FFD700"},
    "Juvenile": {"translated_name": "Çocuk", "icon_class": "fas fa-child", "color": "#FF6347"},
    "Art": {"translated_name": "Sanat", "icon_class": "fas fa-paint-brush", "color": "#D2691E"},
    "Travel": {"translated_name": "Seyahat", "icon_class": "fas fa-globe", "color": "#20B2AA"},
    "Sports": {"translated_name": "Spor", "icon_class": "fas fa-futbol", "color": "#FF4500"},
    "Nature": {"translated_name": "Doğa", "icon_class": "fas fa-tree", "color": "#228B22"},
    "Biography": {"translated_name": "Biyografi", "icon_class": "fas fa-pen", "color": "#8B4513"},
    "Education": {"translated_name": "Eğitim", "icon_class": "fas fa-chalkboard-teacher", "color": "#32CD32"},
    "Business": {"translated_name": "İş", "icon_class": "fas fa-briefcase", "color": "#FFD700"},
    "Economics": {"translated_name": "Ekonomi", "icon_class": "fas fa-chart-line", "color": "#FFD700"},
    "Political Science": {"translated_name": "Siyaset Bilimi", "icon_class": "fas fa-balance-scale", "color": "#2F4F4F"},
    "Social Science": {"translated_name": "Sosyal Bilimler", "icon_class": "fas fa-users", "color": "#32CD32"},
    "Law": {"translated_name": "Hukuk", "icon_class": "fas fa-gavel", "color": "#2F4F4F"},
    "Engineering": {"translated_name": "Mühendislik", "icon_class": "fas fa-tools", "color": "#FF4500"},
    "True Crime": {"translated_name": "Gerçek Suç", "icon_class": "fas fa-user-secret", "color": "#DC143C"},
    "Literary Criticism": {"translated_name": "Edebi Eleştiri", "icon_class": "fas fa-edit", "color": "#4682B4"},
    "Language Arts": {"translated_name": "Dil Sanatları", "icon_class": "fas fa-language", "color": "#00BFFF"},
    "Religion": {"translated_name": "Din", "icon_class": "fas fa-church", "color": "#8A2BE2"},
    "Antiques": {"translated_name": "Antika", "icon_class": "fas fa-vase", "color": "#D2691E"},
    "Young Adult": {"translated_name": "Genç Yetişkin", "icon_class": "fas fa-graduation-cap", "color": "#FF1493"},
    "Family": {"translated_name": "Aile", "icon_class": "fas fa-home", "color": "#FF69B4"},
    "Relationships": {"translated_name": "İlişkiler", "icon_class": "fas fa-heart", "color": "#FF69B4"},
    "Humor": {"translated_name": "Mizah", "icon_class": "fas fa-laugh", "color": "#FF4500"},
    "Performing Arts": {"translated_name": "Sahne Sanatları", "icon_class": "fas fa-theater-masks", "color": "#D2691E"},
    "Literary Collections": {"translated_name": "Edebi Koleksiyonlar", "icon_class": "fas fa-book", "color": "#4682B4"},
    "Body Mind Spirit": {"translated_name": "Beden Zihin Ruh", "icon_class": "fas fa-pray", "color": "#FFD700"},
    "Foreign Language": {"translated_name": "Yabancı Dil", "icon_class": "fas fa-language", "color": "#00BFFF"},
    "Civilization": {"translated_name": "Medeniyet", "icon_class": "fas fa-landmark", "color": "#D2691E"},
    "Reference": {"translated_name": "Referans", "icon_class": "fas fa-book-open", "color": "#2F4F4F"},
    "Investigators": {"translated_name": "Dedektifler", "icon_class": "fas fa-user-secret", "color": "#2F4F4F"},
    "Nonfiction": {"translated_name": "Kurgusal Olmayan", "icon_class": "fas fa-book", "color": "#4682B4"},
    "Health": {"translated_name": "Sağlık", "icon_class": "fas fa-heartbeat", "color": "#32CD32"},
    "Cooking": {"translated_name": "Yemek", "icon_class": "fas fa-utensils", "color": "#FF6347"},
    "Music": {"translated_name": "Müzik", "icon_class": "fas fa-music", "color": "#D2691E"},
    "Photography": {"translated_name": "Fotoğrafçılık", "icon_class": "fas fa-camera", "color": "#00BFFF"},
    "Poetry": {"translated_name": "Şiir", "icon_class": "fas fa-feather-alt", "color": "#8A2BE2"},
    "Crafts": {"translated_name": "El Sanatları", "icon_class": "fas fa-paint-roller", "color": "#FF4500"},
}


@csrf_exempt
@login_required
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"reply": "Selam kanka! 📚 Kitap istersen söyle, yoksa muhabbet edelim! 😎"})

            # Kategori haritası
            category_map = {ALLOWED_CATEGORIES[cat]["translated_name"].lower(): cat for cat in ALLOWED_CATEGORIES}
            lower_message = user_message.lower()

            # Kitapla ilgili mi kontrol et
            book_keywords = ["bana", "getir", "öner", "göster", "getirirmisin", "önerirmisin", "gösterirmisin"]
            is_book_request = any(keyword in lower_message for keyword in book_keywords)

            if is_book_request:
                category = None
                category_comment = ""
                book_query = None

                # Kategori kontrolü
                for cat_name_lower, cat_orig in category_map.items():
                    if cat_name_lower in lower_message:
                        category = cat_orig.lower()  # API için İngilizce
                        category_comment = f"{ALLOWED_CATEGORIES[cat_orig]['translated_name']} dedin, şahane tercih! 🎉 İşte önerim!"
                        break

                # Spesifik kitap kontrolü
                if not category:
                    # "bana ... kitabını" kalıbı
                    if "bana" in lower_message and "kitabını" in lower_message:
                        words = lower_message.split()
                        book_name_start = words.index("bana") + 1 if "bana" in words else -1
                        book_name_end = words.index("kitabını") if "kitabını" in words else len(words)
                        if book_name_start != -1:
                            book_query = " ".join(words[book_name_start:book_name_end]).strip()
                    else:
                        # "getir", "öner", "göster" sonrası kitap ismi
                        for keyword in ["getir", "öner", "göster", "getirirmisin", "önerirmisin", "gösterirmisin"]:
                            if keyword in lower_message:
                                book_query = lower_message.replace(keyword, "").strip()
                                break

                # Google Books API ile arama
                try:
                    if category:
                        start_index = random.randint(0, 30)
                        url = f"{settings.BASE_URL}?q=subject:{category}&langRestrict=tr&startIndex={start_index}&maxResults=10&key={settings.GOOGLE_BOOKS_API_KEY}"
                        response = requests.get(url, timeout=5)
                        response.raise_for_status()
                        books = response.json().get("items", [])

                        if not books:
                            url = f"{settings.BASE_URL}?q=subject:{category}&startIndex={start_index}&maxResults=10&key={settings.GOOGLE_BOOKS_API_KEY}"
                            response = requests.get(url, timeout=5)
                            books = response.json().get("items", [])

                        if books:
                            selected_book = random.choice(books)
                            book_id = selected_book["id"]
                            title = selected_book["volumeInfo"]["title"]
                            authors = ", ".join(selected_book["volumeInfo"].get("authors", ["Yazar bilinmiyor"]))
                            detail_url = reverse('details', args=[f"google_{book_id}"])
                            reply = f"{category_comment} '{title}' - {authors}. Kanka, buna bayılacaksın, detaylar için <a href='{detail_url}'>şuraya tıkla</a>!"
                        else:
                            reply = f"Kanka, {ALLOWED_CATEGORIES[category.upper()]['translated_name']} kategorisinde bi şey bulamadım! 😅 Başka ne deneyelim?"
                    elif book_query:
                        url = f"{settings.BASE_URL}?q={book_query}&langRestrict=tr&maxResults=1&key={settings.GOOGLE_BOOKS_API_KEY}"
                        response = requests.get(url, timeout=5)
                        response.raise_for_status()
                        books = response.json().get("items", [])

                        if not books:
                            url = f"{settings.BASE_URL}?q={book_query}&maxResults=1&key={settings.GOOGLE_BOOKS_API_KEY}"
                            response = requests.get(url, timeout=5)
                            books = response.json().get("items", [])

                        if books:
                            selected_book = books[0]
                            book_id = selected_book["id"]
                            title = selected_book["volumeInfo"]["title"]
                            authors = ", ".join(selected_book["volumeInfo"].get("authors", ["Yazar bilinmiyor"]))
                            detail_url = reverse('details', args=[f"google_{book_id}"])
                            reply = f"Kanka, '{book_query}' dedin, işte buldum: '{title}' - {authors}. Detaylar için <a href='{detail_url}'>şuraya tıkla</a>!"
                        else:
                            reply = f"Kanka, '{book_query}' diye bi kitap bulamadım! 😅 Başka ne öneriyim?"
                    else:
                        reply = "Kanka, neyi arayayım tam anlayamadım! 😅 Bi kitap ismi ya da kategori söylesen?"

                except Exception as e:
                    print(f"Error in book search: {str(e)}")  # Konsola log
                    reply = "Kanka, ufak bir karışıklık oldu, bi daha dene! 😅"
            else:
                # Normal muhabbet için handle_general_chat çağır
                try:
                    reply = handle_general_chat(user_message)
                except Exception as e:
                    print(f"Error in general chat: {str(e)}")  # Konsola log
                    reply = "Kanka, ufak bir karışıklık oldu, bi daha dene! 😅"

            return JsonResponse({"reply": reply})

        except Exception as e:
            print(f"General error: {str(e)}")  # Konsola log
            return JsonResponse({"reply": "Kanka, ufak bir karışıklık oldu, bi daha dene! 😅"})

    return JsonResponse({"error": "POST isteği lazım kanka! 😛"}, status=400)

def handle_general_chat(message):
    try:
        # Kullanıcının Türkçe mesajını İngilizce’ye çevir
        translator = GoogleTranslator(source='tr', target='en')
        eng_message = translator.translate(message)

        # Hugging Face API’ye istek için headers ve payload
        headers = {
            "Authorization": f"Bearer {settings.HUGGINGFACE_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": eng_message,
            "parameters": {
                "max_length": 100,
                "min_length": 10,
                "temperature": 0.9
            }
        }

        # API’ye POST isteği gönder
        response = requests.post(settings.API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()

        # Yanıtı al
        result = response.json()
        if isinstance(result, list) and result:
            bot_reply_eng = result[0].get("generated_text", "Kanka, bir şey diyemedim! 😅")
        else:
            bot_reply_eng = result.get("generated_text", "Kanka, bir şey diyemedim! 😅")

        # Botun İngilizce yanıtını Türkçe’ye çevir
        translator = GoogleTranslator(source='en', target='tr')
        bot_reply_tr = translator.translate(bot_reply_eng)

        # Kullanıcıya Türkçe yanıt dön
        return bot_reply_tr

    except requests.RequestException as e:
        print(f"Error in Hugging Face API: {str(e)}")  # Konsola log
        return "Kanka, ufak bir karışıklık oldu, bi daha dene! 😅"
    except Exception as e:
        print(f"General error in handle_general_chat: {str(e)}")  # Konsola log
        return "Kanka, ufak bir karışıklık oldu, bi daha dene! 😅"

def chatbot_page(request):
    categories = Category.objects.filter(name__in=ALLOWED_CATEGORIES.keys())
    if not categories.exists():
        for cat_name, attrs in ALLOWED_CATEGORIES.items():
            Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    "translated_name": attrs["translated_name"],
                    "icon_class": attrs["icon_class"],
                    "color": attrs["color"]
                }
            )
        categories = Category.objects.filter(name__in=ALLOWED_CATEGORIES.keys())
    return render(request, 'libraryapp/chatbot.html', {'categories': categories})


def relax_page(request):
    return render(request,'libraryapp/relax.html')

@login_required
def get_notifications(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Okunmamış mesajlar
        unread_messages_qs = Message.objects.filter(receiver=request.user, is_read=False).order_by('-created_at')
        # Mesaj detayları (sohbet kısmı için)
        notifications = [
            {
                'sender': message.sender.username,
                'content': message.content,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
            for message in unread_messages_qs
        ]
        # Okunmamış mesaj sayısı (navbar badge için)
        unread_messages = unread_messages_qs.count()
        # Bekleyen arkadaşlık istekleri (navbar için, şu an kullanmıyorsun ama dursun)
        pending_friend_requests = FriendRequest.objects.filter(receiver=request.user, status='pending').count()

        data = {
            'notifications': notifications,              # Sohbet kısmı için mesaj detayları
            'unread_messages': unread_messages,          # Navbar badge için mesaj sayısı
            'pending_friend_requests': pending_friend_requests,  # İleride lazım olursa
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def send_message(request, username):
    receiver = get_object_or_404(User, username=username)

    if request.user == receiver:
        return render(request, 'send_message.html', {
            'receiver': receiver,
            'all_messages': [],
            'error': "Kendinize mesaj gönderemezsiniz."
        })

    # Mesajları GET ile çek
    sent_messages = Message.objects.filter(sender=request.user, receiver=receiver)
    received_messages = Message.objects.filter(sender=receiver, receiver=request.user)
    all_messages = (sent_messages | received_messages).order_by('created_at')

    # Gelen mesajları okundu olarak işaretle
    received_messages.filter(is_read=False).update(is_read=True)

    if request.method == 'POST':
        # Sadece AJAX isteği kabul edilecek
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            content = request.POST.get('content')
            if content:
                message = Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    content=content
                )
                one_hour_ago = timezone.now() - timedelta(hours=1)
                Message.objects.filter(created_at__lt=one_hour_ago).delete()
                # Zamanı Türkiye saatine çevir
                local_time = timezone.localtime(message.created_at)
                return JsonResponse({
                    'success': True,
                    'message': {
                        'sender': message.sender.username,
                        'content': message.content,
                        'created_at': local_time.strftime('%d.%m.%Y %H:%M')
                    }
                })
            return JsonResponse({'success': False, 'error': 'Mesaj içeriği boş olamaz.'})
        return JsonResponse({'success': False, 'error': 'Bu işlem yalnızca AJAX ile yapılabilir.'})

    # Tüm mesajların zamanını yerel saate çevir
    for msg in all_messages:
        msg.local_time = timezone.localtime(msg.created_at)

    return render(request, 'send_message.html', {
        'receiver': receiver,
        'all_messages': all_messages,
    })

@login_required
def profilim(request):
    user = request.user
    
    # Kullanıcı profili yoksa oluştur
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    # Profil güncelleme formu
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profiliniz güncellendi!")
            return redirect('profilim')
        else:
            messages.error(request, "Profil güncellenirken bir hata oluştu.")
    else:
        form = UserProfileForm(instance=profile)

    # Toplam kullanıcı sayısı
    total_users = User.objects.count()

    # Aktif kullanıcılar (oturumu açık olanlar)
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions if session.get_decoded().get('_auth_user_id')]
    active_users = User.objects.filter(id__in=user_ids)

    # Hata ayıklama: Oturum açık kullanıcıları kontrol et
    all_users = User.objects.all()[:5]  # İlk 5 kullanıcıyı al
    for u in all_users:
        print(f"Kullanıcı: {u.username}, Last Login: {u.last_login}")

    # Arama ve kullanıcı filtreleme
    search_query = request.GET.get('q', '')
    if search_query:
        users = User.objects.filter(username__icontains=search_query)
    else:
        users = active_users

    # Her kullanıcı için aktiflik durumunu belirle
    user_status = {u.id: u.id in user_ids for u in users}  # Aktifse True, pasifse False

    # Aktif kullanıcılar için sayfalama
    users_paginator = Paginator(users, 5)
    users_page_number = request.GET.get('page_active', 1)
    users_page = users_paginator.get_page(users_page_number)

    # Kullanıcının kitaplığı
    user_books = BookLibrary.objects.filter(user=user)

    # Gelen arkadaşlık istekleri
    friend_requests = FriendRequest.objects.filter(receiver=user, status='pending')

    # Arkadaşlar
    friendships = Friendship.objects.filter(user1=user) | Friendship.objects.filter(user2=user)
    friends = [f.user2 if f.user1 == user else f.user1 for f in friendships]

    # Önerilen kitaplar için sayfalama
    recommended_to_me = RecommendedBook.objects.filter(user=user)
    rec_paginator = Paginator(recommended_to_me, 3)
    rec_page_number = request.GET.get('page', 1)
    recommended_books_page = rec_paginator.get_page(rec_page_number)

    # Hata ayıklama
    print(f"Aktif kullanıcı sayısı: {active_users.count()}")
    print(f"Filtrelenmiş kullanıcı sayısı: {users.count()}")
    for u in users:
        print(f"Arama sonucu kullanıcı: {u.username}, Aktif mi: {user_status[u.id]}")

    context = {
        'user': user,
        'form': form,
        'total_users': total_users,
        'active_users': active_users,
        'active_users_count': active_users.count(),
        'users_page': users_page,
        'search_query': search_query,
        'user_books': user_books,
        'friend_requests': friend_requests,
        'friends': friends,
        'recommended_to_me': recommended_books_page,
        'user_status': user_status,  # Aktif/pasif durumları context'e eklendi
    }
    return render(request, 'profilim.html', context)

@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    user_books = BookLibrary.objects.filter(user=profile_user)
    
    
    # Sayfalama işlemi
    paginator = Paginator(user_books, 4)  # Sayfada 4 kitap göster
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Arkadaşlık kontrolü
    is_friend = Friendship.objects.filter(
        Q(user1=request.user, user2=profile_user) | 
        Q(user1=profile_user, user2=request.user)
    ).exists()
    
    # Kullanıcının kendi kitaplığı
    my_books = BookLibrary.objects.filter(user=request.user)
    
    # Önerilen kitaplar
    recommended_books = RecommendedBook.objects.filter(user=profile_user)
    
    if request.method == 'POST':
        if 'send_friend_request' in request.POST:
            if request.user == profile_user:
                messages.error(request, "Kendinize arkadaşlık isteği gönderemezsiniz!")
            elif FriendRequest.objects.filter(sender=request.user, receiver=profile_user).exists():
                messages.error(request, f"{profile_user.username}'a zaten bir istek gönderdiniz!")
            else:
                FriendRequest.objects.create(sender=request.user, receiver=profile_user)
                messages.success(request, f"{profile_user.username}'a arkadaş isteği gönderildi.")
            return redirect('user_profile', username=username)
        
        elif 'submit_review' in request.POST:
            book_id = request.POST.get('book_id')
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            book = get_object_or_404(BookLibrary, id=book_id)
            
            if not is_friend:
                messages.error(request, "Sadece arkadaşların kitaplarını değerlendirebilirsiniz!")
            else:
                updated = False
                if rating:
                    try:
                        rating = int(rating)
                        if 1 <= rating <= 5:
                            book.rating = rating
                            book.save()
                            messages.success(request, f"{book.title} puanlandı!")
                            updated = True
                        else:
                            messages.error(request, "Puan 1-5 arasında olmalı!")
                    except ValueError:
                        messages.error(request, "Geçersiz puan değeri!")
                if comment:
                    BookComment.objects.create(user=request.user, book=book, content=comment)
                    messages.success(request, f"{book.title}'a yorum eklendi!")
                    updated = True
                if not updated:
                    messages.error(request, "Puan veya yorumdan en az biri dolu olmalı!")
            return redirect('user_profile', username=username)
        
        elif 'recommend_my_book' in request.POST:
            book_id = request.POST.get('book_id')
            if book_id:
                book = get_object_or_404(BookLibrary, id=book_id, user=request.user)
                RecommendedBook.objects.create(
                    user=profile_user,
                    title=book.title,
                    author=book.author,
                    image=book.image if book.image else '',
                    info_link=book.info_link if book.info_link else '',
                    rating=0
                )
                messages.success(request, f"{profile_user.username}'a {book.title} önerildi!")
            else:
                messages.error(request, "Lütfen bir kitap seçin!")
            return redirect('user_profile', username=username)

    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'is_friend': is_friend,
        'my_books': my_books,
        'recommended_books': recommended_books,
    })

@login_required
def manage_friend_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
    if action == 'accept':
        friend_request.status = 'accepted'
        friend_request.save()
        Friendship.objects.create(user1=friend_request.sender, user2=friend_request.receiver)
        messages.success(request, f"{friend_request.sender.username} ile arkadaş oldunuz!")
    elif action == 'reject':
        friend_request.status = 'rejected'
        friend_request.save()
        messages.info(request, f"{friend_request.sender.username}'ın isteği reddedildi.")
    return redirect('profilim')


@login_required
def kitaplik(request):
    kitaplar = BookLibrary.objects.filter(user=request.user)
    
    category_count = {}
    for kitap in kitaplar:
        category_count[kitap.category] = category_count.get(kitap.category, 0) + 1

    return render(request, 'libraryapp/kitaplik.html', {'kitaplar': kitaplar, 'category_count': category_count})


@login_required
def kitap_ekle(request, kitap_id):
    if kitap_id.startswith('gutendex_'):
        book_id_raw = kitap_id.replace('gutendex_', '')
        url = f"https://gutendex.com/books/{book_id_raw}/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            book_data = response.json()
            formats = book_data.get('formats', {})

            authors = book_data.get('authors', [])
            author_name = authors[0].get('name', 'Yazar Bilgisi Bulunamadı') if authors else 'Yazar Bilgisi Bulunamadı'

            new_book = BookLibrary(
                user=request.user,
                book_id=kitap_id,
                title=book_data.get('title', 'Başlık Bulunamadı'),
                author=author_name,
                image=formats.get('image/jpeg', ''),
                category=', '.join(book_data.get('subjects', ['Bilinmiyor'])),
            )
            new_book.save()
            messages.success(request, 'Kitap başarıyla eklendi!')
            return redirect('kitaplik')
        except requests.RequestException as e:
            print(f"Gutendex API hatası: {e} - Status Code: {response.status_code if 'response' in locals() else 'Yok'}")
            messages.error(request, 'Kitap verileri alınırken bir hata oluştu!')
            return redirect('kitaplik')
    else:
        clean_kitap_id = kitap_id.replace('google_', '') if kitap_id.startswith('google_') else kitap_id
        url = f"{settings.BASE_URL}/{clean_kitap_id}?key={settings.GOOGLE_BOOKS_API_KEY}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            book_data = response.json()
            volume_info = book_data.get('volumeInfo', {})

            authors = volume_info.get('authors', ['Yazar Bilgisi Bulunamadı'])
            author_name = authors[0] if authors else 'Yazar Bilgisi Bulunamadı'

            new_book = BookLibrary(
                user=request.user,
                book_id=kitap_id,
                title=volume_info.get('title', 'Başlık Bulunamadı'),
                author=author_name,
                image=volume_info.get('imageLinks', {}).get('thumbnail', ''),
                category=', '.join(volume_info.get('categories', ['Bilinmiyor'])),
            )
            new_book.save()
            messages.success(request, 'Kitap başarıyla eklendi!')
            return redirect('kitaplik')
        except requests.RequestException as e:
            print(f"Google Books API hatası: {e} - Status Code: {response.status_code if 'response' in locals() else 'Yok'}")
            messages.error(request, 'Kitap verileri alınırken bir hata oluştu!')
            return redirect('kitaplik')

@login_required
def delete_book(request, id):
    if request.method == "POST":
        try:
            # Sadece kullanıcının kendi kitabını silmesine izin ver
            kitap = get_object_or_404(BookLibrary, id=id, user=request.user)
            kitap.delete()
            return JsonResponse({"success": True, "message": "Kitap başarıyla silindi!"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Geçersiz istek!"}, status=400)



def get_recommended_books(user):
    """
    Kullanıcının kitaplığına göre benzer kitaplar önerir.
    Aynı kitapları önermemek için kullanıcının mevcut kitaplarını hariç tutar.
    """
    recommended_books = []
    if not user.is_authenticated:
        return recommended_books

    # Kullanıcının kitaplığını al
    user_books = BookLibrary.objects.filter(user=user)
    user_book_ids = {book.book_id for book in user_books}  # Kullanıcının kitaplarının ID'leri

    # Her bir kitap için öneri getir
    for book in user_books:
        # Kitap başlığı ve yazarı ile arama yap
        query = f"{book.title} inauthor:{book.author}" if book.author else book.title
        url = f"{settings.BASE_URL}?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}&maxResults=9"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Hata varsa exception fırlat
            books_data = response.json()

            for item in books_data.get('items', []):
                book_id = item['id']
                # Eğer kitap zaten kullanıcının kitaplığındaysa, önerilere ekleme
                if book_id in user_book_ids:
                    continue

                book_data = {
                    'id': book_id,
                    'title': item['volumeInfo'].get('title', 'Başlık Bulunamadı'),
                    'author': item['volumeInfo'].get('authors', ['Yazar Bilgisi Bulunamadı'])[0],
                    'image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                    'publishedDate': item['volumeInfo'].get('publishedDate', 'Tarih Bilgisi Bulunamadı'),
                    'infoLink': item['volumeInfo'].get('infoLink', '#'),
                }
                recommended_books.append(book_data)
                # Her kitap için maksimum 3 öneri alalım (toplam öneriyi sınırlamak için)
                if len(recommended_books) >= 3 * len(user_books):
                    break
            if len(recommended_books) >= 9:  # Toplam 9 öneriyle sınırlı
                break

        except requests.RequestException as e:
            print(f"Google Books API hatası: {e}")
            continue

    return recommended_books

def index(request):
    # Kullanıcının kitaplığı
    if request.user.is_authenticated:
        user_books = BookLibrary.objects.filter(user=request.user)
    else:
        user_books = []

    # Önerilen kitaplar
    recommended_books = get_recommended_books(request.user)
    
    # Popüler Kitaplar
    popular_books = []
    popular_url = f"{settings.BASE_URL}?q=subject:fiction&key={settings.GOOGLE_BOOKS_API_KEY}&orderBy=relevance&maxResults=9"
    try:
        popular_response = requests.get(popular_url, timeout=5)
        popular_response.raise_for_status()
        popular_books_data = popular_response.json()
        for item in popular_books_data.get('items', []):
            book_data = {
                'id': item['id'],
                'title': item['volumeInfo'].get('title', 'Başlık Bulunamadı'),
                'author': item['volumeInfo'].get('authors', ['Yazar Bilgisi Bulunamadı'])[0],
                'image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'publishedDate': item['volumeInfo'].get('publishedDate', 'Tarih Bilgisi Bulunamadı'),
                'infoLink': item['volumeInfo'].get('infoLink', '#'),
            }
            popular_books.append(book_data)
    except requests.RequestException as e:
        print(f"Popüler kitaplar alınırken hata: {e}")

    # En Yüksek Puanlı Kitaplar
    if request.user.is_authenticated:
        top_rated_books = BookLibrary.objects.filter(user=request.user).order_by('-rating')[:9]
        top_rated_books_data = []
        for book in top_rated_books:
            book_data = {
                'id': book.book_id,
                'title': book.title,
                'author': book.author,
                'image': book.image,
                'rating': book.rating,
                'infoLink': f"/book/{book.book_id}/"
            }
            top_rated_books_data.append(book_data)
        grouped_top_rated_books = [top_rated_books_data[i:i+3] for i in range(0, len(top_rated_books_data), 3)]
    else:
        grouped_top_rated_books = []

    # Ücretsiz Kitaplar (Romanlar ve Text/Plain Garantisi)
    free_books = []
    free_url = "https://gutendex.com/books/?languages=en&limit=32&subjects=fiction"
    try:
        free_response = requests.get(free_url, timeout=5)
        free_response.raise_for_status()
        free_books_data = free_response.json()

        for item in free_books_data.get('results', []):
            formats = item.get('formats', {})
            text_plain_url = next((url for mime, url in formats.items() if 'text/plain' in mime), None)
            if text_plain_url:
                authors = item.get('authors', [])
                author_name = authors[0].get('name', 'Yazar Bilgisi Bulunamadı') if authors else 'Yazar Bilgisi Bulunamadı'
                free_book_data = {
                    'id': f"gutendex_{item['id']}",
                    'title': item['title'],
                    'author': author_name,
                    'image': formats.get('image/jpeg', ''),
                    'description': '',
                    'downloadLink': text_plain_url,
                }
                free_books.append(free_book_data)
                if len(free_books) >= 9:
                    break
    except requests.RequestException as e:
        print(f"Gutendex API hatası: {e}")

    # Eğer 9 roman bulunmazsa, sabit klasik romanları ekle
    if len(free_books) < 9:
        sabit_romanlar = [
            {'id': 'gutendex_1342', 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'image': 'https://www.gutenberg.org/cache/epub/1342/pg1342.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/1342/1342-0.txt'},
            {'id': 'gutendex_84', 'title': 'Frankenstein', 'author': 'Mary Shelley', 'image': 'https://www.gutenberg.org/cache/epub/84/pg84.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/84/84-0.txt'},
            {'id': 'gutendex_11', 'title': 'Alice’s Adventures in Wonderland', 'author': 'Lewis Carroll', 'image': 'https://www.gutenberg.org/cache/epub/11/pg11.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/11/11-0.txt'},
            {'id': 'gutendex_1661', 'title': 'The Adventures of Sherlock Holmes', 'author': 'Arthur Conan Doyle', 'image': 'https://www.gutenberg.org/cache/epub/1661/pg1661.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/1661/1661-0.txt'},
            {'id': 'gutendex_174', 'title': 'The Picture of Dorian Gray', 'author': 'Oscar Wilde', 'image': 'https://www.gutenberg.org/cache/epub/174/pg174.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/174/174-0.txt'},
            {'id': 'gutendex_5200', 'title': 'Metamorphosis', 'author': 'Franz Kafka', 'image': 'https://www.gutenberg.org/cache/epub/5200/pg5200.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/5200/5200-0.txt'},
            {'id': 'gutendex_1080', 'title': 'A Modest Proposal', 'author': 'Jonathan Swift', 'image': 'https://www.gutenberg.org/cache/epub/1080/pg1080.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/1080/1080-0.txt'},
            {'id': 'gutendex_1952', 'title': 'The Yellow Wallpaper', 'author': 'Charlotte Perkins Gilman', 'image': 'https://www.gutenberg.org/cache/epub/1952/pg1952.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/1952/1952-0.txt'},
            {'id': 'gutendex_98', 'title': 'A Tale of Two Cities', 'author': 'Charles Dickens', 'image': 'https://www.gutenberg.org/cache/epub/98/pg98.cover.medium.jpg', 'downloadLink': 'https://www.gutenberg.org/files/98/98-0.txt'},
        ]
        free_books.extend(sabit_romanlar[:9 - len(free_books)])

    # Gruplama
    grouped_free_books = [free_books[i:i+3] for i in range(0, min(len(free_books), 9), 3)]
    grouped_recommended_books = [recommended_books[i:i+3] for i in range(0, len(recommended_books), 3)]
    grouped_popular_books = [popular_books[i:i+3] for i in range(0, len(popular_books), 3)]

    return render(request, 'base.html', {
        'grouped_recommended_books': grouped_recommended_books,
        'grouped_popular_books': grouped_popular_books,
        'grouped_top_rated_books': grouped_top_rated_books,
        'grouped_free_books': grouped_free_books,
    })



@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return render(request, 'libraryapp/search.html', {'results': [], 'query': query})

    results = []

    # Google Books API
    try:
        google_url = f"{settings.BASE_URL}?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}&maxResults=5"
        google_response = requests.get(google_url)
        google_response.raise_for_status()
        google_data = google_response.json()

        for item in google_data.get('items', []):
            book_data = {
                'id': item['id'],
                'title': item['volumeInfo'].get('title', 'Başlık Bulunamadı'),
                'author': item['volumeInfo'].get('authors', ['Yazar Bilgisi Bulunamadı'])[0],
                'image': item['volumeInfo'].get('imageLinks', {}).get('thumbnail', ''),
                'publishedDate': item['volumeInfo'].get('publishedDate', 'Tarih Bilgisi Bulunamadı'),
                'infoLink': item['volumeInfo'].get('infoLink', '#'),
                'source': 'google',
                'description': item['volumeInfo'].get('description', 'Açıklama Yok'),
                'downloadLink': None,  # Google Books’ta tam metin yok
            }
            results.append(book_data)
    except requests.RequestException as e:
        print(f"Google Books API hatası: {e}")

    # Gutendex API
    try:
        gutendex_url = f"https://gutendex.com/books/?search={query}&languages=en&limit=5"
        gutendex_response = requests.get(gutendex_url)
        gutendex_response.raise_for_status()
        gutendex_data = gutendex_response.json()

        for item in gutendex_data.get('results', []):
            formats = item.get('formats', {})
            text_plain_url = next((url for mime, url in formats.items() if 'text/plain' in mime), None)
            if text_plain_url:
                authors = item.get('authors', [])
                author_name = authors[0].get('name', 'Yazar Bilgisi Bulunamadı') if authors else 'Yazar Bilgisi Bulunamadı'
                book_data = {
                    'id': f"gutendex_{item['id']}",
                    'title': item['title'],
                    'author': author_name,
                    'image': formats.get('image/jpeg', ''),
                    'publishedDate': '',
                    'infoLink': f"https://www.gutenberg.org/ebooks/{item['id']}",
                    'source': 'gutendex',
                    'description': '',
                    'downloadLink': text_plain_url,  # Metin linkini tutuyoruz ama göstermiyoruz
                }
                results.append(book_data)
    except requests.RequestException as e:
        print(f"Gutendex API hatası: {e}")

    # Alfabetik sıralama
    results.sort(key=lambda x: x['title'].lower())

    return render(request, 'libraryapp/search.html', {
        'results': results,
        'query': query,
    })

@login_required
def book_list(request, category_id=None):
    # Kategori ID'sini alalım
    category = None
    if category_id:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404("Kategori bulunamadı")

    # API sorgusu için kategori adını ya da varsayılan "kitap" kelimesini kullanalım
    query = "kitap"  # Varsayılan sorgu
    if category:
        query = category.name  # Kategoriye göre sorgu

    # Google Books API'den veri çekelim
    api_key = ""  # API key’in
    books = []

    # Toplam 100 kitap çekmek için 3 istek
    for start_index in [0, 40, 80]:
        max_results = 40 if start_index < 80 else 20  # Son istekte 20 çekiyoruz (100’e tamamlamak için)
        url = f"{settings.BASE_URL}?q={query}&key={settings.GOOGLE_BOOKS_API_KEY}&langRestrict=tr&maxResults={max_results}&startIndex={start_index}"
        response = requests.get(url)
        
        if response.status_code == 200:
            books_data = response.json()
            books.extend(books_data.get('items', []))
        else:
            print(f"API Hatası: {response.status_code} - startIndex={start_index}")
            messages.error(request, "Bazı kitap verileri alınamadı!")
            break  # Hata olursa duruyoruz

    # API’den gelen verileri işleyelim
    filtered_books = []
    for book in books:
        google_books_id = book.get('id')
        volume_info = book.get('volumeInfo', {})
        sale_info = book.get('saleInfo', {})

        book_data = {
            'google_books_id': f"google_{google_books_id}",  # details ile uyumlu ID
            'title': volume_info.get('title', 'Başlık Bulunamadı'),
            'description': volume_info.get('description', ''),
            'page_count': volume_info.get('pageCount', 0),
            'cover_url': volume_info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150'),
            'info_link': volume_info.get('infoLink', ''),
            'price': sale_info.get('listPrice', {}).get('amount', None),
            'publisher': volume_info.get('publisher', None),
            'published_date': volume_info.get('publishedDate', None),
        }

        # Eksik veri kontrolü
        if not book_data['title'] or not book_data['cover_url'] or not book_data['info_link']:
            continue  # Eksik verili kitapları atla

        # Fiyat yoksa varsayılan bir değer atayalım
        if not book_data['price']:
            book_data['price'] = 'Fiyat bilgisi yok'

        filtered_books.append(book_data)

    # Sıralama: Başlığa göre alfabetik
    filtered_books.sort(key=lambda x: x['title'].lower())

    # Sayfalama: Her sayfada 6 kitap
    paginator = Paginator(filtered_books, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'libraryapp/list.html', {
        'page_obj': page_obj,
        'category': category,
    })


def fetch_book_cover(book_title):
    url = f'https://openlibrary.org/search.json?title={book_title}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['docs']:
            first_book = data['docs'][0]
            cover_id = first_book.get('cover_i')
            if cover_id:
                return f'http://covers.openlibrary.org/b/id/{cover_id}-L.jpg'
    return None

@login_required
def details(request, id):
    book_data = {}

    expiry_time = timezone.now() - timedelta(hours=24)
    Book.objects.filter(created_at__lt=expiry_time).delete()

    clean_id = id
    if id.startswith('google_'):
        clean_id = id.replace('google_', '')
    elif id.startswith('gutendex_'):
        clean_id = id.replace('gutendex_', '')

    if request.method == 'POST':
        try:
            book_instance, created = Book.objects.get_or_create(
                google_books_id=id,
                defaults={'title': 'Bilinmeyen Kitap', 'created_at': timezone.now()}
            )

            if 'delete' in request.POST:
                review_id = request.POST.get('review_id')
                review = Review.objects.get(id=review_id, user=request.user, book=book_instance)
                review.delete()
                messages.success(request, 'Yorum başarıyla silindi!')
                return redirect('details', id=id)

            elif 'update' in request.POST:
                review_id = request.POST.get('review_id')
                review = Review.objects.get(id=review_id, user=request.user, book=book_instance)
                content = request.POST.get('content')
                rating = request.POST.get('rating')
                if content:
                    review.content = content
                if rating:
                    review.rating = int(rating)
                review.save()
                messages.success(request, 'Yorum başarıyla güncellendi!')
                return redirect('details', id=id)

            else:
                content = request.POST.get('content')
                rating = request.POST.get('rating')
                if content or rating:
                    review, created = Review.objects.get_or_create(
                        user=request.user,
                        book=book_instance,
                        defaults={'content': content or '', 'rating': int(rating or 1)}
                    )
                    if not created:
                        if content:
                            review.content = content
                        if rating:
                            review.rating = int(rating)
                        review.save()
                    messages.success(request, 'Yorum ve/veya puan başarıyla eklendi!')
                return redirect('details', id=id)

        except Review.DoesNotExist:
            messages.error(request, 'Yorum bulunamadı!')
            return redirect('details', id=id)
        except ValueError:
            messages.error(request, 'Geçersiz puan değeri!')
            return redirect('details', id=id)

    if id.startswith('gutendex_'):
        url = f"https://gutendex.com/books/{clean_id}/"
        response = requests.get(url)
        if response.status_code != 200:
            messages.error(request, 'Kitap verileri alınırken bir hata oluştu!')
            return redirect('index')
        
        book_data_raw = response.json()
        formats = book_data_raw.get('formats', {})
        text_url = next((url for mime, url in formats.items() if 'text/plain' in mime), None)

        authors = book_data_raw.get('authors', [])
        author_name = authors[0].get('name', 'Yazar Bilgisi Bulunamadı') if authors else 'Yazar Bilgisi Bulunamadı'

        book_data = {
            'id': id,
            'volumeInfo': {
                'title': book_data_raw.get('title', 'Başlık Bulunamadı'),
                'authors': [author_name],
                'imageLinks': {'thumbnail': formats.get('image/jpeg', '')},
                'categories': book_data_raw.get('subjects', ['Bilinmiyor']),
                'infoLink': f"https://www.gutenberg.org/ebooks/{clean_id}",
                'description': book_data_raw.get('description', 'Açıklama Bulunamadı'),
            },
            'previewText': None,
            'extendedText': None,
            'sourceLink': f"https://www.gutenberg.org/ebooks/{clean_id}",
        }

        if text_url:
            try:
                text_response = requests.get(text_url)
                if text_response.status_code == 200:
                    full_text = text_response.text
                    book_data['previewText'] = full_text[:500] + "..." if len(full_text) > 500 else full_text
                    book_data['extendedText'] = full_text[:2000] + "..." if len(full_text) > 2000 else full_text
            except requests.RequestException as e:
                print(f"Metin çekilemedi: {e}")

        # Book modelini güncelle
        book_instance, created = Book.objects.get_or_create(
            google_books_id=id,
            defaults={
                'title': book_data['volumeInfo']['title'],
                'cover_url': book_data['volumeInfo']['imageLinks']['thumbnail'],
                'info_link': book_data['volumeInfo']['infoLink'],
                'publisher': 'Project Gutenberg',
                'created_at': timezone.now(),
            }
        )
        if not created:
            book_instance.title = book_data['volumeInfo']['title']
            book_instance.cover_url = book_data['volumeInfo']['imageLinks']['thumbnail']
            book_instance.info_link = book_data['volumeInfo']['infoLink']
            book_instance.created_at = timezone.now()
            book_instance.save()

    else:
        url = f"https://www.googleapis.com/books/v1/volumes/{clean_id}"
        response = requests.get(url)
        if response.status_code != 200:
            messages.error(request, 'Kitap verileri alınırken bir hata oluştu!')
            return redirect('index')
        
        book_data_raw = response.json()
        volume_info = book_data_raw.get('volumeInfo', {})
        book_data = {
            'id': id,
            'volumeInfo': {
                'title': volume_info.get('title', 'Başlık Bulunamadı'),
                'authors': volume_info.get('authors', ['Yazar Bilgisi Bulunamadı']),
                'imageLinks': {'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', '')},
                'categories': volume_info.get('categories', ['Bilinmiyor']),
                'infoLink': volume_info.get('infoLink', '#'),
                'description': volume_info.get('description', 'Açıklama Bulunamadı'),
            },
        }

        book_instance, created = Book.objects.get_or_create(
            google_books_id=id,
            defaults={
                'title': book_data['volumeInfo']['title'],
                'description': book_data['volumeInfo']['description'],
                'cover_url': book_data['volumeInfo']['imageLinks']['thumbnail'],
                'info_link': book_data['volumeInfo']['infoLink'],
                'publisher': volume_info.get('publisher', ''),
                'published_date': volume_info.get('publishedDate', ''),
                'created_at': timezone.now(),
            }
        )
        if not created:
            book_instance.title = book_data['volumeInfo']['title']
            book_instance.description = book_data['volumeInfo']['description']
            book_instance.cover_url = book_data['volumeInfo']['imageLinks']['thumbnail']
            book_instance.info_link = book_data['volumeInfo']['infoLink']
            book_instance.publisher = volume_info.get('publisher', '')
            book_instance.published_date = volume_info.get('publishedDate', '')
            book_instance.created_at = timezone.now()
            book_instance.save()

    reviews = Review.objects.filter(book=book_instance).order_by('-created_at')
    user_review = Review.objects.filter(book=book_instance, user=request.user).first()

    return render(request, 'libraryapp/details.html', {
        'book': book_data,
        'reviews': reviews,
        'user_review': user_review,
    })
@login_required
def category(request):

    categories = Category.objects.filter(name__in=ALLOWED_CATEGORIES.keys())

    for cat_name, attrs in ALLOWED_CATEGORIES.items():
        Category.objects.get_or_create(
            name=cat_name,
            defaults={
                "translated_name": attrs["translated_name"],
                "icon_class": attrs["icon_class"],
                "color": attrs["color"]
            }
        )
    
    categories = Category.objects.filter(name__in=ALLOWED_CATEGORIES.keys())
    
    return render(request, 'libraryapp/category.html', {'categories': categories})


def category_books(request, category_id):
    try:
        # Burada Category modelinden kategori bilgilerini alıyoruz (veritabanından)
        category = Category.objects.get(id=category_id)

        # API üzerinden kitapları alıyoruz
        response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={category.name}&langRestrict=tr")
        
        if response.status_code == 200:
            books_data = response.json()
            books = books_data.get('items', [])
        else:
            books = []
        
        # Şablona veri gönderme
        return render(request, 'libraryapp/category-list.html', {'category': category, 'books': books})

    except Category.DoesNotExist:
        return HttpResponseNotFound('Kategori bulunamadı')
    

def hakkında(request):
    return render(request, 'libraryapp/hakkında.html')


@login_required
def sikayet_gonder(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            # Admin’e bildirim gönder (superuser olanlara)
            admins = User.objects.filter(is_superuser=True)
            for admin in admins:
                Notification.objects.create(
                    user=admin,
                    message=f"{request.user.username} bir şikayet gönderdi: {complaint.subject}"
                )

            messages.success(request, "Şikayetiniz başarıyla gönderildi!")
            return redirect('index')  # Ana sayfaya yönlendir
        else:
            messages.error(request, "Lütfen formu doğru doldurun!")
    else:
        form = ComplaintForm()
    
    return render(request, 'libraryapp/sikayet-gonder.html', {'form': form})

@staff_member_required  # Sadece admin/staff görebilir
def admin_bildirimler(request):
    complaints = Complaint.objects.filter(is_resolved=False).order_by('-created_at')
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    context = {
        'complaints': complaints,
        'notifications': notifications,
    }
    return render(request, 'libraryapp/admin-bildirimler.html', context)


@staff_member_required
def sikayet_sil(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        # Şikayete bağlı bildirimleri sil
        Notification.objects.filter(
            message__contains=f"{complaint.user.username} bir şikayet gönderdi: {complaint.subject}"
        ).delete()
        # Şikayeti sil
        complaint.delete()
        messages.success(request, "Şikayet ve ilgili bildirimler başarıyla silindi!")
        return redirect('admin_bildirimler')
    return redirect('admin_bildirimler')

@staff_member_required
def şikayet_sayısı(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        unresolved_complaints = Complaint.objects.filter(is_resolved=False).count()
        return JsonResponse({
            'unresolved_complaints': unresolved_complaints,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


    