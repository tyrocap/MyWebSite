from django.urls import path

from .views import BookListView, BookDetailView, data_update, add_to_shelf, \
    ProfileView, update_book_progress

urlpatterns = [
    path('', BookListView.as_view(), name='home_page'),
    path('<uuid:pk>', BookDetailView.as_view(), name='single_product_page'),
    path('<str:pk>', ProfileView.as_view(), name='profile_view'),
    path('data_update/', data_update, name='data_update'),
    path('add_to_shelf/', add_to_shelf, name='add_to_shelf'),
    path('update_book_progress/', update_book_progress, name='update_book_progress'),
]
