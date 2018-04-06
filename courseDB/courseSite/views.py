from django.shortcuts import render
from .models import Course, Review
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import datetime

# Create your views here.
def getCatalog(request):
    course_list = Course.objects.all()
    return render(request,'Catalog.html', {'class_list': Course.objects.all()})

def FrontPage(request):
    return render(request, 'FrontPage.html')

def class_page(request, class_name):
    review_list = Review.objects.filter(name=class_name)
    course = Course.objects.filter(title=class_name)[0]
    return render(request, 'classPage.html', {'course': course, 'review_list': review_list})

def search_results(request):
    query = request.POST.get("query", "")
    category = request.POST.get("category")
    class_list = retrieveObjects(request)
    return render(request, 'searchResults.html', {'query': category, 'class_list': class_list})

def retrieveObjects(request):
    query = request.POST.get("query", "")
    entries = Course.objects.filter(
        Q(title__icontains= query) |
        Q(instructor__icontains= query) |
        Q(description__icontains=query)
    ).distinct()
    return entries

def retrieveInstructor(request):
    query = request.POST.get("query", "")
    entries = Course.objects.filter(
        Q(instructor__icontains= query)
    ).distinct()

    return entries

def retrieveDepartment(request):
    query = request.POST.get("query", "")
    entries = Course.objects.filter(
        Q(description__icontains= query)
    ).distinct()

    return entries

def advanced_results(request):
    query = request.POST.get("query", "")
    value = request.POST.get("category", "")
    class_list = retrieveObjects(request)
    if value == "0":
        class_list = retrieveObjects(request)
    if value == "1":
        class_list = retrieveInstructor(request)
    if value == "2":
        class_list = retrieveDepartment(request)
    return render(request, 'searchResults.html', {'query': query, 'class_list': class_list})



def submit_review(request,class_name):
    diff = request.POST.get("time")
    cost = request.POST.get("cost")
    recommend = request.POST.get("recommend")
    comment = request.POST.get("comment")
    Review.objects.create(name=class_name, text=comment, author=request.user, pub_date=datetime.datetime.now(), cost = cost, difficulty=diff, recommend=recommend)
    return redirect(class_page, permanent=True, class_name = class_name)

def rate_course(request, class_name):
    course = Course.objects.filter(title=class_name)[0]
    return render(request, 'ratingInterface.html', {'name':class_name, 'course': course})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('search')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

