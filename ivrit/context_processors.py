from ivrit.models import Setting


def context_controller(request):
    language = request.GET.get('language', 'ru')
    locales = {
        "ru": {
            "site_name": "Корни глаголов",
            "binyans": "Биньяны",
            "by_time": "По временам",
                       
            "all_table": "вся таблица",
            "present": "настоящее время",
            "past": "прошедшее время",
            "future": "будущее время",
            "naklon": "повелительное наклонение",

            "infinitive": "инфинитив",
            "all_groups": "все",
            "by_groups": "по групам",

            "find": "Найти",
            "input": "Введите корень или глагольную форму",

            "login_account": "Войти в аккаунт",
            "enter_email": "Введите email",
            "enter_password": "Введите пароль",
            "sign_up": "Нет аккаунта? Регистрация",
            
            "sign_up_account": "Регистрация",
            "login": "Есть аккаунт? Войти",
            "login_enter": "Войти",
            "logout": "Выйти",

            "subscription_status": "Статус подписки",
            "status_sub": "Статус: Активна",
            "status_not_sub": "Статус: Неактивна",
            "active_to": "Активна до",
            "continue_sub": "Продлить",
            "trial": 'Попробовать 30 дней бесплатно',
            "home": "На главную",

            "manage_sub": "Управлять подпиской"
        },
        "ua": {
            "site_name": "Корені дієслів",
            "binyans": "Біньяни",
            "by_time": "За часами",
            "all_table": "вся таблиця",
            "present": "теперішній час",
            "past": "минулий час",
            "future": "майбутній час",
            "naklon": "наказовий спосіб",
            "infinitive": "інфінітив",
            "all_groups": "всі",
            "by_groups": "за групами",
            "find": "Знайти",
            "input": "Введіть корінь або дієслівну форму",
        },
        "en": {
            "site_name": "Verb Roots",
            "binyans": "Binyans",
            "by_time": "By Tenses",
            "all_table": "whole table",
            "present": "present tense",
            "past": "past tense",
            "future": "future tense",
            "naklon": "imperative mood",
            "infinitive": "infinitive",
            "all_groups": "all",
            "by_groups": "by groups",
            "find": "Find",
            "input": "Enter root or verb form",
        }
    }

    settings = Setting.get_settings()

    context = {
        'locale': locales[language],
        "language": language,
        "settings": settings,
    }
    return context
