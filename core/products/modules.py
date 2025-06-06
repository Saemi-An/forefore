from django.shortcuts import get_object_or_404

from .models import Cookies, Sales


def get_cookie_sales():
    # sale, created = Sales.objects.get_or_create(id=1)  # 테스트 필요
    cookie_salse = get_object_or_404(Sales, pk=1).on_sale
    return cookie_salse


def match_category_from_int_to_str(int_type):
    if int_type == 0:
        return 'financier'
    elif int_type == 1:
        return 'cakepiece'
    elif int_type == 2:
        return 'scone'
    elif int_type == 3:
        return 'todays-menu'


def change_cookie_index(idx, target_idx):
    if Cookies.objects.filter(index=target_idx):
        Cookies.objects.filter(index=idx).update(index=1000)
        Cookies.objects.filter(index=target_idx).update(index=idx)
        Cookies.objects.filter(index=1000).update(index=target_idx)
        return True
    else:
        return False
