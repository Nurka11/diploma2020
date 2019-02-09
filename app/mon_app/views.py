from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as BS
import csv
from .models import Item
from .yamarket import main


def index(request):
    # main()
    return render(request, 'yam_app/index.html')


def parsing(request):
    main()
    return render(request, 'yam_app/success.html')
