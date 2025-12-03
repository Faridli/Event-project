from django.shortcuts import render

# Create your views here.

def Event(request):
    return render(request, 'text.html')