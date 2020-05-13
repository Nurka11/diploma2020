from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from mon_app.models import Match

import json


@csrf_exempt
def api_match_id(request, id):
    # ПОЛУЧИТЬ СРАВНЕНИЕ ПО id
    if request.method == "GET":
        match = Match.objects.get(id=id)
        match_json = {"id": match.id,
                      "status": match.status,
                      "created": match.created,
                      "name_competitor": match.name_competitor,
                      "name_my": match.name_my,
                      "price_competitor": match.price_competitor,
                      "price_my": match.price_my,
                      "diff": match.diff,
                      "shop_competitor": match.shop_competitor,
                      "url": match.url,
                      }
        return JsonResponse(match_json, safe=False)

    # ИЗМЕНИТЬ СРАВНЕНИЕ C УКАЗАННЫМ id
    if request.method == "PUT":
        match = Match.objects.filter(id=id)
        updated_match = json.loads(request.body)
        updated_match_url = updated_match.get('url')
        match.update(status=updated_match.get('status'),
                     created=updated_match.get('created'),
                     name_competitor=updated_match.get('name_competitor'),
                     name_my=updated_match.get('name_my'),
                     price_competitor=updated_match.get('price_competitor'),
                     price_my=updated_match.get('price_my'),
                     diff=updated_match.get('diff'),
                     shop_competitor=updated_match.get('shop_competitor'),
                     url=updated_match_url
                     )
        updated_match = Match.objects.get(id=id)
        return JsonResponse({"updated": 1,
                             "status": updated_match.status,
                             "created": updated_match.created,
                             "name_competitor": updated_match.name_competitor,
                             "name_my": updated_match.name_my,
                             "price_competitor": updated_match.price_competitor,
                             "price_my": updated_match.price_my,
                             "diff": updated_match.diff,
                             "shop_competitor": updated_match.shop_competitor,
                             "url": updated_match.url,
                             }, safe=False)

    # УДАЛИТЬ СРАВНЕНИЕ С УКАЗАННЫМ id
    if request.method == "DELETE":
        deleted_match = Match.objects.get(id=id)
        deleted_match.delete()
        return JsonResponse({
            "deleted": 1,
            "id": deleted_match.id,
            "status": deleted_match.status,
            "created": deleted_match.created,
            "name_competitor": deleted_match.name_competitor,
            "name_my": deleted_match.name_my,
            "price_competitor": deleted_match.price_competitor,
            "price_my": deleted_match.price_my,
            "diff": deleted_match.diff,
            "shop_competitor": deleted_match.shop_competitor,
            "url": deleted_match.url,
        })


@csrf_exempt
def api_match(request):
    # ДОБАВИТЬ НОВОЕ СРАВНЕНИЕ
    if request.method == "POST":
        new_match = json.loads(request.body)
        new_match_url = new_match.get('url')
        match, posted = Match.objects.get_or_create(url=new_match_url,
                                                    defaults={'status': new_match.get('status'),
                                                              'created': new_match.get('created'),
                                                              'name_competitor': new_match.get('name_compeetitor'),
                                                              'name_my': new_match.get('name_my'),
                                                              'price_competitor': new_match.get('price_competitor'),
                                                              'price_my': new_match.get('price_my'),
                                                              'diff': new_match.get('diff'),
                                                              'shop_competitor': new_match.get('shop_competitor'),
                                                              'url': new_match.get('url')
                                                              })
        return JsonResponse({"posted": 1,
                             "id": match.id,
                             "status": match.status,
                             "created": match.created,
                             "name_competitor": match.name_competitor,
                             "name_my": match.name_my,
                             "price_competitor": match.price_competitor,
                             "price_my": match.price_my,
                             "diff": match.diff,
                             "shop_competitor": match.shop_competitor,
                             "url": match.url,
                             }, safe=False)

    # ПОЛУЧИТЬ ВСЕ СРАВНЕНИЯ
    if request.method == "GET":
        matches = Match.objects.all()
        matches_json = [{"id": match.id,
                         "status": match.status,
                         "created": match.created,
                         "name_competitor": match.name_competitor,
                         "name_my": match.name_my,
                         "price_competitor": match.price_competitor,
                         "price_my": match.price_my,
                         "diff": match.diff,
                         "shop_competitor": match.shop_competitor,
                         "url": match.url,
                         }
                        for match in matches]
        return JsonResponse(matches_json, safe=False)
