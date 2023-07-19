from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=300)


class Reader(models.Model):
    name = models.CharField(max_length=300)
    cart_id = models.CharField(max_length=10)


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    book = models.ForeignKey("Book", on_delete=models.CASCADE, unique=True)
    borrower = models.ForeignKey('Reader', on_delete=models.CASCADE)
    
