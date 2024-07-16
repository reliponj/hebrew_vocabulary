from django.core.management import BaseCommand

from ivrit.models import RCategory

data = [
    ['a', 'שֵם הַפּוֹעַל'],

    ['b', 'אֲנִי, אַתָה, הוּא'],
    ['c', 'אֲנִי, אַת, הִיא'],
    ['d', 'אֲנַחנוּ, אַתֶם, הֵם'],
    ['e', 'אֲנַחנוּ, אַתֶן, הֵן'],

    ['f', 'אֲנִי'],
    ['g', 'אַתָה'],
    ['h', 'אַת'],
    ['i', 'הוּא'],
    ['j', 'הִיא'],
    ['k', 'אֲנַחנוּ'],
    ['l', 'אַתֶם'],
    ['m', 'אַתֶן'],
    ['n', 'הֵם, הֵן'],

    ['o', 'אֲנִי'],
    ['p', 'אַתָה'],
    ['q', 'אַת'],
    ['r', 'הוּא'],
    ['s', 'הִיא'],
    ['t', 'אֲנַחנוּ'],
    ['u', 'אַתֶם, אַתֶן'],
    ['v', 'הֵם, הֵן'],

    ['w', 'אַתָה'],
    ['x', 'אַת'],
    ['y', 'אַתֶם, אַתֶן'],
]


def main():
    for row in data:
        category = RCategory(
            r=row[0],
            description=row[1])
        category.save()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        main()

