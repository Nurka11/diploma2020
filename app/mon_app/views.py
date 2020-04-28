# standard imports
import random

# third-party imports
from chartjs.views.lines import BaseLineChartView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework import status

# django imports
from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

# local imports
from .parsers.mvideo import sulpak
from .parsers.citilink import alser
from .parsers.wildberries import mechta
from .models import CompetitorProduct
from .serializers import PrefixSerializer


import re


def index(request):
    return render(request, 'mon_app/index.html')


def support(request):
    return render(request, 'mon_app/support/support.html')


def parsing(request):
    if request.method == 'GET':
        return render(request, 'mon_app/index.html')
    elif request.method == 'POST':
        url_target = request.POST.get('url_target')
        page_count = request.POST.get('page_count')

        # Check if there is a url_target and page_count
        if url_target and page_count:

            # Checking valid of page_count
            if re.match(r'\d\b', page_count) or re.match(r'\d\d\b', page_count) and not re.match('0', page_count):

                # If target_url - mvideo
                if re.match('https://www.sulpak.kz/', url_target):
                    sulpak(url_target, page_count)

                # If target_url - citilink
                elif re.match('https://alser.kz/', url_target):
                    alser(url_target, page_count)

                # If target_url - citilink
                elif re.match('https://www.mechta.kz/', url_target):
                    mechta(url_target, page_count)

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


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return [CompetitorProduct.Alser, CompetitorProduct.Sulpak, CompetitorProduct.Mechta, "другой"]

    def get_providers(self):
        """Return names of datasets."""
        product = get_object_or_404(CompetitorProduct.objects, pk=self.request.GET.get('id'))
        return [product.name]

    def get_data(self):
        """Return 3 datasets to plot."""
        prices = [None, None, None, None]
        conditions = [CompetitorProduct.Alser, CompetitorProduct.Sulpak, CompetitorProduct.Mechta]
        name = self.request.GET.get('name')
        products = CompetitorProduct.objects.filter(name=name)
        for product in products:
            for i in range(len(conditions)):
                if product.shop == conditions[i]:
                    prices[i] = int(product.price)
                    break
            if product.shop not in conditions:
                prices[3] = int(product.price)
        return [prices]


line_chart = TemplateView.as_view(template_name='some_grtaphic.html')
line_chart_json = LineChartJSONView.as_view()

@api_view(('GET',))
def get_with_prefix(request):
    word = request.GET.get('word')
    prefixes_arr = []
    prefixes_set = set()
    if word:
        prefix = CompetitorProduct.objects.filter(Q(name__icontains=word)).order_by('name')
        for p in prefix:
            if p.name not in prefixes_set:
                prefixes_set.add(p.name)
                prefixes_arr.append(p)
        serializer = PrefixSerializer(prefixes_arr, many=True)
        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response([], status.HTTP_200_OK)
            # return Response({}, status=status.HTTP_200_OK)
