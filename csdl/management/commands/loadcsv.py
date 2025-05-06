import pandas as pd
from django.core.management.base import BaseCommand
from csdl.models import BaiViet, DuyetBaiViet, Media, BaiVietMedia, BaiVietLichDangBai, LichDangBai, BaiVietThe, The, \
    DanhMuc
from django.utils.dateparse import parse_date


class Command(BaseCommand):
    help = 'Load data from Excel file into the database'

    def handle(self, *args, **kwargs):
        # Đọc dữ liệu từ file Excel
        df_baiviet = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='BaiViet')
        df_duyetbaiviet = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx',
                                        sheet_name='DuyetBaiViet')
        df_media = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='Media')
        df_baivietmedia = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx',
                                        sheet_name='BaiVietMedia')
        df_baivietlichdangbai = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx',
                                              sheet_name='BaiVietLichDangBai')
        df_lichdangbai = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='LichDangBai')
        df_baivietthe = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='BaiVietThe')
        df_the = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='The')
        df_danhmuc = pd.read_excel('D:/LapTrinhWeb/BaiTap/Group9_CMS/tables_updated.xlsx', sheet_name='DanhMuc')

        # Chèn dữ liệu vào các bảng
        for index, row in df_baiviet.iterrows():
            BaiViet.objects.create(
                ma_bv=row['ma_bv'],
                ngay_dang=parse_date(str(row['ngay_dang'])),
                tieu_de=row['tieu_de'],
                noi_dung=row['noi_dung'],
                duong_dan=row['duong_dan'],
                tom_tat=row['tom_tat'],
                ma_nguoi_dung=row['ma_nguoi_dung'],
                ma_dm=row['ma_dm'],
                ma_the=row['ma_the']
            )

        for index, row in df_duyetbaiviet.iterrows():
            DuyetBaiViet.objects.create(
                ma_duyet=row['ma_duyet'],
                ngay_duyet=parse_date(str(row['ngay_duyet'])),
                trang_thai=row['trang_thai'],
                ghi_chu=row['ghi_chu'],
                ma_bai_viet=row['ma_bai_viet'],
                ma_nguoi_dung=row['ma_nguoi_dung']
            )

        for index, row in df_media.iterrows():
            Media.objects.create(
                ma_media=row['ma_media'],
                folder_name=row['folder_name'],
                file_name=row['file_name'],
                type_name=row['type_name'],
                size=row['size'],
                ma_nguoi_dung=row['ma_nguoi_dung']
            )

        for index, row in df_baivietmedia.iterrows():
            BaiVietMedia.objects.create(
                ma_bv=row['ma_bv'],
                ma_media=row['ma_media']
            )

        for index, row in df_baivietlichdangbai.iterrows():
            BaiVietLichDangBai.objects.create(
                ma_ldb=row['ma_ldb'],
                ma_bv=row['ma_bv'],
                ma_nguoi_dung=row['ma_nguoi_dung']
            )

        for index, row in df_lichdangbai.iterrows():
            LichDangBai.objects.create(
                ma_ldb=row['ma_ldb'],
                ngay_dang=parse_date(str(row['ngay_dang'])),
                do_uu_tien=row['do_uu_tien'],
                ngay_dong=parse_date(str(row['ngay_dong'])) if row['ngay_dong'] else None,
                ma_bv=row['ma_bv'],
                ma_nguoi_dung=row['ma_nguoi_dung']
            )

        for index, row in df_baivietthe.iterrows():
            BaiVietThe.objects.create(
                ma_bv=row['ma_bv'],
                ma_the=row['ma_the']
            )

        for index, row in df_the.iterrows():
            The.objects.create(
                ma_the=row['ma_the'],
                ten_the=row['ten_the'],
                so_ba_viet=row['so_ba_viet'],
                slug=row['slug']
            )

        for index, row in df_danhmuc.iterrows():
            DanhMuc.objects.create(
                ma_dm=row['ma_dm'],
                ten_dm=row['ten_dm'],
                slug=row['slug'],
                so_ba_viet=row['so_ba_viet'],
                parent_id=row['parent_id'],
                order_index=row['order_index']
            )

        self.stdout.write(self.style.SUCCESS('Data loaded successfully from the Excel file!'))
