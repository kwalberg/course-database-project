from django.shortcuts import render
from .models import Course, Review
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import datetime

# Create your views here.

#
def getCatalog(request):
    return render(request,'Catalog.html', {'class_list': Course.objects.all()})

def FrontPage(request):
    most_popular = Course.objects.all()[0:3]
    return render(request, 'FrontPage.html', {'most_popular': most_popular})

def class_page(request, class_name):
    c = Course.objects.filter(course_id=class_name)[0]
    review_list = Review.objects.filter(course=c)[::-1]
    course = Course.objects.filter(course_id=class_name)[0]
    return render(request, 'classPage.html', {'course': course, 'review_list': review_list})

def search_results(request):
    query = request.POST.get("query", "")
    category = request.POST.get("category")
    class_list = retrieveObjects(request)
    return render(request, 'searchResults.html', {'query': query, 'class_list': class_list})

def retrieveObjects(request):
    query = request.POST.get("query", "")
    entries = Course.objects.filter(
        Q(course_id__icontains= query) |
        Q(instructor__icontains= query) |
        Q(full_title__icontains=query)
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
        Q(department__icontains= query)
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
    workload = request.POST.get("time")
    diff = request.POST.get("diff")
    has_book = request.POST.get("book")
    recommend = request.POST.get("recommend")
    comment = request.POST.get("comment")
    c = Course.objects.filter(course_id=class_name)[0]
    Review.objects.create(course=c, text=comment, author=request.user, pub_date=datetime.datetime.now(), has_book = has_book, workload = workload, test_difficulty=diff, recommend=recommend)
    return redirect(class_page, permanent=True, class_name = class_name)

def rate_course(request, class_name):
    if request.user.is_authenticated:
        course = Course.objects.filter(course_id=class_name)[0]
        return render(request, 'ratingInterface.html', {'name':class_name, 'course': course})
    else:
        return redirect(f"/login/?next={request.path}")

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

