from django.http import JsonResponse
from django.shortcuts import render

from .parsers.mvideo import mvideo
from .parsers.citilink import citilink
from .parsers.wildberries import wildberries
from .models import *
from django.views.decorators.csrf import csrf_exempt

import re
import json


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
def api_productcompetitor_id(request, id):

    # ПОЛУЧИТЬ ТОВАР ПО id
    if request.method == "GET":
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

    # ИЗМЕНИТЬ ТОВАР C УКАЗАННЫМ id
    if request.method == "PUT":
        product = CompetitorProduct.objects.filter(id=id)
        new_product = json.loads(request.body)
        new_product_url = new_product.get('url')
        new_product_name = new_product.get('name')
        if new_product_url and new_product_name:
            updated = product.update(name=new_product_name,
                                     price=new_product.get('price'),
                                     categoryId=new_product.get('categoryId'),
                                     categoryName=new_product.get('categoryName'),
                                     vendorName=new_product.get('vendorName'),
                                     groupId=new_product.get('groupId'),
                                     url=new_product_url,
                                     status=new_product.get('status'),
                                     shop=new_product.get('shop'),
                                     created=new_product.get('created')
                                     )
            updated_product = CompetitorProduct.objects.get(id=id)
            return JsonResponse({"updated": updated,
                                 "id": updated_product.id,
                                 "name": updated_product.name,
                                 "price": updated_product.price,
                                 "categoryId": updated_product.categoryId,
                                 "categoryName": updated_product.categoryName,
                                 "vendorName": updated_product.vendorName,
                                 "groupId": updated_product.groupId,
                                 "url": updated_product.url,
                                 "status": updated_product.status,
                                 "shop": updated_product.shop,
                                 "created": updated_product.created
                                 }, safe=False)
        return JsonResponse({'err': True, 'message': 'Url or Name is lost'})

    # УДАЛИТЬ ТОВАР С УКАЗАННЫМ id
    if request.method == "DELETE":
        deleted_product = CompetitorProduct.objects.get(id=id)
        deleted_product.delete()
        return JsonResponse({
            "deleted": 1,
            "id": deleted_product.id,
            "name": deleted_product.name,
            "price": deleted_product.price,
            "categoryId": deleted_product.categoryId,
            "categoryName": deleted_product.categoryName,
            "vendorName": deleted_product.vendorName,
            "groupId": deleted_product.groupId,
            "url": deleted_product.url,
            "status": deleted_product.status,
            "shop": deleted_product.shop,
            "created": deleted_product.created
        })


@csrf_exempt
def api_productcompetitor(request):

    # ДОБАВИТЬ НОВЫЙ ТОВАР
    if request.method == "POST":
        new_product = json.loads(request.body)
        new_product_url = new_product.get('url')
        new_product_name = new_product.get('name')
        if new_product_url and new_product_name:
            product, posted = CompetitorProduct.objects.get_or_create(url=new_product_url,
                                                                      defaults={'name': new_product_name,
                                                                                'price': new_product.get('price'),
                                                                                'categoryId': new_product.get('categoryId'),
                                                                                'categoryName': new_product.get('categoryName'),
                                                                                'vendorName': new_product.get('vendorName'),
                                                                                'groupId': new_product.get('groupId'),
                                                                                'status': new_product.get('status'),
                                                                                'shop': new_product.get('shop'),
                                                                                'created': new_product.get('created')})
            return JsonResponse({"posted": posted,
                                 "id": product.id,
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
                                 }, safe=False)
        return JsonResponse({'err': True, 'message': 'Url or Name is lost'})

    # ПОЛУЧИТЬ ВСЕ ТОВАРЫ
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
