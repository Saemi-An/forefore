from django.shortcuts import get_object_or_404
from urllib.parse import urlparse
from django.core.paginator import Paginator

from .models import Cookies, Sales

# ==============================================================
# *************************** 공통 ***************************
# ==============================================================

def get_referer(request, fallback):
    referer = request.META.get('HTTP_REFERER', f'/{fallback}/')
    
    # 보안: 호스트가 동일할 경우에만 사용
    parsed = urlparse(referer)
    if parsed.netloc and parsed.netloc != request.get_host():
        referer = f'/{fallback}/'

    return referer

def get_paginated_objects(request, queryset):
    page = request.GET.get('page', '1')   # url에서 page값 가져옴(index의 경우 디폴트 '1')
    paginator = Paginator(queryset, 10)   # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)   # 해당 페이지의 데이터만 조회하도록 쿼리 (데이터 전체 조회 X)
    return page_obj


# ==============================================================
# *************************** 구움과자 ***************************
# ==============================================================

def get_cookie_sales():
    # sale, created = Sales.objects.get_or_create(id=1)  # 테스트 필요
    cookie_salse = get_object_or_404(Sales, pk=1).on_sale
    return cookie_salse
    
def match_category_from_str_to_int(str_type):
    if str_type == 'financier':
        return 1
    elif str_type == 'cakepiece':
        return 2
    elif str_type == 'scone':
        return 3
    elif str_type == 'todays-menu':
        return 4
    elif str_type == 'all':
        return 0

def change_cookie_index(idx, target_idx):
    if Cookies.objects.filter(index=target_idx):
        Cookies.objects.filter(index=idx).update(index=1000)
        Cookies.objects.filter(index=target_idx).update(index=idx)
        Cookies.objects.filter(index=1000).update(index=target_idx)
        return True
    else:
        return False


# ==============================================================
# *************************** 홀케이크 ***************************
# ==============================================================
def get_cakes_sales():
    # sale, created = Sales.objects.get_or_create(id=1)  # 테스트 필요
    cakes_sales = get_object_or_404(Sales, pk=2).on_sale
    return cakes_sales

def match_type_from_str_to_int(str_type):
    if str_type == 'size':
        return 1
    elif str_type == 'add_fruite':
        return 2
    elif str_type == 'mix_fruite':
        return 3
    elif str_type == 'change_cream':
        return 4
    elif str_type == 'change_sheet':
        return 5
    elif str_type == 'choco_glassage':
        return 6
    elif str_type == 'all':
        return 0