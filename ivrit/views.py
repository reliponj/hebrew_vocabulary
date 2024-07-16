from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from ivrit.models import Vocabulary, Root, RCategory, Spisok1


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])

        if not user:
            return render(request, 'login.html')
        else:
            auth.login(request, user)
            return redirect('index')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if not user:
            user = User.objects.create_user(request.POST['email'],
                                            request.POST['email'],
                                            request.POST['password'])
            auth.login(request, user)
            return redirect('index')
        else:
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user:
                auth.login(request, user)
                return redirect('index')

    return render(request, 'sign_up.html')


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_subscribe:
        return redirect('pay_status')

    chosen_filter = request.GET.get('group_filter', 'root')
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
            root = roots[0].root

    binyan = request.GET.get('binyan', None)
    chosen_root, chosen_word = get_root(root)
    if not chosen_root:
        chosen_binyan = None
    elif not binyan:
        chosen_binyan = chosen_root.binyans.filter().first()
    else:
        chosen_binyan = chosen_root.binyans.filter(binyan=binyan).first()

    scroll_to_root = False
    if chosen_filter == 'number':
        if not request.GET.get('root') and not request.GET.get('input_root'):
            roots = roots.order_by('number')
        else:
            group = chosen_root.groups.filter().first()
            if not group:
                roots = []
            else:
                scroll_to_root = True
                roots = roots.filter(groups__in=[group]).order_by('number')

    if not chosen_binyan:
        r_categories, infinitive = None, None
        modal = 'no_verb'
    else:
        r_categories, infinitive = get_sub_data(chosen_root, chosen_binyan, r_filter, language)

    context = {
        "chosen_filter": chosen_filter,
        "r_filter": r_filter,

        "roots": roots,
        "language": language,
        "infinitive": infinitive,

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


def get_root(root):
    spisok = Spisok1.objects.filter(word=root)
    if not spisok:
        spisok = Spisok1.objects.filter(roots=root)
        if not spisok:
            spisok = Spisok1.objects.filter(words=root)
            if not spisok:
                return None, None

    spisok = spisok.first()
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
