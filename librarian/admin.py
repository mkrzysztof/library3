from django.contrib import admin

from .models import Reader, Book, Borrowing

# Register your models here.
admin.site.register(Reader)
admin.site.register(Book)
admin.site.register(Borrowing)
