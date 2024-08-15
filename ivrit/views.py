from django.conf import settings
from django.db.models import Q
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.shortcuts import render, redirect

from ivrit.models import Vocabulary, Root, RCategory, Spisok1, Setting, Kluch
from ivrit.schemas import VocabularySchema, SettingsSchema, KluchSchema


def index(request):
    if not request.user.is_authenticated:
        return redirect('welcome')

    if not request.user.is_sub_active():
        return redirect('profile')

    chosen_filter = request.GET.get('group_filter', 'all')
    r_filter = request.GET.get('r_filter', 'all')
    language = request.GET.get('language', 'ru')
    modal = request.GET.get('modal', None)

    roots = Root.objects.filter(root__icontains='.').order_by('root')
    roots = roots.filter(~Q(groups=None))

    root = request.GET.get('root')
    input_root = request.GET.get('input_root', '')
    if not root:
        if input_root:
            root = input_root
        else:
            if chosen_filter == 'all':
                root = roots[0].root
            else:
                root = roots.order_by('number')[0]

    binyan = request.GET.get('binyan', None)
    chosen_root, chosen_word = get_root(root, chosen_filter)
    if not chosen_root:
        chosen_binyan = None
    elif not binyan:
        chosen_binyan = chosen_root.binyans.filter().first()
    else:
        chosen_binyan = chosen_root.binyans.filter(binyan=binyan).first()

    scroll_to_root = False
    if chosen_filter == 'number' and chosen_root:
        if not request.GET.get('root') and not request.GET.get('input_root'):
            roots = roots.order_by('number')
        else:
            group = chosen_root.groups.filter().first()
            if not group:
                roots = []
            else:
                if request.GET.get('root'):
                    scroll_to_root = True
                roots = roots.filter(groups__in=[group]).order_by('number')

    if not chosen_binyan:
        r_categories, infinitive = None, None
        modal = 'no_verb'
    else:
        r_categories, infinitive = get_sub_data(chosen_root, chosen_binyan, r_filter, language)

    infinitive_size = 16
    if infinitive and len(infinitive) > 10:
        infinitive_size = 12

    check_roots = []
    new_roots = []
    for root in roots:
        if root.root not in check_roots:
            check_roots.append(root.root)
            new_roots.append(root)

    context = {
        "chosen_filter": chosen_filter,
        "r_filter": r_filter,

        "roots": new_roots,
        "language": language,
        "infinitive": infinitive,
        "infinitive_size": infinitive_size,

        "chosen_root": chosen_root,
        "chosen_word": chosen_word,
        "chosen_binyan": chosen_binyan,
        "input_word": root,
        "input_root": input_root,

        "r_categories": r_categories,
        "modal": modal,
        "scroll_to_root": scroll_to_root,
    }
    return render(request, 'korny.html', context=context)


def privacy(request):
    return render(request, 'privacy.html')


def get_root(root, group_filter):
    spisok = Spisok1.objects.filter(word=root)
    if not spisok:
        spisok = Spisok1.objects.filter(roots=root)
        if not spisok:
            spisok = Spisok1.objects.filter(words=root)
            if not spisok:
                return None, None

    spisok = spisok.first()

    result_word = ''
    if group_filter != 'number':
        result_word = spisok.word

    root = Root.objects.filter(root=spisok.roots)
    if not root:
        return None, None
    root = root.first()
    return root, result_word


def change_filter(request, param, value):
    url = request.META.get('HTTP_REFERER')

    link = url.split('?')[0]
    params = url.split('?')
    if len(params) > 1:
        params = params[1]
    else:
        params = ''

    found = False
    new_params = []
    params = params.split('&')
    for param_string in params:
        if param in param_string:
            param_string = f'{param}={value}'
            found = True
            print(param_string)
        else:
            print('NOT FOUND')

        new_params.append(param_string)

    new_params = '&'.join(new_params)
    if not found:
        new_params += f'&{param}={value}'

    return redirect(link + '?' + new_params)


def get_sub_data(chosen_root, chosen_binyan, r_filter, language):
    spisok = Spisok1.objects.filter(links=chosen_binyan.link).first()
    same_links = Spisok1.objects.filter(links=spisok.links)

    r_categories = get_r_categories(r_filter)
    for category in r_categories:
        found = same_links.filter(r=category.r)
        if found:
            category.word = found.first().words
            category.word_simple = found.first().word
            category.word_size = 30
            if len(category.word_simple) > 5:
                category.word_size = 24
        else:
            category.word = ''
            category.word_simple = ''
            category.word_size = 30

    slovar = Vocabulary.objects.filter(root=chosen_root.root, binyan=chosen_binyan.binyan)
    if not slovar:
        return
    slovar = slovar.first()

    infinitive = ''
    if language == 'ru':
        infinitive = slovar.word
    if language == 'ua':
        infinitive = slovar.word_u
    if language == 'en':
        infinitive = slovar.word_a

    return r_categories, infinitive


def get_r_categories(r_filter):
    r_categories = RCategory.objects.filter()

    r_categories = list(r_categories)
    if r_filter == 'all':
        pass
    elif r_filter == '1':
        r_categories = [r_categories[0]] + r_categories[1:5]
    elif r_filter == '2':
        r_categories = [r_categories[0]] + r_categories[5:14]
    elif r_filter == '3':
        r_categories = [r_categories[0]] + r_categories[14:22]
    elif r_filter == '4':
        r_categories = [r_categories[0]] + r_categories[22:25]
    return r_categories


def api_settings(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    setting = Setting.get_settings()
    settings_data = SettingsSchema.from_orm(setting).dict()
    return JsonResponse(settings_data, safe=False)


def api_kluch(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    kluch = Kluch.objects.filter()
    kluch_list = [KluchSchema.from_orm(item).dict() for item in kluch]
    return JsonResponse(kluch_list, safe=False)


def api_vocabulary(request):
    token = request.GET.get('token')
    if token != settings.API_TOKEN:
        return redirect('index')

    value = request.GET.get('value')
    is_all_results = request.GET.get('is_all_results')
    language = request.GET.get('language')
    if value:
        value = value.strip()

        kluch = Kluch.objects.filter()
        kluch_roots = [item.root for item in kluch]
        vocabulary = Vocabulary.objects.filter(root__in=kluch_roots)

        check = None
        if language == 'ru':
            order_by = 'word'
            check = vocabulary.filter(Q(word__istartswith=value)).order_by(Lower(order_by)).first()
        elif language == 'ua':
            order_by = 'word_u'
            check = vocabulary.filter(Q(word_u__istartswith=value)).order_by(Lower(order_by)).first()
        elif language == 'en':
            order_by = 'word_a'
            check = vocabulary.filter(Q(word_a__istartswith=value)).order_by(Lower(order_by))
            # for v in check:
            #     print(v.word_a)
            check = check.first()

        if not check:
            order_by = 'words1'
            check = vocabulary.filter(Q(words__istartswith=value) |
                                      Q(words_clear__istartswith=value) |
                                      Q(words1__istartswith=value) |
                                      Q(words2__istartswith=value)).order_by(order_by).first()

        if is_all_results:
            if check:
                result = vocabulary.filter(root__icontains=check.root).order_by('link')
                vocabulary = result
            else:
                vocabulary = []
        else:
            if check:
                vocabulary = [check]
            else:
                vocabulary = []

        vocabulary_list = [VocabularySchema.from_orm(item).dict() for item in vocabulary]
    else:
        vocabulary_list = []
    return JsonResponse(vocabulary_list, safe=False)
