from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'searchBar.html',context={})

def class_page(request, class_name):

    return render(request, 'classPage.html', {'name': class_name})