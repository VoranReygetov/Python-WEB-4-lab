from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest, Http404
from django.db.models import F
import json
import uuid  # For generating unique IDs
from pathlib import Path
from .models import *

# Create your views here.

json_file = Path("D:\Reposit\Python-WEB-4-lab\LibraryProject\data.json")

with open(json_file, 'r') as f:
    data = json.load(f)  # Load the existing JSON data

def secure_view(request):
    return render(request, 'secure_page.html')

def home(request):
    """
    Redirect form empty page.
    """
    return redirect("login")

@login_required  # Ensures that only authenticated users can access this view
def book_list(request):
    """
    Returns the render of the book list page.
    """
    if request.method == 'GET':
        if request.user['is_superuser']:
            template_file = 'book-list-roles/admin-book-list.html'
        else:
            template_file = 'book-list-roles/user-book-list.html'
        return render(request, template_file, Book.objects.get)
    
    elif request.method == 'POST':
        if not request.user['is_superuser']:
            raise HttpResponseForbidden("Authorization failed")
        
        Book.nameBook=request.get("nameBook")
        Book.yearBook=request.get("yearBook")
        Book.availableBook=request.get("availableBook")
        Book.category=request.get("category")
        Book.author=request.get("author_id")
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)  # Save the updated JSON data
        return JsonResponse({"message": f"{request}"})

@login_required  # Ensures that only authenticated users can access this view
def book_page(request, book_id):
    """
    Handles a book CRUD operations
    """
    if request.method == 'GET':
        # Fetch the book from the database
        for book in data['books']:
            if book['id'] == book_id:
                return JsonResponse(book)  # Return the first match

        if book is None:
            # If the book is not found, raise a 404 exception
            raise Http404('Book is not found')

    elif request.method == 'PUT':
        if not request.user['is_superuser']:
            raise HttpResponseForbidden("Authorization failed")
        
        request_data = json.load(request)
        book_data = {
        "id": book_id,
        "nameBook": request_data.get("nameBook"),
        "yearBook": request_data.get("yearBook"),
        "availableBook": request_data.get("availableBook"),
        "category_id": request_data.get("category_id"),
        "author_id": request_data.get("author_id")
        }

        for index, book in enumerate(data['books']):
            if book['id'] == book_id:
                # Replace the existing book data with new book data
                data['books'][index] = book_data
                break
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        return JsonResponse({"message": f"{data['books']}"})
    
    elif request.method == 'DELETE':
        if not request.user['is_superuser']:
            raise HttpResponseForbidden("Authorization failed")
        
        for book in data['books']:
            if book['id'] == book_id:
                # Replace the existing book data with new book data
                data['books'].remove(book)
                break

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        return JsonResponse({"message": f"{data['books']}"})

@login_required  # Ensures that only authenticated users can access this view
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

    return JsonResponse({
        "user_id": rent.user.id,
        "book_id": rent.books.id,
        "dateLoan": rent.dateLoan,
        "isReturned": rent.isReturned
    })


# def rent_list(request):
#     if not request.user:
#         redirect('login')
#     if not request.user['is_superuser']:
#         return HttpResponseForbidden("Authorization failed")
    
#     rents_list =  sorted(
#             data['histories'], key=lambda b: b["isReturned"], reverse=True)
#     print(rents_list)
#     context = {
#         "rents": rents_list, 
#         "username" : request.user['emailUser']
#         }
#     return render(request, "rent-list.html", context)


def rent_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Authorization failed")

    # Get all rent records, sorted by isReturned in descending order
    rents_list = History.objects.all().order_by('-isReturned')

    context = {
        "rents": rents_list,
        "username": request.user,
    }

    return render(request, "rent-list.html", context)