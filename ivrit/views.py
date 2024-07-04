from django.shortcuts import render, redirect

from ivrit.models import Vocabulary, Root, RCategory, Spisok1


def index(request):
    chosen_filter = request.GET.get('group_filter', 'root')
    r_filter = request.GET.get('r_filter', 'all')
    language = request.GET.get('language', 'ru')
    modal = request.GET.get('modal', None)

    roots = Root.objects.filter(root__icontains='.').order_by('root')
    root = request.GET.get('root')
    if not root:
        root = roots[0].root

    binyan = request.GET.get('binyan', None)
    chosen_root, root = get_root(root)
    if not chosen_root:
        return
    if not binyan:
        chosen_binyan = chosen_root.binyans.filter().first()
    else:
        chosen_binyan = chosen_root.binyans.filter(binyan=binyan).first()

    if chosen_filter == 'number':
        if not request.GET.get('root'):
            roots = roots.filter(group__lt=10000).order_by('number')
        else:
            roots = roots.filter(group=chosen_root.group).order_by('number')

    r_categories, infinitive = get_sub_data(chosen_root, chosen_binyan, r_filter, language)
    context = {
        "chosen_filter": chosen_filter,
        "r_filter": r_filter,

        "roots": roots,
        "language": language,
        "infinitive": infinitive,

        "chosen_root": chosen_root,
        "chosen_binyan": chosen_binyan,
        "input_word": root,

        "r_categories": r_categories,
        "modal": modal,
    }
    return render(request, 'korny.html', context=context)


def get_root(root):
    result_word = root
    spisok = Spisok1.objects.filter(word=root)
    if not spisok:
        spisok = Spisok1.objects.filter(roots=root)
        if not spisok:
            spisok = Spisok1.objects.filter(words=root)
            if not spisok:
                return None
    else:
        result_word = spisok.first().words

    spisok = spisok.first()
    root = Root.objects.filter(root=spisok.roots)
    if not root:
        return None
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
