import json
import re

import openpyxl
from django.core.management import BaseCommand

from ivrit.models import Spisok1


def main():
    spisok1 = Spisok1.objects.filter()

    for spisok in spisok1:
        niqqud_pattern = re.compile(r"[\u0591-\u05C7]")
        new_word = niqqud_pattern.sub("", spisok.word)

        if new_word != spisok.word:
            spisok.word = new_word
            spisok.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        main()
