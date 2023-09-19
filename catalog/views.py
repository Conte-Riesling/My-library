from django.shortcuts import render

# Create your views here.
from .models import Book, Author, BorrowRequest, Genre

def index(request):
    # Функция просмотра домашней страницы сайта
    # Генерируем счетчики некоторых основных объектов
    num_books=Book.objects.all().count()
    num_requests=BorrowRequest.objects.all().count()
    # Доступные экземпляры книг
    num_requests_available=BorrowRequest.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  
    

    # Отобразите HTML-шаблон index.html с данными в переменной context
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_requests':num_requests,'num_requests_available':num_requests_available,'num_authors':num_authors},
    )

from django.views import generic

# Общее представление списка книг на основе классов
class BookListView(generic.ListView):
    model = Book

# Общее подробное представление книги на основе классов
class BookDetailView(generic.DetailView):
    model = Book

# Общее представление списка авторов на основе классов
class AuthorListView(generic.ListView):
    model = Author

# Общее подробное представление на основе классов для автора
class AuthorDetailView(generic.DetailView):
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    # Общий список книг на основе классов, предоставленных текущему пользователю
    model = BorrowRequest
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self):
        return (
            BorrowRequest.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_date')
        )

from django.contrib.auth.decorators import login_required, permission_required


@permission_required('catalog.can_mark_returned', raise_exception=True)
def my_view(request):

    from django.contrib.auth.mixins import PermissionRequiredMixin
    from django.views.generic import View

    class MyView(PermissionRequiredMixin, View):
        permission_required = 'catalog.can_mark_returned'
    

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm

@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)

# Функция просмотра для обновления определенного экземпляра книги библиотекарем
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BorrowRequest, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_date)
            book_inst.due_date = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.contrib.auth.mixins import PermissionRequiredMixin

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth']
    permission_required = 'catalog.can_mark_returned'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' 
    permission_required = 'catalog.can_mark_returned'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'publisher', 'published_date']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'publisher', 'published_date']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'
    


   