from django.core.management.base import BaseCommand
import pandas as pd
from app01.models import Academic

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **kwargs):
        # 定义CSV文件的绝对路径
        csv_file_path = 'C:/Users/user/Desktop/112專題/django/app01/management/commands/academic_test.csv'
        
        df = pd.read_csv(csv_file_path, sep='@')

        

        # 使用Django的数据库设置来连接到数据库
        from django.db import connections
        connection = connections['default']

        # 将 DataFrame 写入数据库
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM app01_academic')  # 清空表
            for _, row in df.iterrows():
                cursor.execute(
                    'INSERT INTO app01_academic (topic, optionA, optionB, optionC, optionD, answer, year, topic_number) '
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    [row['topic'], row['optionA'], row['optionB'], row['optionC'], row['optionD'],
                     row['answer'], row['year'], row['topic_number']]
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully!'))
       

