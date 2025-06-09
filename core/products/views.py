from urllib.parse import urlparse
from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CookieAdd, ProductAdd, TimeAdd
from .models import Cookies, Products, Sales, Times
from .modules import change_cookie_index, get_cookie_sales, match_category_from_str_to_int, get_referer, match_category_from_int_to_str


def cookies(request, category='all'):
    int_category = match_category_from_str_to_int(category)
    if int_category == 100:
        cookies = Cookies.objects.all().order_by('index')
    else:
        cookies = Cookies.objects.filter(product__category=int_category).order_by('index')

    sales = get_cookie_sales()
    times = Times.objects.all().order_by('name', 'start', 'end')
    selected_times = Times.objects.filter(selected=True).order_by('name', 'start', 'end')
    form = CookieAdd()

    context = {
        'filter': int_category,
        'cookies': cookies,
        'sales': sales,
        'times': times,
        'selected_times': selected_times,
        'form': form,
    }

    return render(request, 'products/cookies.html', context)

def change_cookies_sale(request):
    referer = get_referer(request, 'cookies')

    status = get_object_or_404(Sales, id=1)
    if status.on_sale:  # 판매중 --> 판매 종료
        # 알림: 사용자용 픽업시간 테이블 초기화, 관리자가 선택한 픽업시간 초기화
        # exclude(status=3): status = 0, current = 0
        # Times selected = False
        Cookies.objects.exclude(status=3).update(status=0, current=0)
        Times.objects.filter(selected=True).update(selected=False)
    
    else:   # 판매 종료 --> 판매 시작
        # 조건1: Times selected 최소 1개 이상일 것
        if not Times.objects.filter(selected=True):
            messages.error(request, '최소 1개의 픽업시간을 설정해 주세요.')
            return redirect(referer)
        else:
            # 알림: 안전재고 = 현재 재고로 시작, 판매중에 픽업시간 변경 불가
            # exclude(status=3): status = 1, current = self.safe
            cookies = Cookies.objects.exclude(status=3)
            for cookie in cookies:
                cookie.status = 1
                cookie.current = cookie.safe
                cookie.save()

    status.on_sale = not status.on_sale
    status.save()
    toast_msg = '시작' if status.on_sale else '종료'
    messages.success(request, f'구움과자 예약 판매가 {toast_msg} 되었습니다.')

    return redirect(referer)

def cookies_pickups_add(request):
    referer = get_referer(request, 'cookies')

    if request.method == 'POST':
        str_selected_times = request.POST['selected_times'].strip()   # '1 2 10'        
        id_list = list(map(int, str_selected_times.split())) if str_selected_times else []  # ['1', '2', '10'] --> [1, 2, 10]

        all_times = Times.objects.all().order_by('name')
        for time in all_times:
            if time.selected and time.id not in id_list:
                time.selected = False
                time.save()
            elif not time.selected and time.id in id_list:
                time.selected = True
                time.save()        

        # 시그널 트리거 안됨
        # Times.objects.filter(selected=True).exclude(id__in=id_list).update(selected=False)   # T --> F
        # Times.objects.filter(selected=False, id__in=id_list).update(selected=True)   # F --> T
        messages.success(request, f'픽업시간이 변경 되었습니다.')
        return redirect(referer)
    else:
        messages.error(request, f'잘못된 접근 경로 입니다.')
        return redirect(referer)
    
def change_cookies_index(request, idx, action):
    referer = get_referer(request, 'cookies')

    if action == 'up':
        target_idx = idx - 1
        if change_cookie_index(idx, target_idx):
            messages.success(request, '노출 순서가 변경 되었습니다.')
        else:
            messages.error(request, '더 이상 이동할 수 없습니다.')

    elif action == 'down':
        target_idx = idx + 1
        if change_cookie_index(idx, target_idx):
            messages.success(request, '노출 순서가 변경 되었습니다.')
        else:
            messages.error(request, '더 이상 이동할 수 없습니다.')
    
    return redirect(referer)

def cookies_view(request, pk):
    cookie = get_object_or_404(Cookies, id=pk)
    context = {'cookie': cookie}

    return render(request, 'products/cookies_view.html', context)

# add, edit 합쳐놓음
def cookies_add(request, pk=None):
    referer = get_referer(request, 'cookies')

    if request.method == 'POST':
        if pk:
            cookie = get_object_or_404(Cookies, id=pk)
            form = CookieAdd(request.POST, instance=cookie)
        else:
            form = CookieAdd(request.POST)

        if form.is_valid():
            valid_form = form.save(commit=False)
            if get_cookie_sales():
                valid_form.current = valid_form.safe
            else:
                valid_form.current = 0
            valid_form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')

    messages.error(request, f'잘못된 접근 경로 입니다.')
    return redirect(referer)

def cookies_delete(request, pk):
    referer = get_referer(request, 'cookies')
    cookie = get_object_or_404(Cookies, id=pk)
    cookie.delete()
    messages.success(request, '성공적으로 삭제 되었습니다.')
    return redirect(referer)


def cookies_products(request, category='all'):
    int_category = match_category_from_str_to_int(category)
    if int_category == 100:
        products = Products.objects.all().order_by('id')
    else:
        products = Products.objects.filter(category=int_category).order_by('id')

    if request.method == 'POST':
        int_category = int(request.POST['product_category'])
        products = Products.objects.filter(category=int_category).order_by('id')
        str_category = match_category_from_int_to_str(int_category)
        return redirect('cookies_products', str_category)

    context = {
        'products': products,
        'selected_category': int_category,
    }

    return render(request, 'products/cookies_products.html', context)


def cookies_products_view(request, pk):
    product = get_object_or_404(Products, id=pk)
    context = {'product': product}

    return render(request, 'products/cookies_products_view.html', context)


def cookies_products_add(request):
    form = ProductAdd()
    referer = get_referer(request, 'cookies-products')

    if request.method == 'POST':
        redirect_url = request.POST['redirect_url']
        
        form = ProductAdd(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)
    context = {'form': form, 'referer': referer}

    return render(request, 'products/cookies_products_add.html', context)


def cookies_products_edit(request, pk):
    product = get_object_or_404(Products, id=pk)
    form = ProductAdd(instance=product)
    referer = get_referer(request, 'cookies-products')

    if request.method == 'POST':
        redirect_url = request.POST['redirect_url']
        
        form = ProductAdd(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)

    context = {'form': form, 'product': product, 'referer': referer}

    return render(request, 'products/cookies_products_add.html', context)


def cookies_products_delete(request, pk):
    referer = get_referer(request, 'cookies-products')
    product = get_object_or_404(Products, id=pk)
    try:
        product.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    except ProtectedError:
        messages.error(request, '해당 상품은 현재 판매중으로 삭제할 수 없습니다.')
        # 유저가 주문서 작성 도중에 삭제하는 경우 - 예외처리 필요
        # get()으로 인스턴스 조회한 다음 분기처리 필요(4번)

    return redirect(referer)


def cookies_times(request):
    times = Times.objects.all().order_by('name', 'start', 'end')
    context = {'times': times}

    return render(request, 'products/cookies_times.html', context)


def cookies_times_view(request, pk):
    time = get_object_or_404(Times, id=pk)
    context = {'time': time}

    return render(request, 'products/cookies_times_view.html', context)


def cookies_times_add(request):
    form = TimeAdd()

    if request.method == 'POST':
        form = TimeAdd(request.POST)
        if form.is_valid():
            instance = form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect('cookies_times_view', pk=instance.id)

    context = {'form': form}

    return render(request, 'products/cookies_times_add.html', context)


def cookies_times_edit(request, pk):
    time = get_object_or_404(Times, id=pk)
    form = TimeAdd(instance=time)

    if request.method == 'POST':
        form = TimeAdd(request.POST, instance=time)
        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect('cookies_times_view', pk=time.id)

    context = {'form': form, 'time': time}

    return render(request, 'products/cookies_times_add.html', context)


def cookies_times_delete(request, pk):
    time = get_object_or_404(Times, id=pk)
    try:
        time.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    except ProtectedError:
        messages.error(request, '해당 픽업시간은 현재 사용중으로 삭제할 수 없습니다.')

        # 유저가 주문서 작성 도중에 삭제하는 경우 - 삭제 못하게 막아둠

    return redirect('cookies_times')


def test(request):
    if request.method == 'POST':

        referer = get_referer(request, 'cookies')
        return redirect(referer)

    return render(request, 'products/test.html')

