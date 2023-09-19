from django.db import models
from django.urls import reverse # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
from django.contrib.auth.models import User  



# Create your models here.


class Author(models.Model):
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.CharField(max_length=255, help_text="Short biography and description of the author")

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        # Возвращает URL-адрес для доступа к конкретному экземпляру автора
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        # Строка для представления объекта модели
        return '{0}, {1}'.format(self.last_name, self.first_name)
 

# Модель, представляющая жанр книги
class Genre(models.Model):
     name = models.CharField(max_length=200, help_text="Enter a book genre (Fiction, Science, Romance, Science Fiction, French Poetry etc.)")

# Строка для представления объекта модели (на сайте администратора и т. д.)
def __str__(self):
    return self.name

# Модель, представляющая книгу
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, help_text='Book Author')
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN',max_length=15, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, help_text="Select a genre for this book")
    available = models.BooleanField(default=True)
    published_date = models.DateField()
    publisher = models.CharField(max_length=255, help_text="Enter the organization or company that printed and sold the book")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class Meta:
        ordering = ['title', 'author']


# Возвращает URL-адрес для доступа к определенному экземпляру книги
def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

# Строка для представления объекта модели   
def __str__(self):
    return self.title

    
# Модель, которая фиксирует намерение пользователя взять конкретную книгу
class BorrowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    request_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,  default='', help_text="User who wants to borrow a book")

    @property
    def is_overdue(self):
        if self.due_date and date.today() > self.due_date:
            return True
        return False


    LOAN_STATUS = (
        ('1', 'PENDING'),
        ('2', 'APPROVED'),
        ('3', 'COLLECTED'),
        ('4', 'COMPLETE'),
        ('5', 'DECLINED')
    )

    status = models.CharField(max_length=20, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_date"]
        permissions = (("can_mark_returned", "Set book as returned"),)

# Строка для представления объекта модели
    def __str__(self):
        return '%s (%s)' % (self.id,self.book.title)
    

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
