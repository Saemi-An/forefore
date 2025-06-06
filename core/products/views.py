from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cookies, Products, Times, Sales
from .forms import ProductAdd, TimeAdd, CookieAdd
from .modules import get_cookie_sales, match_category_from_int_to_str, change_cookie_index


    # 판매중 --> 판매 종료
        # exclude(status=3) current = 0
        # Times selected = False
    # 판매 종료 --> 판매 시작
        # 조건1: Times selected 최소 1개
        # 조건2: 안전재고 = 현재 재고로 시작함 고지
        # 조건3: 판매중에는 픽업시간 변경 불가
def change_cookies_sale(request):
    print('여기 찍히긴 함?')
    status = get_object_or_404(Sales, id=1)
    print(f'변경 전 판매 상태: {"판매중" if status.on_sale else "판매 종료"}')
    filter = 'all'
    print(f'변경 전 판매 상태: {status.on_sale}')

    if status.on_sale:   # 판매중 --> 판매 종료
        Cookies.objects.exclude(status=3).update(current=0)
        Times.objects.filter(selected=True).update(selected=False)
    else:
        if not Times.objects.filter(selected=True):
            messages.error(request, '최소 1개의 픽업시간을 설정해 주세요.')
            return redirect('cookies', filter) 

    status.on_sale = not status.on_sale
    status.save()
    print(f'변경 후 판매 상태: {status.on_sale}')
    toast_msg = '시작' if status.on_sale else '종료'
    messages.success(request, f'구움과자 예약 판매가 {toast_msg} 되었습니다.')
        
    return redirect('cookies', filter)

def change_cookies_index(request, category, action, idx):
    filter = match_category_from_int_to_str(category)
    
    if action == 'up':
        target_idx = idx - 1
        if change_cookie_index(idx, target_idx):
            messages.success(request, '노출 순서가 변경 되었습니다.')
            return redirect('cookies', filter)
        else:
            messages.error(request, '더 이상 이동할 수 없습니다.')
            return redirect('cookies', filter)
    elif action == 'down':
        target_idx = idx + 1
        if change_cookie_index(idx, target_idx):
            messages.success(request, '노출 순서가 변경 되었습니다.')
            return redirect('cookies', filter)
        else:
            messages.error(request, '더 이상 이동할 수 없습니다.')
            return redirect('cookies', filter)

def cookies(request, category='all'):
    if category == 'financier':
        cookies = Cookies.objects.filter(product__category=0).order_by('index')
        filter = 0
    elif category == 'cakepiece':
        cookies = Cookies.objects.filter(product__category=1).order_by('index')
        filter = 1
    elif category == 'scone':
        cookies = Cookies.objects.filter(product__category=2).order_by('index')
        filter = 2
    elif category == 'todays-menu':
        cookies = Cookies.objects.filter(product__category=3).order_by('index')
        filter = 3
    else:
        cookies = Cookies.objects.all().order_by('index')
        filter = 100
        

    sales = get_cookie_sales()
    times = Times.objects.all().order_by('name', 'start', 'end')
    selected_times = Times.objects.filter(selected=True).order_by('name', 'start', 'end')
    form = CookieAdd()

    print(f'세일즈: {sales}')

    context = {
        'sales': sales,
        'cookies': cookies,
        'times': times,
        'selected_times': selected_times,
        'form': form,
        'filter': filter,
    }

    return render(request, 'products/cookies.html', context)

def cookies_view(request, pk):
    cookie = get_object_or_404(Cookies, id=pk)
    context = {'cookie': cookie}

    return render(request, 'products/cookies_view.html', context)

def cookies_add(request, pk=None):
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
                valid_form.status = 0
                valid_form.current = 0
            valid_form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect('cookies')
    
        # 테스트용 -- 추후 삭제 or 예외처리 필요
        else:
            print('cookies_add로 POST 요청 + 유효하지 않음 요청임')
            for k, v in form.errors.items():
                print(f'{k}: {v}')
            messages.error(request, '예외처리 필요 - POST 요청 실패')
            return redirect('cookies')

def cookies_pickups_add(request):
    if request.method == 'POST':
        val = request.POST['selected_times']
        if val:
            id_list = list(map(lambda str_id: int(str_id), request.POST['selected_times'].strip().split(' ')))   # ['1', '2', '5']
            Times.objects.filter(id__in=id_list).update(selected=True)   # 시그널 발생 안됨
        return redirect('cookies', 'all')

def cookies_delete(request, pk):
    cookie = get_object_or_404(Cookies, id=pk)
    cookie.delete()
    messages.success(request, '성공적으로 삭제 되었습니다.')
    return redirect('cookies')

def cookies_products(request):
    products = Products.objects.all().order_by('id')
    selected_category = None

    if request.method == 'POST':
        selected_category = request.POST['product_category']
        if selected_category:
            products = Products.objects.filter(category=int(selected_category)).order_by('id')

    context = {
        'products': products,
        'selected_category': selected_category,
    }

    return render(request, 'products/cookies_products.html', context)


def cookies_products_view(request, pk):
    product = get_object_or_404(Products, id=pk)
    context = {'product': product}

    return render(request, 'products/cookies_products_view.html', context)


def cookies_products_add(request):
    form = ProductAdd()

    if request.method == 'POST':
        form = ProductAdd(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect('cookies_products_view', pk=instance.id)
    context = {'form': form}

    return render(request, 'products/cookies_products_add.html', context)


def cookies_products_edit(request, pk):
    product = get_object_or_404(Products, id=pk)
    form = ProductAdd(instance=product)

    if request.method == 'POST':
        form = ProductAdd(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect('cookies_products_view', pk=product.id)

    context = {'form': form, 'product': product}

    return render(request, 'products/cookies_products_add.html', context)


def cookies_products_delete(request, pk):
    product = get_object_or_404(Products, id=pk)
    try:
        product.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    except ProtectedError:
        messages.error(request, '해당 상품은 현재 판매중으로 삭제할 수 없습니다.')
        # 유저가 주문서 작성 도중에 삭제하는 경우 - 예외처리 필요
        # get()으로 인스턴스 조회한 다음 분기처리 필요(4번)

    return redirect('cookies_products')


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
