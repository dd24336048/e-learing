import csv
import os
import logging
from django.core.management.base import BaseCommand
from app01.models import QuizQuestion

# 配置日志
logging.basicConfig(filename='import_log.txt', level=logging.INFO)

class Command(BaseCommand):
    help = 'Import quiz questions from a CSV file'

    def handle(self, *args, **options):
        # 获取当前脚本所在的目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 构建文件的绝对路径，这里使用 'english_bank.csv'，确保文件名大小写一致
        file_path = os.path.join(current_dir, 'english_bank.csv')

        # 打开文件
        with open(file_path, 'r') as csv_file:
            # 从文件中读取数据并导入到数据库中
            csv_reader = csv.reader(csv_file, delimiter='@')
            for row in csv_reader:
                try:
                    if len(row) == 5:
                        question_id, question_text, options, correct_answer, year = row
                        option_a, option_b, option_c, option_d = options.split()
                        quiz_question = QuizQuestion(
                            question_id=question_id,
                            question_text=question_text,
                            option_a=option_a,
                            option_b=option_b,
                            option_c=option_c,
                            option_d=option_d,
                            correct_answer=correct_answer,
                            year=year
                        )
                        quiz_question.save()
                        logging.info(f"Successfully imported question: {question_text}")
                    else:
                        logging.error(f"Invalid row format: {row}")
                except Exception as e:
                    logging.error(f"Error importing question: {e}")

