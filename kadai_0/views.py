from django.shortcuts import render
from django.http import HttpRespose

def index(request):
    return HttpRespose("ようこそ")