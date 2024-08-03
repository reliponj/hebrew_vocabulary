import re

import openpyxl
from django.core.management import BaseCommand

from ivrit.models import Kluch, Vocabulary


def import_vocabulary_by_kluch():
    kluchs = Kluch.objects.filter()
    i = 0

    vocs = Vocabulary.objects.filter(filter_for_app=True)
    for voc in vocs:
        voc.filter_for_app = False
        voc.save()

    for kluch in kluchs:
        i += 1
        vocabulary = Vocabulary.objects.filter(words=kluch.value)
        if not vocabulary:
            print(i)
            print(kluch.value)
            print("בְּעֶטיוֹ")
            continue

        for voc in vocabulary:
            voc.filter_for_app = True
            voc.save()

            vocabulary_2 = Vocabulary.objects.filter(root=voc.root)
            for voc2 in vocabulary_2:
                voc2.filter_for_app = True
                voc2.save()

    print(len(Vocabulary.objects.filter(filter_for_app=True)))


class Command(BaseCommand):
    def handle(self, *args, **options):
        wb = openpyxl.load_workbook('kluch.xlsx')
        ws = wb.active

        Kluch.objects.filter().delete()
        niqqud_pattern = re.compile(r"[\u0591-\u05C7]")
        for i in range(2, 100):
            value = ws.cell(row=i, column=1).value
            if not value:
                continue

            # value = niqqud_pattern.sub("", value)
            if '_' in value:
                value = value.split('_')[0]

            kluch = Kluch(value=value)
            kluch.save()

        import_vocabulary_by_kluch()
