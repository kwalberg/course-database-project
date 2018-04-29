from .models import Course, Review
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import datetime
import random

# Create your views here.

def getCatalog(request):
    return render(request,'Catalog.html', {'class_list': Course.objects.all()})


def FrontPage(request):
    count = Course.objects.all().count()
    slice = random.random() * (count - 3)
    most_popular = Course.objects.all()[slice: slice+3]
    return render(request, 'FrontPage.html', {'most_popular': most_popular})


def scale_workload(w):
    scaled_dict = {'1': '1-3',
                   '2': '4-5',
                   '3': '6-7',
                   '4': '8-9',
                   '5': '10+'}
    return scaled_dict[str(w)]


def class_page(request, class_name):
    c = Course.objects.filter(course_id=class_name)[0]
    review_list = Review.objects.filter(course=c)[::-1]
    course = Course.objects.filter(course_id=class_name)[0]

    # Calculate average values for all metrics to be displayed on course pages
    recommended_percent = 0
    # Calculates number of times this individual metric was provided by a reviewer
    num_recommends = len([review.recommend is not None for review in review_list])
    for review in review_list:
        if review.recommend is not None:
            recommended_percent += review.recommend
    # Handle potential division by zero
    if num_recommends != 0:
        recommended_percent = int(round(recommended_percent*100/num_recommends,-1))

    enjoyed_teaching = 0
    num_teaching_rated = len([review.liked_teaching is not None for review in review_list])
    for review in review_list:
        if review.liked_teaching is not None:
            enjoyed_teaching += review.liked_teaching
    if num_teaching_rated != 0:
        enjoyed_teaching = int(round(enjoyed_teaching * 100 / num_teaching_rated, -1))

    overall_rating = 0
    num_ratings = len([review.ratings is not None for review in review_list])
    for review in review_list:
        if review.ratings is not None:
            overall_rating += review.ratings
    if num_ratings != 0:
        overall_rating = int(round(overall_rating / num_ratings))

    difficulty = 0
    num_diff_rated = len([review.test_difficulty is not None for review in review_list])
    for review in review_list:
        if review.test_difficulty is not None:
            difficulty += review.test_difficulty
    if num_diff_rated != 0:
        average_difficulty = int(round(difficulty / num_diff_rated))

    workload = 0
    num_workload_rated = len([review.workload is not None for review in review_list])
    for review in review_list:
        if review.workload is not None:
            workload += review.workload
    if num_workload_rated != 0:
        average_workload = int(round(workload / num_workload_rated))

    return render(request, 'classPage.html', {'course': course,
                                              'review_list': review_list,
                                              'percent_recommend': recommended_percent,
                                              'rating': overall_rating,
                                              'percent_enjoyed_teaching': enjoyed_teaching,
                                              'difficulty': average_difficulty,
                                              'workload': scale_workload(average_workload),
                                              'range_l': range(0,overall_rating), 'range_u': range(overall_rating, 5)})


def search_results(request):
    query = request.POST.get("query", "")
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
    c = Course.objects.filter(course_id=class_name)[0]
    # Create new review based on POST parameters
    Review.objects.create(course=c,
                          text=request.POST.get("comment"),
                          author=request.user,
                          pub_date=datetime.datetime.now(),
                          liked_teaching=request.POST.get("teaching"),
                          attendance=request.POST.get("attend"),
                          has_book=request.POST.get("book"),
                          workload=request.POST.get("time"),
                          test_difficulty=request.POST.get("diff"),
                          recommend=request.POST.get("recommend"),
                          ratings=request.POST.get("rating"))
    return redirect(class_page, permanent=True, class_name=class_name)


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

