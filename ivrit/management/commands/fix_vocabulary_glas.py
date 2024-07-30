import re

from django.core.management import BaseCommand

from ivrit.models import Vocabulary


class Command(BaseCommand):
    def handle(self, *args, **options):
        vocabulary = Vocabulary.objects.filter()
        for voc in vocabulary:
            niqqud_pattern = re.compile(r"[\u0591-\u05C7]")
            new_word = niqqud_pattern.sub("", voc.words1)
            voc.words2 = new_word

            if voc.words:
                new_word = niqqud_pattern.sub("", voc.words)
                voc.words_clear = new_word
                voc.save()
