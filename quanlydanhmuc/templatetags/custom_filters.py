# from django import template
#
# register = template.Library()
#
# @register.filter
# def get_item(dictionary, key):
#     """
#     Lấy giá trị từ dictionary theo key
#     Sử dụng trong template: {{ my_dict|get_item:key }}
#     """
#     return dictionary.get(key)
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Lấy giá trị từ dictionary theo key
    Sử dụng trong template: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key)
