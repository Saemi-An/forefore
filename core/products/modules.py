from django.shortcuts import get_object_or_404
from urllib.parse import urlparse

from .models import Cookies, Sales


def get_cookie_sales():
    # sale, created = Sales.objects.get_or_create(id=1)  # 테스트 필요
    cookie_salse = get_object_or_404(Sales, pk=1).on_sale
    return cookie_salse

# 현재 사용 안함
def match_category_from_int_to_str(int_type):
    if int_type == 0:
        return 'financier'
    elif int_type == 1:
        return 'cakepiece'
    elif int_type == 2:
        return 'scone'
    elif int_type == 3:
        return 'todays-menu'
    
def match_category_from_str_to_int(str_type):
    if str_type == 'financier':
        return 0
    elif str_type == 'cakepiece':
        return 1
    elif str_type == 'scone':
        return 2
    elif str_type == 'todays-menu':
        return 3
    else:
        return 100

def change_cookie_index(idx, target_idx):
    if Cookies.objects.filter(index=target_idx):
        Cookies.objects.filter(index=idx).update(index=1000)
        Cookies.objects.filter(index=target_idx).update(index=idx)
        Cookies.objects.filter(index=1000).update(index=target_idx)
        return True
    else:
        return False

def get_referer(request, fallback):
    referer = request.META.get('HTTP_REFERER', f'/{fallback}/')
    
    # 보안: 호스트가 동일할 경우에만 사용
    parsed = urlparse(referer)
    if parsed.netloc and parsed.netloc != request.get_host():
        referer = f'/{fallback}/'

    return referer