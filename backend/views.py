from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def sign_in_out(request):
    return render(request, "sign_in_out.html")
