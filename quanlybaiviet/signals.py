from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from csdl.models import BaiViet, DanhMuc, The


@receiver(post_delete, sender=BaiViet)
def update_counts_on_delete(sender, instance, **kwargs):
    """
    Cập nhật số lượng bài viết trong danh mục và thẻ khi xóa bài viết
    """
    # Giảm số lượng bài viết trong danh mục
    if instance.ma_dm:
        instance.ma_dm.so_bai_viet = max(0, instance.ma_dm.so_bai_viet - 1)
        instance.ma_dm.save()

    # Giảm số lượng bài viết trong thẻ
    if instance.ma_the:
        instance.ma_the.so_bai_viet = max(0, instance.ma_the.so_bai_viet - 1)
        instance.ma_the.save()
