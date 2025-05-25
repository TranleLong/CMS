from django.core.management.base import BaseCommand
from django.db.models import Count
from csdl.models import DanhMuc, The, BaiViet


class Command(BaseCommand):
    help = 'Đồng bộ lại số lượng bài viết trong danh mục và thẻ'

    def handle(self, *args, **options):
        # Đồng bộ danh mục
        danh_mucs = DanhMuc.objects.all()
        for dm in danh_mucs:
            count = BaiViet.objects.filter(ma_dm=dm).count()
            dm.so_bai_viet = count
            dm.save()
            self.stdout.write(f'Danh mục "{dm.ten_dm}": {count} bài viết')

        # Đồng bộ thẻ
        thes = The.objects.all()
        for the in thes:
            count = BaiViet.objects.filter(ma_the=the).count()
            the.so_bai_viet = count
            the.save()
            self.stdout.write(f'Thẻ "{the.ten_the}": {count} bài viết')

        self.stdout.write(self.style.SUCCESS('Đồng bộ thành công!'))
