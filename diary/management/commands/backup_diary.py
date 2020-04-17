import csv
import datetime
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import Diary


class Command(BaseCommand):
    help = "Backup Diary data"

    def handle(self, *args, **options):
        # 実行時のYYYYMMDDを取得
        date = datetime.date.today().strftime("%Y%m%d")

        # 保存ファイルの相対パス
        file_path = settings.BACKUP_PATH + 'diary_' + date + '.csv'

        # 保存ディレクトリが存在しなければ作成
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        # バックアップファイルの作成
        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            # ヘッダーの書き込み
            header = [field.name for field in Diary._meta.fields]
            writer.writerow(header)

            # Diaryテーブルの全データを取得
            diaries = Diary.objects.all()

            # データ部分の書き込み
            for diary in diaries:
                writer.writerow([str(diary.user),
                                 diary.title,
                                 diary.content,
                                 str(diary.photo1),
                                 str(diary.photo2),
                                 str(diary.photo3),
                                 str(diary.created_at),
                                 str(diary.updated_at)])

        # 保存ディレクトリのファイルリストを取得
        files = os.listdir(settings.BACKUP_PATH)
        # ファイルが設定数以上あったら一番古いファイルを削除
        if len(files) >= settings.NUM_SAVED_BACKUP:
            files.sort()
            os.remove(settings.BACKUP_PATH + files[0])