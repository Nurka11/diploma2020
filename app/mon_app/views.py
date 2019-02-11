from django.shortcuts import render
# from .yamarket import main
from .mvideo import mvideo


def index(request):
    return render(request, 'yam_app/index.html')


def parsing(request):
    if request.method == 'GET':
        return render(request, 'yam_app/index.html')
    elif request.method == 'POST':
        url_target = request.POST.get('url_target')
        page_count = request.POST.get('page_count')
        if url_target and page_count:
            mvideo(url_target, page_count)
            return render(request, 'yam_app/success.html')
