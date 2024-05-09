from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Author(models.Model):
    nameAuthor = models.CharField(max_length=255)
    surnameAuthor = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nameAuthor} {self.surnameAuthor}"


class Category(models.Model):
    nameCategory = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nameCategory


class Book(models.Model):
    nameBook = models.CharField(max_length=255)
    yearBook = models.PositiveIntegerField(blank=True, null=True)
    availableBook = models.PositiveIntegerField(default=0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.nameBook


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories')
    books = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='histories')
    dateLoan = models.DateTimeField(default=timezone.now)
    dateReturn = models.DateTimeField(blank=True, null=True)
    isReturned = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan by {self.user.get_full_name()} for {self.books.nameBook}"
