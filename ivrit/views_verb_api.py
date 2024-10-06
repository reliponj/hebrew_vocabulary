from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import redirect

from ivrit.models import Root, Spisok1, Vocabulary, RCategory, Binyan
from ivrit.schemas import RootSchema, VocabularySchema, BinyanSchema, VerbSchema, RCategorySchema
from ivrit.views import get_sub_data


def get_roots():
    roots = Root.objects.filter(root__icontains='.').order_by('root')
    roots = roots.filter(~Q(groups=None))
    return roots


def get_vocabulary():
    roots = Root.objects.filter(root__icontains='.').order_by('root')
    # roots = get_roots()
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

        order_by = "words"
        first_filter = None
        second_filter = None
        third_filter = None
        if language == 'ru':
            order_by = 'word'
            first_filter = Q(word=value)
            second_filter = Q(word__icontains=value) & Q(word__icontains=',')
            third_filter = Q(word__icontains=value)
        elif language == 'ua':
            order_by = 'word_u'
            first_filter = Q(word_u__istartswith=value[0], word_u__icontains=value)
            second_filter = Q(word_u__icontains=value) & Q(word_u__icontains=',')
            # second_filter = Q(word_u__regex=r'\b{}\b'.format(value))
            third_filter = Q(word__icontains=value)
        elif language == 'en':
            order_by = 'word_a'
            first_filter = Q(word_a__istartswith=value[0], word_a__icontains=value)
            second_filter = Q(word_a__icontains=value) & Q(word_a__icontains=',')
            # second_filter = Q(word_a__regex=r'\b{}\b'.format(value))
            third_filter = Q(word__icontains=value)

        check = []
        if first_filter:
            check = list(vocabulary.filter(first_filter).order_by(Lower(order_by)))
            second_filtered = vocabulary.filter(second_filter).order_by(Lower(order_by))
            for filtered in second_filtered:
                if filtered not in check:
                    check.append(filtered)
            third_filtered = vocabulary.filter(third_filter).order_by(Lower(order_by))
            for filtered in third_filtered:
                if filtered not in check:
                    check.append(filtered)

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


def api_verb(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    word = request.GET.get('word')
    chosen_binyan = request.GET.get('binyan')

    vocabulary = get_vocabulary()
    word = vocabulary.filter(words1=word).first()
    root = Root.objects.filter(root=word.root).first()

    # BINYANS
    binyans = root.binyans.all()
    if not chosen_binyan:
        chosen_binyan = binyans.filter(binyan=word.binyan).first()
        if not chosen_binyan:
            chosen_binyan = binyans[0]
    else:
        chosen_binyan = binyans.filter(binyan=chosen_binyan).first()

    # R-CATEGORY
    r_categories, infinitives = get_sub_data(root, chosen_binyan, "all")

    binyans_list = [BinyanSchema.from_orm(item).dict() for item in binyans]
    r_categories_list = [RCategorySchema.from_orm(item).dict() for item in r_categories]
    verb_schema = VerbSchema(
        binyans=binyans_list,
        chosen_binyan=BinyanSchema.from_orm(chosen_binyan).dict(),
        infinitives=infinitives,
        main_form=r_categories_list[0],
        present=r_categories_list[1:5],
        past=r_categories_list[5:14],
        future=r_categories_list[14:22],
        naklon=r_categories_list[22:25],
    )
    return JsonResponse(verb_schema.dict(), safe=False)
