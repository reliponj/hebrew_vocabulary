import json
import re

import openpyxl
from django.core.management import BaseCommand

from ivrit.models import Spisok1, Vocabulary


def main():
    spisok1 = Spisok1.objects.filter()

    for spisok in spisok1:
        if len(spisok.roots) > 1:
            if spisok.roots[-1] != '.':
                spisok.roots += '.'
                spisok.save()

    vocab = Vocabulary.objects.filter()

    for v in vocab:
        if len(v.root) > 1:
            if v.root[-1] != '.':
                v.root += '.'
                v.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        main()
