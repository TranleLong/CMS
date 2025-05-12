from django import template
from csdl.models import Menu, BaiViet

register = template.Library()


@register.inclusion_tag('menu.html')
def render_menu(menu_id):
    """
    Template tag để render menu
    Cách sử dụng: {% render_menu 1 %}
    """
    try:
        menu = Menu.objects.get(ma_menu=menu_id, trang_thai='Dang hoat dong')
        bai_viet_list = BaiViet.objects.filter(menu=menu).order_by('-ngay_dang')

        return {
            'menu': menu,
            'bai_viet_list': bai_viet_list
        }
    except Menu.DoesNotExist:
        return {
            'menu': None,
            'bai_viet_list': []
        }
