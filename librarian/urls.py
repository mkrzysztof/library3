from django.urls import path

from librarian.views import (StartView, AdministrationView,
                             CreateBookView, AddingBookView,
                             CreateReaderView, AddingReaderView,
                             ReaderView, ReaderChoseView,
                             FindReaderView, ReturnBookView,
                             BorrowBookView, ReaderBookView,
                             SearchBookView)

urlpatterns = [
    path('', StartView.as_view(), name='start'),
    path('administration/', AdministrationView.as_view(),
         name='administration'),
    path('add_book/', CreateBookView.as_view(), name='add_book'),
    path('book_adding/', AddingBookView.as_view(), name='book_adding'),
    path('add_reader/', CreateReaderView.as_view(), name='add_reader'),
    path('reader_adding/', AddingReaderView.as_view(), name='reader_adding'),
    path('reader/', ReaderView.as_view(), name='reader'),
    path('chose_reader/', ReaderChoseView.as_view(), name='chose_reader'),
    path('find_reader/', FindReaderView.as_view(), name='find_reader'),
    path('return_book/', ReturnBookView.as_view(), name='return_book'),
    path('borrow_book/', BorrowBookView.as_view(), name='borrow_book'),
    path('view_reader_book/', ReaderBookView.as_view(),
         name='view_reader_book'),
    path('search_book', SearchBookView.as_view(), name='search_book'),
]
