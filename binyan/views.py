import re

from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render, redirect

from binyan.models import BinyanInApp
from binyan.schemas import BinyanInAppSchema
from ivrit.models import Spisok1
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

    data = [VocabularySchema.from_orm(item).dict() for item in vocabulary]
    return JsonResponse(data, safe=False)


def verb_by_search(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    value = request.GET.get('search')
    language = request.GET.get('language')
    vocabulary = []
    if value:
        value = value.strip().lower()
        vocabulary = get_vocabulary()

        order_by = "words"
        first_filter = None
        second_filter = None
        third_filter = None
        if language == 'ru':
            order_by = 'word'
            first_filter = Q(word=value)
            second_filter = Q(word__icontains=value) & (Q(word__icontains=',') |
                                                        Q(word__icontains='.') |
                                                        Q(word__icontains=';') |
                                                        Q(word__icontains='='))
            # third_filter = Q(word__icontains=value)
        elif language == 'ua':
            order_by = 'word_u'
            first_filter = Q(word_u__istartswith=value[0], word_u__icontains=value)
            second_filter = Q(word_u__icontains=value) & (Q(word_u__icontains=',') |
                                                          Q(word_u__icontains='.') |
                                                          Q(word_u__icontains=';') |
                                                          Q(word_u__icontains='='))
            # second_filter = Q(word_u__regex=r'\b{}\b'.format(value))
            # third_filter = Q(word__icontains=value)
        elif language == 'en':
            order_by = 'word_a'
            first_filter = Q(word_a__istartswith=value[0], word_a__icontains=value)
            second_filter = Q(word_a__icontains=value) & (Q(word_a__icontains=',') |
                                                          Q(word_a__icontains='.') |
                                                          Q(word_u__icontains=';') |
                                                          Q(word_u__icontains='='))
            # second_filter = Q(word_a__regex=r'\b{}\b'.format(value))
            # third_filter = Q(word__icontains=value)

        check = []
        if first_filter:
            check = list(vocabulary.filter(first_filter).order_by(Lower(order_by)))
            second_filtered = vocabulary.filter(second_filter).order_by(Lower(order_by))
            for filtered in second_filtered:
                if language == 'ru':
                    word = filtered.word
                elif language == 'ua':
                    word = filtered.word_u
                elif language == 'en':
                    word = filtered.word_a

                print(word)
                word = re.sub(r'\d+', '', word)
                word = word.replace(';', ',')
                word = word.replace('=', ',')
                word = word.replace('.', ',')
                print(word)

                check_split = word.split(',')

                for check_split_word in check_split:
                    if check_split_word.strip() == value:
                        if filtered not in check:
                            check.append(filtered)

                # if filtered not in check:
                #     check.append(filtered)
            # third_filtered = vocabulary.filter(third_filter).order_by(Lower(order_by))
            # for filtered in third_filtered:
            #     if filtered not in check:
            #         check.append(filtered)

        if not check:
            if '.' not in value:
                spisok1 = Spisok1.objects.filter(Q(words=value) |
                                                 Q(word=value)).order_by('links')

                for spisok in spisok1:
                    voc = vocabulary.filter(root=spisok.roots, link=spisok.links)[:1]
                    for v in voc:
                        if v not in check:
                            v.infinitive = spisok.words
                            check.append(v)
            else:
                check = vocabulary.filter(root__icontains=value).order_by(Lower(order_by))

        vocabulary = check[:20]

    if not vocabulary:
        return JsonResponse({'verb': None}, safe=False)
    verb = vocabulary[0]
    binyan = BinyanInApp.objects.filter(binyan=verb.binyan).first()
    data = {'verb': VocabularySchema.from_orm(verb).dict(),
            'binyan': BinyanInAppSchema.from_orm(binyan).dict()}
    return JsonResponse(data, safe=False)
