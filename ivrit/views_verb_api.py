from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import redirect

from ivrit.models import Root, Vocabulary
from ivrit.schemas import RootSchema, VocabularySchema


def get_roots():
    roots = Root.objects.filter(root__icontains='.').order_by('root')
    roots = roots.filter(~Q(groups=None))
    return roots


def get_vocabulary():
    roots = get_roots()
    filter_roots = [item.root for item in roots]
    vocabulary = Vocabulary.objects.filter(root__in=filter_roots)
    return vocabulary


def api_root(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    roots = get_roots()
    roots_list = []
    for item in roots:
        schema = RootSchema.from_orm(item).dict()
        if schema not in roots_list:
            roots_list.append(schema)
    return JsonResponse(roots_list, safe=False)


def api_root_vocabulary_by_search(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    value = request.GET.get('search')
    language = request.GET.get('language')
    vocabulary = []
    if value:
        value = value.strip()

        vocabulary = get_vocabulary()

        check = None
        if language == 'ru':
            order_by = 'word'
            check = vocabulary.filter(Q(word__istartswith=value)).order_by(Lower(order_by))
        elif language == 'ua':
            order_by = 'word_u'
            check = vocabulary.filter(Q(word_u__istartswith=value)).order_by(Lower(order_by))
        elif language == 'en':
            order_by = 'word_a'
            check = vocabulary.filter(Q(word_a__istartswith=value)).order_by(Lower(order_by))
        if not check:
            order_by = 'words1'
            check = vocabulary.filter(Q(words__istartswith=value) |
                                      Q(words_clear__istartswith=value) |
                                      Q(words1__istartswith=value) |
                                      Q(words2__istartswith=value)).order_by(order_by).first()

        vocabulary = check
    vocabulary_list = [VocabularySchema.from_orm(item).dict() for item in vocabulary]
    return JsonResponse(vocabulary_list, safe=False)


def api_root_vocabulary_by_root(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    root = request.GET.get('root')
    vocabulary = []
    if root:
        root = Root.objects.filter(root=root).first()
        if root:
            vocabulary = get_vocabulary()
            result = vocabulary.filter(root__icontains=root).order_by('link')
            vocabulary = result

    vocabulary_list = [VocabularySchema.from_orm(item).dict() for item in vocabulary]
    return JsonResponse(vocabulary_list, safe=False)