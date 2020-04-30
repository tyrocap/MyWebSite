from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Book, CustomUser, CustomUserProfile
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.postgres.search import SearchVector
from django.conf import settings
from .forms import WanttoReadForm, BookProgressForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


class BookListView(ListView):
    model = Book
    paginate_by = 12
    context_object_name = 'book_list'
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('contains_qs'):
            context['filtered_book_list'] = Book.objects.annotate(
                search=SearchVector(
                    'title', 'author', 'category'), ).filter(
                search=self.request.GET.get(
                    'contains_qs'))
            return context
        elif self.request.GET.get('all'):
            return context
        elif self.request.GET.get('his'):
            context['filtered_book_list'] = Book.objects.filter(
                category='History')
            return context
        elif self.request.GET.get('b&a'):
            context['filtered_book_list'] = Book.objects.filter(
                category='Biography & Autobiography')
            return context
        elif self.request.GET.get('lic'):
            context['filtered_book_list'] = Book.objects.filter(
                category='Literary Criticism')
            return context
        else:
            return context


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'single_product_page.html'


class ProfileView(DetailView):
    model = CustomUser
    template_name = 'new.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile_books'] = CustomUserProfile.objects.filter(
            cu_user=self.object)
        return context





def data_update(request):
    author_title_dic = {}
    api_key_google = settings.GOOGLE_API_KEY
    for i in author_title_dic:
        author = i
        title = author_title_dic[i]
        book_url_google = f'https://www.googleapis.com/books/v1/volumes?q=intitle:{title}&key={api_key_google}'
        content_google = requests.get(url=book_url_google).json()
        try:
            img_url_google = \
                content_google['items'][0]['volumeInfo']['imageLinks'][
                    'smallThumbnail']
        except:
            img_url_google = ""
        try:
            description_google = content_google['items'][0]['volumeInfo'][
                'description']
        except:
            description_google = ""
        try:
            categories_google = \
                content_google['items'][0]['volumeInfo']['categories'][0]
        except:
            categories_google = "None"
        try:
            primary_isbn13_google = \
                content_google['items'][0]['volumeInfo']['industryIdentifiers'][
                    0][
                    'identifier']
        except:
            primary_isbn13_google = 111111111111
        try:
            preview_link_google = content_google['items'][0]['volumeInfo'][
                'previewLink']
        except:
            preview_link_google = 'https://books.google.com/'
        try:
            price_google = content_google['items'][0]['saleInfo']['listPrice'][
                'amount']
        except:
            price_google = 0
        try:
            page_count = content_google['items'][0]['volumeInfo']['pageCount']
        except:
            page_count = 0
        try:
            average_rating = content_google['items'][0]['volumeInfo']['averageRating']
        except:
            average_rating = 0.0
        try:
            rating_count = content_google['items'][0]['volumeInfo']['ratingsCount']
        except:
            rating_count = 0
        book = Book(
            title=title,
            author=author,
            price=price_google,
            category=categories_google,
            description=description_google,
            image=img_url_google,
            primary_isbn13=primary_isbn13_google,
            preview_link_google=preview_link_google,
            page_count=page_count,
            average_rating=average_rating,
            rating_count=rating_count
        )
        book.save()

    return redirect('home_page')


def add_to_shelf(request):
    if 'wanttoread' in request.POST:
        book_id = request.POST.get('book_id', None)
        book_obj = Book.objects.get(id=book_id)
        user_obj = request.user
        # check if the book clicked is in the bookshelf already
        try:
            user_profile_check = CustomUserProfile.objects.get(cu_user=user_obj, cu_wanttoread_book=book_obj)
        except ObjectDoesNotExist:
            user_profile_check = False
        if not user_profile_check:
            user_profile = CustomUserProfile(cu_user=user_obj, cu_wanttoread_book=book_obj)
            user_profile.save()
            messages.success(request, "The book successfully added to your "
                                      "shelf.")
        else:
            messages.error(request, "You cannot add the same book twice.")
    return redirect('home_page')


def update_book_progress(request):
    if request.method == "POST":
        form = BookProgressForm(request.POST)
        if form.is_valid():
            book_progress_input = form.cleaned_data['book_progress_input']
            book_progress_id = form.cleaned_data['book_progress_id']
            try:
                book_progress_note = form.cleaned_data['book_progress_note_input']
            except:
                pass
            user_profile = CustomUserProfile.objects.get(
                cu_user=request.user,
                cu_wanttoread_book=Book.objects.get(id=book_progress_id))
            user_profile.cu_book_progress = book_progress_input
            try:
                user_profile.cu_book_progress_note = book_progress_note
            except:
                pass
            print("A"*39)
            print(book_progress_id)
            print("A" * 39)
            user_profile.save()
        else:
            messages.error(request, "Please try again.")
        return redirect('profile_view', pk=request.user.id)
    else:
        form = BookProgressForm()
        return redirect('profile_view', pk=request.user.id)

# tried & changed
# 'b5de4a8d-70f6-4205-b053-34a164f380c4 _ The Last Lecture by Randy Pausch'

# tried
# '069d3a18-bbf2-4650-b086-424b68f12d3e _ Lead and Succeed Through Motivation: \
#     How to motivate your staff and inspire them to achieve goals in the workplace by Abraham Goldberg
# changed
# The Last Lecture by Randy Pausch

# tried
# 'fe90cad8-805c-4ec3-8917-a39fcc00842b _ High Output Management by Andrew S. Grove'
# changed
# Lead and Succeed Through Motivation: How to motivate your staff and inspire them to achieve goals in the workplace
# by Abraham Goldberg

# cu_user
# cu_wanttoread_book
# cu_book_id
# cu_book_progress
# cu_book_progress_note




# book_progress_input
# book_progress_note_input
# name="cancel"
# name="update_progress"
