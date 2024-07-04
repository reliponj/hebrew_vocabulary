import openpyxl
from django.core.management import BaseCommand

from ivrit.models import Spisok1


def main():
    wb = openpyxl.load_workbook('spisok1.xlsx')
    ws = wb.active

    Spisok1.objects.filter().delete()
    for i in range(2, 67000):
        roots = ws.cell(row=i, column=1).value
        if not roots:
            continue

        words = ws.cell(row=i, column=2).value
        word = ws.cell(row=i, column=3).value
        r = ws.cell(row=i, column=4).value
        links = ws.cell(row=i, column=5).value

        vocabulary = Spisok1(
            roots=roots,
            words=words,
            word=word,
            r=r,
            links=links)
        vocabulary.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        main()
