from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render, redirect

from binyan.models import BinyanInApp
from binyan.schemas import BinyanInAppSchema
from ivrit.schemas import VocabularySchema
from ivrit.views_verb_api import get_vocabulary


def binyans(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    binyan_list = BinyanInApp.objects.filter()
    response = [BinyanInAppSchema.from_orm(item).dict() for item in binyan_list]
    return JsonResponse(response, safe=False)


def verbs(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    binyan = request.GET.get('binyan')
    if binyan:
        binyan = BinyanInApp.objects.filter(binyan=binyan).first()
        if not binyan:
            return redirect('index')
    else:
        return redirect('index')

    vocabulary = get_vocabulary()
    vocabulary = vocabulary.filter(binyan=binyan)

    value = request.GET.get('value')
    language = request.GET.get('language')

    if language == 'ru':
        order_by = 'word'
        vocabulary = vocabulary.filter(Q(word__istartswith=value)).order_by(Lower(order_by))
    elif language == 'ua':
        order_by = 'word_u'
        vocabulary = vocabulary.filter(Q(word_u__istartswith=value)).order_by(Lower(order_by))
    elif language == 'en':
        order_by = 'word_a'
        vocabulary = vocabulary.filter(Q(word_a__istartswith=value)).order_by(Lower(order_by))

    data = [VocabularySchema.from_orm(item).dict() for item in vocabulary[:20]]
    return JsonResponse(data, safe=False)
