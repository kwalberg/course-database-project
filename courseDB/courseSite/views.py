from django.shortcuts import render
from .models import Course


# Create your views here.
def index(request):
    return render(request,'searchBar.html',context={})

def class_page(request, class_name):
    course = Course.objects.filter(title=class_name)[0]
    return render(request, 'classPage.html', {'course': course})

def search_results(request):
    query = request.POST.get("query", "")
    class_list = retrieveObjects(request)
    return render(request, 'searchResults.html', {'query': query, 'class_list': class_list})

def retrieveObjects(request):
    query = request.POST.get("query", "")
    softwareDev = Course(title="Software Dev")
    entries = Course.objects.filter(title= query)
    return entries



