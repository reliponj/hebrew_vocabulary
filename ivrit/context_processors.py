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
            "input": "Введите корень или глагол",

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

            "manage_sub": "Управлять подпиской",

            "profile_change": "Изменить профиль",
            "change": "Изменить",

            "profile": "Профиль",
            "you_subscribe": "Вы купили доступ",
            "buy": "Купить",
            "free_until": "Бесплатно до",
            "welcome": "Корни иврита",
            "sub_expired": "Ваш пробный период истек!",

            "privacy_policy": "Политика конфиденциальности",
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
            "input": "Введіть корінь або дієслово",

            "login_account": "Увійти до облікового запису",
            "enter_email": "Введіть email",
            "enter_password": "Введіть пароль",
            "sign_up": "Немає облікового запису? Реєстрація",

            "sign_up_account": "Реєстрація",
            "login": "Є акаунт? Увійти",
            "login_enter": "Увійти",
            "logout": "Вийти",

            "subscription_status": "Статус підписки",
            "status_sub": "Статус: Активна",
            "status_not_sub": "Статус: Неактивна",
            "active_to": "Активна до",
            "continue_sub": "Продовжити",
            "trial": 'Спробувати 30 днів безкоштовно',
            "home": "На головну",

            "manage_sub": "Керувати підпискою",

            "profile_change": "Змінити профіль",
            "change": "Змінити",

            "profile": "Профіль",
            "you_subscribe": "Ви купили доступ",
            "buy": "Купити",
            "free_until": "Безкоштовно до",
            "welcome": "Коріння івриту",
            "sub_expired": "Ваш пробний період минув!",
            "privacy_policy": "Політика конфіденціальності",
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
            "input": "Enter root or verb",

            "login_account": "Login to account",
            "enter_email": "Enter email",
            "enter_password": "Enter password",
            "sign_up": "No account? Register",

            "sign_up_account": "Registration",
            "login": "Have an account? Log in",
            "login_enter": "Login",
            "logout": "Logout",

            "subscription_status": "Subscription status",
            "status_sub": "Status: Active",
            "status_not_sub": "Status: Inactive",
            "active_to": "Active to",
            "continue_sub": "Continue",
            "trial": 'Try 30 days free',
            "home": "Home",

            "manage_sub": "Manage subscription",

            "profile_change": "Change profile",
            "change": "Change",

            "profile": "Profile",
            "you_subscribe": "You have purchased access",
            "buy": "Buy",
            "free_until": "Free until",
            "welcome": "Hebrew roots",
            "sub_expired": "Your trial period has expired!",

            "privacy_policy": "Privacy Policy",
        }
    }

    settings = Setting.get_settings()

    context = {
        'locale': locales[language],
        "language": language,
        "settings": settings,
    }
    return context
