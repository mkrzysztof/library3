from django.db.utils import IntegrityError
from django.db import connection
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, ListView

from librarian.forms import (ReaderChoseForm, ReturnBookForm, BorrowBookForm,
                             SearchBookForm)
from librarian.models import Book, Reader, Borrowing
# Create your views here.

def test(request):
    return render(request, 'librarian/test.html')


class StartView(TemplateView):
    template_name = 'librarian/start.html'


class AddingBookView(TemplateView):
    template_name = 'librarian/book_detail.html'


class AdministrationView(TemplateView):
    template_name = 'librarian/administration.html'


class CreateBookView(CreateView):
    model = Book
    success_url = reverse_lazy('book_adding')
    fields = '__all__'

class CreateReaderView(CreateView):
    model = Reader
    fields = '__all__'
    success_url = reverse_lazy('reader_adding')

class AddingReaderView(TemplateView):
    template_name = 'librarian/reader_detail.html'


class ReaderView(TemplateView):
    template_name = 'librarian/reader.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reader_name'] = self.request.session['reader_name']
        context['reader_id'] = self.request.session['reader_id']
        context['was_borrowing'] = self.request.session.get('was_borrowing',
                                                            True)
        return context


class ReaderChoseView(FormView):
    template_name = 'librarian/chose_reader.html'
    form_class = ReaderChoseForm
    success_url = reverse_lazy('chose_reader')
    
        


class FindReaderView(View):
    def post(self, request):
        form = ReaderChoseForm(request.POST)
        request.session['reader_name'] = "NIE MA"
        if form.is_valid():
            id = form.cleaned_data['reader_id']
            try:
                reader = Reader.objects.get(pk=id)
            except Reader.DoesNotExist:
                request.session['reader_id'] = 0
            else:
                request.session['reader_id'] = id
                request.session['reader_name'] = reader.name
        return redirect(reverse('reader'))
    

class ReturnBookView(FormView):
    template_name = 'librarian/manipulate_book.html'
    form_class = ReturnBookForm
    success_url = reverse_lazy('reader')

    def form_valid(self, form):
        print(dir(self.request))
        form.return_book()
        self.request.session['was_borrowing'] = True
        return super().form_valid(form)


class BorrowBookView(FormView):
    template_name = 'librarian/manipulate_book.html'
    form_class = BorrowBookForm
    success_url = reverse_lazy('reader')

    def form_valid(self, form):
        # form.borrow_book()
        print(form.cleaned_data)
        print(self.request.session.keys())
        print(self.request.session['reader_id'])
        reader = Reader.objects.get(id=self.request.session['reader_id'])
        book = Book.objects.get(id = form.cleaned_data['book_id'])
        try:
            bor = Borrowing(book=book, borrower=reader)
            bor.save()
        except IntegrityError:
            self.request.session['was_borrowing'] = False
        else:
            self.request.session['was_borrowing'] = True
        return super().form_valid(form)


class ReaderBookView(ListView):
    model = Book
    
    def get_queryset(self):
        reader_id = self.request.session['reader_id']
        books = Book.objects.filter(borrowing__borrower_id=reader_id)
        return books


class SearchBookView(View):
    def get(self, request):
        find_books = request.session.get('books_find', None)
        ctx = {'form': SearchBookForm(),
               'find_books': find_books}
        return render(request, 'librarian/search_book.html',
                      context=ctx)

    def post(self, request):
        form = SearchBookForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            title = form.cleaned_data['title']
            with connection.cursor() as cursor:
                cursor.execute('''
                SELECT book.id, book.author, book.title,
                CASE
                   WHEN borrowing.id is null THEN "wolna"
                   ELSE "wypożyczona"
                END AS is_free
                FROM librarian_book as book LEFT JOIN
                librarian_borrowing as borrowing
                ON (book.id=borrowing.book_id)
                WHERE book.title like %s
                ''', [title])
                rows = cursor.fetchall()
            request.session['books_find'] = rows
            for r in rows:
                print(r)
        return redirect(reverse('search_book'))
    
