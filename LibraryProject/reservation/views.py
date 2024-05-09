from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest, Http404
import json
import uuid  # For generating unique IDs
from pathlib import Path
from .models import *

# Create your views here.

json_file = Path("D:\Programs\KPI\Python-WEB-4-lab\LibraryProject\data.json")

with open(json_file, 'r') as f:
    data = json.load(f)  # Load the existing JSON data


def authenticate_user(email, password):

    users_collection = data['users']
    # Find the user with the email
    searched_user = None
    for user in users_collection:
        if user['emailUser'] == email:
            searched_user = user
    # If the user is found and the password matches, return the user 
    if searched_user and searched_user.get("passwordUser") == password:
        return searched_user
    
    return None


def assign_id(item):
    if "id" not in item:  # Assign ID only if it's not already set
        item["id"] = str(uuid.uuid4())  # Using UUID for unique IDs
    return item


def home(request):
    """
    Redirect form empty page.
    """
    return redirect("login")

# @csrf_exempt
# @api_view(['GET', 'POST'])
# def login(request):
#     """
#     Retrieves the login page.
#     """
#     if request.method != 'POST':
#         email = request.COOKIES.get("email")
#         password = request.COOKIES.get("password")
#         user = authenticate_user(email, password)
#         if user:
#             return redirect("/book-list")
#         return render(request, 'login.html')
    
#     request_data = json.load(request)
#     email = request_data.get("emailUser")
#     password = request_data.get("passwordUser")
#     user = authenticate_user(email, password)
#     try:
#         if user:
#             response = JsonResponse({"message": f"{user}"})
#             response.set_cookie(key="email", value=request_data.get("emailUser"))
#             response.set_cookie(key="password", value=request_data.get("passwordUser"))
#             return response
#         else:
#             return HttpResponseBadRequest("Login failed")
#     except:
#         raise HttpResponseBadRequest("Login failed")
    
# @csrf_exempt
# def registration(request):
#     """
#     Retrieves the registration page.
#     """
#     if request.method != 'POST':
#         return render(request, 'registration.html')
    
#     request_data = json.load(request)
#     inserted_user = {
#             "nameUser": request_data["nameUser"],
#             "surnameUser": request_data["surnameUser"],
#             "passwordUser": request_data["passwordUser"],
#             "is_admin": False,
#             "emailUser": request_data["emailUser"],
#             "numberUser": request_data["numberUser"]
#         }
#     try:

#         email_exists = any(user['emailUser'] == inserted_user['emailUser'] for user in data['users'])
#         # If the email doesn't exist, add the user
#         if not email_exists:
#             inserted_user = assign_id(inserted_user)
#             data['users'].append(inserted_user)
#         else:
#             raise Exception

#         with open(json_file, 'w') as f:
#             json.dump(data, f, indent=4)
        
#         response = JsonResponse({"message": f"{inserted_user}"})
#         response.set_cookie(key="email", value=inserted_user.get("emailUser"))
#         response.set_cookie(key="password", value=inserted_user.get("passwordUser"))
#         return response
#     except:
#         return HttpResponseBadRequest('Registration failed')


@csrf_exempt
def book_list(request):
    """
    Returns the render of the book list page.
    """
    if request.method == 'GET':
        email = request.COOKIES.get("email")
        password = request.COOKIES.get("password")
        user = authenticate_user(email, password)
        if user['is_admin']:
            template_file = 'book-list-roles/admin-book-list.html'
        else:
            template_file = 'book-list-roles/user-book-list.html'

        categories_dict = {cat['id']: cat for cat in data['categories']}
        authors_dict = {author['id']: author for author in data['authors']}

        # Merge categories and authors with books
        books_with_categories_and_authors = []
        for book in data['books']:
            # Get the category and author by id
            category = categories_dict.get(book['category_id'])
            author = authors_dict.get(book['author_id'])

            # Create the new book entry
            book_entry = {
                "id": book["id"],
                "nameBook": book["nameBook"],
                "yearBook": book["yearBook"],
                "availableBook": book["availableBook"],
                "nameCategory": category["nameCategory"] if category else None,
                "authorName": f"{author['nameAuthor']} {author['surnameAuthor']}" if author else None,
            }

            # Append to the final result
            books_with_categories_and_authors.append(book_entry)

        # Sort by 'nameBook'
        books_with_categories_and_authors = sorted(
            books_with_categories_and_authors, key=lambda b: b["nameBook"]
        )

        rents = []
        if not user["is_admin"]:
            rents = [
                history["book_id"]
                for history in data["histories"]
                if history["user_id"] == user["id"] and not history["isReturned"]
                ]

        # A context dictionary with all the key-value pairs
        context = {
            "books": books_with_categories_and_authors,
            "username": email,
            "rents_book_id": rents,
        }

        # Context dictionary in the render function
        return render(request, template_file, context)
    
    elif request.method == 'POST':
        email = request.COOKIES.get("email")
        password = request.COOKIES.get("password")
        user = authenticate_user(email, password)
        if not user["is_admin"]:
            raise HttpResponseForbidden("Authorization failed")
        
        request_data = json.load(request)
        book_data = {
        "nameBook": request_data.get("nameBook"),
        "yearBook": request_data.get("yearBook"),
        "availableBook": request_data.get("availableBook"),
        "category_id": request_data.get("category_id"),
        "author_id": request_data.get("author_id")
        }
        book_data = assign_id(book_data)
        data['books'].append(book_data)

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)  # Save the updated JSON data
        return JsonResponse({"message": f"{book_data}"})

@csrf_exempt
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
        email = request.COOKIES.get("email")
        password = request.COOKIES.get("password")
        user = authenticate_user(email, password)
        if not user["is_admin"]:
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
        email = request.COOKIES.get("email")
        password = request.COOKIES.get("password")
        user = authenticate_user(email, password)
        if not user["is_admin"]:
            raise HttpResponseForbidden("Authorization failed")
        
        for book in data['books']:
            if book['id'] == book_id:
                # Replace the existing book data with new book data
                data['books'].remove(book)
                break

        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)
        return JsonResponse({"message": f"{data['books']}"})

@csrf_exempt
def rent_book(request, book_id):

    if request.method != 'POST':
        Http404('Inappropriate method')
    date_now = datetime.now()
    email = request.COOKIES.get("email")
    password = request.COOKIES.get("password")
    user = authenticate_user(email, password)

    if not user:
        raise HttpResponseForbidden("Authorization failed")
    rent_data = None
    found = False  # Flag to indicate if a matching record is found
    for index1, rent in enumerate(data['histories']):
        if rent['user_id'] == user['id'] and not rent['isReturned'] and rent['book_id'] == book_id:
            # Mark the book as returned
            data['histories'][index1]['isReturned'] = True
            data['histories'][index1]['dateReturn'] = str(date_now)

            # Increase the available count for the book
            for index2, book in enumerate(data['books']):
                if book['id'] == rent['book_id']:
                    data['books'][index2]['availableBook'] += 1
                    break

            rent_data = data['histories'][index1]
            found = True  # A match was found
            break

    if not found:
        # If no matching rent was found, create a new one
        rent_data = {
            "user_id": user['id'],
            "book_id": book_id,
            "dateLoan": str(date_now),
            "isReturned": False
        }
        rent_data = assign_id(rent_data)
        # Append the new rent to the histories list
        data['histories'].append(rent_data)

        # Decrease the available count for the book
        for book in data['books']:
            if book['id'] == rent_data['book_id']:
                book['availableBook'] -= 1
                break
        
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)
    return JsonResponse(rent_data)


def rent_list(request):
    email = request.COOKIES.get("email")
    password = request.COOKIES.get("password")
    user = authenticate_user(email, password)
    if not user:
        redirect('login')
    if not user['is_admin']:
        return HttpResponseForbidden("Authorization failed")
    
    rents_list =  sorted(
            data['histories'], key=lambda b: b["isReturned"], reverse=True)
    print(rents_list)
    context = {
        "rents": rents_list, 
        "username" : user['emailUser']
        }
    return render(request, "rent-list.html", context)


def clear_cookie(request):
    response = HttpResponse("Cookie deleted")
    response.delete_cookie("email")
    response.delete_cookie("password")
    return response