import os
import re
from django.core.management.base import BaseCommand
from app01.models import EnglishWord

class Command(BaseCommand):
    help = 'Import English words from CSV file'

    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, 'english_words.csv')

        with open(csv_file_path, 'r') as csv_file:
            for line in csv_file:
                match = re.match(r'^(.*?)@\(.*?\)(.*?)$', line)
                if match:
                    word = match.group(1).strip()
                    meaning = match.group(2).strip()
                    EnglishWord.objects.create(word=word, meaning=meaning)
                else:
                    print(f"Skipping line: {line.strip()}")
