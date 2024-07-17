import openpyxl
from django.core.management import BaseCommand

from ivrit.models import Vocabulary, Root, Binyan, Spisok6, Group


def import_vocabulary():
    vocabulary = Vocabulary.objects.filter()

    roots = {}
    for v in vocabulary:
        if not v.link:
            continue

        if v.root not in roots.keys():
            roots[v.root] = {}
            roots[v.root]['binyans'] = []

        if v.binyan:
            roots[v.root]['binyans'].append({"binyan": v.binyan, "link": v.link})

    for root_key in roots.keys():
        root = Root(root=root_key)
        root.save()

        for binyan in roots[root_key]['binyans']:
            binyan_obj = Binyan(root=root, binyan=binyan['binyan'], link=binyan['link'])
            binyan_obj.save()


def import_spisok_6():
    spisok6 = Spisok6.objects.filter()
    for spisok in spisok6:
        root = Root.objects.filter(root=spisok.roots)
        if not root:
            print(spisok.roots)
            print('NOT FOUND')
            continue

        root = root.first()
        if root.groups.all():
            continue

        group_name = spisok.tables_2.split('-')[0]
        group = Group.objects.filter(group=group_name)
        if not group:
            group = Group(group=group_name)
            group.save()
        else:
            group = group.first()

        group.roots.add(root)
        root.number = spisok.tables
        root.save()


def import_roots_new():
    Group.objects.all().delete()
    Root.objects.all().delete()
    Binyan.objects.all().delete()

    spisok6 = Spisok6.objects.filter()
    for spisok in spisok6:
        root = Root(
            root=spisok.roots,
            number=spisok.tables)
        root.save()

        group_name = spisok.tables_2.split('-')[0]
        group = Group.objects.filter(group=group_name)
        if not group:
            group = Group(group=group_name)
            group.save()
        else:
            group = group.first()
        group.roots.add(root)


def import_vocabulary_new():
    vocabulary = Vocabulary.objects.filter()

    for v in vocabulary:
        if not v.link:
            continue

        root = Root.objects.filter(root=v.root).first()
        if not root:
            root = Root(
                root=v.root,
                number=100000)
            root.save()

        if v.binyan:
            binyan_obj = Binyan(root=root, binyan=v.binyan, link=v.link)
            binyan_obj.save()


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        import_roots_new()
        import_vocabulary_new()
        # import_vocabulary()
        # import_spisok_6()
