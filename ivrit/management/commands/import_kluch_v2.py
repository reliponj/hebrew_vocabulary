from django.core.management import BaseCommand
from django.db.models import Q

from ivrit.models import Kluch, Vocabulary


def save_all_kluch():
    kluchs = Kluch.objects.filter()
    for kluch in kluchs:
        vocabulary = Vocabulary.objects.filter(Q(words=kluch.value) | Q(words_clear=kluch.value)).first()
        if not vocabulary:
            print(kluch.value)
            print('NOT FOUND')
            continue

        kluch.value_ru = vocabulary.word
        kluch.value_en = vocabulary.word_a
        kluch.value_ua = vocabulary.word_u
        kluch.root = vocabulary.root
        kluch.save()


class Command(BaseCommand):
    def handle(self, *args, **options):
        save_all_kluch()
