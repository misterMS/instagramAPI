from django.shortcuts import render

# Create your views here.

def speed(request):
    return render(request,'Internet_Speed\speed.html')
