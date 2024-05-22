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


# def authenticate_user(email, password):

#     users_collection = data['users']
#     # Find the user with the email
#     searched_user = None
#     for user in users_collection:
#         if user['emailUser'] == email:
#             searched_user = user
#     # If the user is found and the password matches, return the user 
#     if searched_user and searched_user.get("passwordUser") == password:
#         return searched_user
    
#     return None


# def assign_id(item):
#     if "id" not in item:  # Assign ID only if it's not already set
#         item["id"] = str(uuid.uuid4())  # Using UUID for unique IDs
#     return item


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

        # categories_dict = {cat['id']: cat for cat in data['categories']}
        # authors_dict = {author['id']: author for author in data['authors']}
        # Category.objects.get

        # # Merge categories and authors with books
        # books_with_categories_and_authors = []
        # for book in data['books']:
        #     # Get the category and author by id
        #     category = Category.objects.get
        #     author = Author.objects.get

        #     # Create the new book entry
        #     book_entry = {
        #         "id": book["id"],
        #         "nameBook": book["nameBook"],
        #         "yearBook": book["yearBook"],
        #         "availableBook": book["availableBook"],
        #         "nameCategory": category["nameCategory"] if category else None,
        #         "authorName": f"{author['nameAuthor']} {author['surnameAuthor']}" if author else None,
        #     }

        #     # Append to the final result
        #     books_with_categories_and_authors.append(book_entry)

        # # Sort by 'nameBook'
        # books_with_categories_and_authors = sorted(
        #     books_with_categories_and_authors, key=lambda b: b["nameBook"]
        # )

        # rents = []
        # if not request.user["is_superuser"]:
        #     rents = [
        #         history["book_id"]
        #         for history in data["histories"]
        #         if history["user_id"] == request.user["id"] and not history["isReturned"]
        #         ]

        # # A context dictionary with all the key-value pairs
        # context = {
        #     "books": books_with_categories_and_authors,
        #     "username": email,
        #     "rents_book_id": rents,
        # }

        # Context dictionary in the render function
        return render(request, template_file, Book.objects.get)
    
    elif request.method == 'POST':
        if not request.user['is_superuser']:
            raise HttpResponseForbidden("Authorization failed")
        
        Book.nameBook=request.get("nameBook")
        Book.yearBook=request.get("yearBook")
        Book.availableBook=request.get("availableBook")
        Book.category=request.get("category")
        Book.author=request.get("author_id")
        
        # request_data = json.load(request)
        # book_data = {
        # "nameBook": request_data.get("nameBook"),
        # "yearBook": request_data.get("yearBook"),
        # "availableBook": request_data.get("availableBook"),
        # "category_id": request_data.get("category_id"),
        # "author_id": request_data.get("author_id")
        # }
        # #book_data = assign_id(book_data)
        # data['books'].append(book_data)

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
# def rent_book(request, book_id):

#     if request.method != 'POST':
#         Http404('Inappropriate method')
#     date_now = datetime.now()

#     if not request.user:
#         raise HttpResponseForbidden("Authorization failed")
#     rent_data = None
#     found = False  # Flag to indicate if a matching record is found
#     for index1, rent in enumerate(data['histories']):
#         if rent['user_id'] == user['id'] and not rent['isReturned'] and rent['book_id'] == book_id:
#             # Mark the book as returned
#             data['histories'][index1]['isReturned'] = True
#             data['histories'][index1]['dateReturn'] = str(date_now)

#             # Increase the available count for the book
#             for index2, book in enumerate(data['books']):
#                 if book['id'] == rent['book_id']:
#                     data['books'][index2]['availableBook'] += 1
#                     break

#             rent_data = data['histories'][index1]
#             found = True  # A match was found
#             break

#     if not found:
#         # If no matching rent was found, create a new one
#         rent_data = {
#             "user_id": user['id'],
#             "book_id": book_id,
#             "dateLoan": str(date_now),
#             "isReturned": False
#         }
#         #rent_data = assign_id(rent_data)
#         # Append the new rent to the histories list
#         data['histories'].append(rent_data)

#         # Decrease the available count for the book
#         for book in data['books']:
#             if book['id'] == rent_data['book_id']:
#                 book['availableBook'] -= 1
#                 break
        
#     with open(json_file, 'w') as f:
#         json.dump(data, f, indent=4)
#     return JsonResponse(rent_data)

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
        "username": request.user.email,
    }

    return render(request, "rent-list.html", context)