from django import forms
from librarian.models import Book, Reader, Borrowing


class BorrowingForm(forms.ModelForm):
    class Meta:
        model = Borrowing
        fields = ['book']


class ReaderChoseForm(forms.Form):
    reader_id = forms.IntegerField()


class ReturnBookForm(forms.Form):
    book_id = forms.IntegerField()

    def return_book(self):
        print(self.cleaned_data)
        book_id = self.cleaned_data['book_id']
        book = Book.objects.get(id=book_id)
        borrowing = Borrowing.objects.get(book=book)
        borrowing.delete()


class BorrowBookForm(forms.Form):
    book_id = forms.IntegerField()

    def borrow_book(self):
        print(self.cleaned_data)


class SearchBookForm(forms.Form):
    author = forms.CharField(label='autor')
    title = forms.CharField(label='tytuł')
