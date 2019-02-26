from django.http import JsonResponse
from django.shortcuts import render

from .parsers.mvideo import mvideo
from .parsers.citilink import citilink
from .parsers.wildberries import wildberries
from .models import *
from django.views.decorators.csrf import csrf_exempt

import re


def index(request):
    return render(request, 'mon_app/index.html')


def support(request):
    return render(request, 'mon_app/support/support.html')


def other(request):
    return render(request, 'mon_app/other/other.html')


def parsing(request):
    if request.method == 'GET':
        return render(request, 'mon_app/index.html')
    elif request.method == 'POST':
        url_target = request.POST.get('url_target')
        page_count = request.POST.get('page_count')

        # Check if there is a url_target and page_count
        if url_target and page_count:

            # Checking valid of page_count
            if re.match(r'\d\b', page_count) and not re.match('0', page_count):

                # If target_url - mvideo
                if re.match('https://www.mvideo.ru/', url_target):
                    mvideo(url_target, page_count)

                # If target_url - citilink
                elif re.match('https://www.citilink.ru/', url_target):
                    citilink(url_target, page_count)

                # If target_url - citilink
                elif re.match('https://www.wildberries.ru/', url_target):
                    wildberries(url_target, page_count)

                # If target_url invalid
                else:
                    return render(request, 'mon_app/exceptions/invalid_url.html')

            # If page_count invalid
            else:
                return render(request, 'mon_app/exceptions/invalid_page_count.html')

        # If page_count doesn`t exist
        elif url_target and not page_count:
            return render(request, 'mon_app/exceptions/not_page_count.html')

        # If url_target doesn`t existstatus_true
        elif page_count and not url_target:
            return render(request, 'mon_app/exceptions/not_url_target.html')

        # If nothing exist
        else:
            return render(request, 'mon_app/exceptions/not_arguments.html')

        return render(request, 'mon_app/success.html', context={'url_target': url_target,
                                                                'page_count': page_count})


@csrf_exempt
def api_get_or_post_productcompetitor(request):
    if request.method == "POST":
        new_product = request.get_json()
        product = CompetitorProduct.objects.create(id=new_product['id'],
                                                   name=new_product['name'])
        return JsonResponse(product, safe=False)

    if request.method == "GET":
        products = CompetitorProduct.objects.all()
        products_json = [{"id": product.id,
                          "name": product.name,
                          "price": product.price,
                          "categoryId": product.categoryId,
                          "categoryName": product.categoryName,
                          "vendorName": product.vendorName,
                          "groupId": product.groupId,
                          "url": product.url,
                          "status": product.status,
                          "shop": product.shop,
                          "created": product.created
                          }
                         for product in products]
        return JsonResponse(products_json, safe=False)


def api_get_productcompetitor_by_id(request, id):
    product = CompetitorProduct.objects.get(id=id)
    product_json = {"id": product.id,
                     "name": product.name,
                     "price": product.price,
                     "categoryId": product.categoryId,
                     "categoryName": product.categoryName,
                     "vendorName": product.vendorName,
                     "groupId": product.groupId,
                     "url": product.url,
                     "status": product.status,
                     "shop": product.shop,
                     "created": product.created
                     }
    return JsonResponse(product_json, safe=False)


def api_post_productcompetitor(request):
    if request.method == "POST":
        new_product = request.get_json()
        product = CompetitorProduct.objects.create(id=new_product['id'],
                                                   name=new_product['name'])
        return JsonResponse(product, safe=False)
