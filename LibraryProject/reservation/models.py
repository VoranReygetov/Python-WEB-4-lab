from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Custom user manager for creating users with email as unique identifier
class UserManager(BaseUserManager):
    def create_user(self, emailUser, passwordUser=None, **extra_fields):
        if not emailUser:
            raise ValueError("The Email field must be set")
        emailUser = self.normalize_email(emailUser)
        user = self.model(emailUser=emailUser, **extra_fields)
        if passwordUser:
            user.set_password(passwordUser)
        user.save(using=self._db)
        return user

    def create_superuser(self, emailUser, passwordUser=None, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(emailUser, passwordUser, **extra_fields)


# Custom user model
class User(AbstractBaseUser):
    emailUser = models.EmailField(unique=True)
    nameUser = models.CharField(max_length=255)
    surnameUser = models.CharField(max_length=255, blank=True, null=True)
    numberUser = models.PositiveIntegerField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'emailUser'
    REQUIRED_FIELDS = ['nameUser']

    def check_password(self, password):
        return self.check_password(password)  # Django provides this method


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
        return f"Loan by {self.user.emailUser} for {self.books.nameBook}"
