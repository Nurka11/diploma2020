from django.shortcuts import render
# from .monarket import main
from .mvideo import mvideo
from .citilink import citilink


def index(request):
    return render(request, 'mon_app/index.html')


def parsing(request):
    if request.method == 'GET':
        return render(request, 'mon_app/index.html')
    elif request.method == 'POST':
        url_target = request.POST.get('url_target')
        page_count = request.POST.get('page_count')
        if url_target and page_count:
            citilink(url_target, page_count)
            return render(request, 'mon_app/success.html')
