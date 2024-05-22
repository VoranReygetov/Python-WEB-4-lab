from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
from pathlib import Path
from .models import *
from .forms import BookForm
from django.db.models import F
from .serializers import BookSerializer

# Create your views here.

def home(request):
    """
    Redirect form empty page.
    """
    return redirect("login")

@login_required
def book_list(request):
    """
    Returns the render of the book list page.
    """
    current_user = request.user
    if request.method == 'GET':
        if current_user.is_superuser:
            template_file = 'book-list-roles/admin-book-list.html'
        else:
            template_file = 'book-list-roles/user-book-list.html'

        books = Book.objects.all()
        rents = History.objects.filter(user = current_user.id, isReturned = False)

        rents_id = [rent.books.id for rent in rents]
        form = BookForm()
        # A context dictionary with all the key-value pairs
        context = {
            "books": books,
            "username": current_user.username,
            "rents_book_id": rents_id,
            'form':form
        }

        # Context dictionary in the render function
        return render(request, template_file, context)
    
    if request.method == 'POST':
        current_user = request.user
        if not current_user.is_superuser:
            return HttpResponseForbidden("Authorization failed")
        
        book_id = request.POST.get('id')
        if book_id:  # Check if it's an update operation
            book_instance = get_object_or_404(Book, pk=book_id)
            form = BookForm(request.POST, instance=book_instance)
        else:
            form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book-list')
        else:
            # Handle invalid form submission here
            return JsonResponse({"message": "Invalid form data"})
    else:
        # This block handles GET requests or initial form rendering
        form = BookForm()
        return render(request, 'your_template.html', {'form': form})

@login_required
def book_methods(request, book_id):
    if request.method == 'GET':
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        book_json = BookSerializer(book, many = False).data
        return JsonResponse(book_json)
    elif request.method == 'DELETE' and request.user.is_superuser:
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return JsonResponse({'error': 'Book not found'}, status=404)
        book.delete()
        return JsonResponse(BookSerializer(book, many = False).data)


@login_required
def rent_book(request, book_id):
    if request.method != 'POST':
        raise Http404('Inappropriate method')

    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    # Check if the user has already rented this book and not returned it
    rent = History.objects.filter(user=request.user, books=book, isReturned=False).first()
    if rent:
        # If the book is already rented by the user, mark it as returned
        rent.isReturned = True
        rent.dateReturn = timezone.now()
        rent.save()

        # Increase the available count for the book
        book.availableBook = F('availableBook') + 1
        book.save()
    else:
        # If the book is not rented by the user, create a new rent record
        rent = History(user=request.user, books=book, isReturned=False)
        rent.save()

        # Decrease the available count for the book
        book.availableBook = F('availableBook') - 1
        book.save()

    return redirect("book-list")

@login_required
def rent_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Authorization failed")

    rents_list = History.objects.all().order_by('isReturned')

    context = {
        "rents": rents_list,
        "username": request.user,
    }

    return render(request, "rent-list.html", context)