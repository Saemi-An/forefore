from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .models import Sales, Products, Times, Cookies, Options, Schedules, Cakes, CakeOptions, CakeSchedules
from .forms import ProductAdd, TimeAdd, CookieAdd, OptionAdd, ScheduleAdd, TestForm
from .modules import change_cookie_index, get_cookie_sales, match_category_from_str_to_int, get_referer, get_paginated_objects, match_type_from_str_to_int

# 추후 삭제
from .models import BitDays
from .forms import BitDaysForm


def cookies(request, category='all'):
    int_category = match_category_from_str_to_int(category)
    if int_category:
        cookies = Cookies.objects.filter(product__category=int_category).order_by('index')
    else:
        cookies = Cookies.objects.all().order_by('index')

    page_obj = get_paginated_objects(request, cookies)
    sales = get_cookie_sales()
    times = Times.objects.all().order_by('name', 'start', 'end')
    selected_times = Times.objects.filter(selected=True).order_by('name', 'start', 'end')
    form = CookieAdd()

    context = {
        'filter': category,
        'cookies': page_obj,
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
    referer = get_referer(request, 'cookies')   # 뷰페이지에서 수정할 경우 
    sales = get_cookie_sales()
    form = CookieAdd()
    context = {
        'cookie': cookie,
        'referer': referer,
        'sales': sales,
        'form': form
    }

    return render(request, 'products/cookies_view.html', context)


def cookies_add_and_edit(request, pk=None):
    cookie = get_object_or_404(Cookies, id=pk) if pk else None
    if request.method == 'POST':
        view_referer = request.POST.get('redirect_url', None)   # 뷰페이지에서 수정시 전전페이지 url
        referer = view_referer if view_referer else get_referer(request, 'cookies')   # view referer 없으면 cookies 페이지 refer 사용
        form = CookieAdd(request.POST, instance=cookie)

        if form.is_valid():
            valid_form = form.save(commit=False)
            if get_cookie_sales():
                valid_form.current = valid_form.safe
            else:
                valid_form.current = 0
            valid_form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(referer)


def cookies_delete(request, pk):
    if request.method == 'POST':
        referer = request.POST.get('redirect_url', '/manager/cookies/')
    else:
        referer = get_referer(request, 'cookies')
    
    cookie = get_object_or_404(Cookies, id=pk)
    cookie.delete()
    messages.success(request, '성공적으로 삭제 되었습니다.')
    return redirect(referer)


def cookies_products(request, str_category='all'):
    int_category = match_category_from_str_to_int(str_category)
    if int_category:
        products = Products.objects.filter(category=int_category).order_by('id')
    else:
        products = Products.objects.all().order_by('id')
            
    page_obj = get_paginated_objects(request, products)

    context = {
        'products': page_obj,
        'selected_category': str_category,
    }

    return render(request, 'products/cookies_products.html', context)


def cookies_products_view(request, pk):
    product = get_object_or_404(Products, id=pk)
    referer = get_referer(request, 'cookies-products')
    context = {'product': product, 'referer': referer}

    return render(request, 'products/cookies_products_view.html', context)


def cookies_products_add_and_edit(request, pk=None):
    product = get_object_or_404(Products, id=pk) if pk else None
    if request.method == 'POST':
        form = ProductAdd(request.POST, request.FILES, instance=product)
        redirect_url = request.POST.get('redirect_url', '/manager/cookies-products/all/')

        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)
    else:
        form = ProductAdd(instance=product)
        referer = get_referer(request, 'cookies-products')
    
    context = {
        'form': form,
        'product': product,
        'referer': referer if request.method == 'GET' else None
    }
    return render(request, 'products/cookies_products_add.html', context)


def cookies_products_delete(request, pk):
    if request.method == 'POST':
        referer = request.POST.get('redirect_url', '/manager/cookies-products/')
    else:
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
    page_obj = get_paginated_objects(request, times)
    
    context = {'times': page_obj}

    return render(request, 'products/cookies_times.html', context)


def cookies_times_view(request, pk):
    time = get_object_or_404(Times, id=pk)
    context = {'time': time}

    return render(request, 'products/cookies_times_view.html', context)


def cookies_times_add_and_edit(request, pk=None):
    time = get_object_or_404(Times, id=pk) if pk else None
    if request.method == 'POST':
        form = TimeAdd(request.POST, instance=time)
        redirect_url = request.POST.get('redirect_url', '/manager/cookies-times/')

        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)
    else:
        form = TimeAdd(instance=time)
        referer = get_referer(request, 'cookies-times')
    
    context = {
        'form': form,
        'time': time,
        'referer': referer if request.method == 'GET' else None
    }

    return render(request, 'products/cookies_times_add.html', context)


def cookies_times_delete(request, pk):
    referer = get_referer(request, 'cookies-products')
    time = get_object_or_404(Times, id=pk)

    try:
        time.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    # 유저가 주문서 작성 도중에 삭제하는 경우 - 삭제 못하게 막아둠
    except ProtectedError:
        messages.error(request, '해당 픽업시간은 현재 사용중으로 삭제할 수 없습니다.')

    return redirect(referer)

# ==============================================================
# *************************** 홀케이크 ***************************
# ==============================================================

def cakes(reqeust):
    return

def cakes_options(request, str_type='all'):
    int_type = match_type_from_str_to_int(str_type)
    if int_type:
        options = Options.objects.filter(type=int_type).order_by('type', 'name', 'price')
    else:
        options = Options.objects.all().order_by('type', 'name', 'price')
    page_obj = get_paginated_objects(request, options)
    
    context = {'options': page_obj, 'selected_type': str_type}

    return render(request, 'products/cakes_options.html', context)


def cakes_options_view(request, pk):
    option = get_object_or_404(Options, id=pk)
    is_being_used = CakeOptions.objects.filter(option=option).exists()
    referer = get_referer(request, 'cakes-options')

    context = {'option': option, 'referer': referer, 'is_being_used': is_being_used}

    return render(request, 'products/cakes_options_view.html', context)


def cakes_options_add_and_edit(request, pk=None):
    option = get_object_or_404(Options, id=pk) if pk else None
    if request.method == 'POST':
        form = OptionAdd(request.POST, instance=option)
        redirect_url = request.POST.get('redirect_url', '/manager/cakes-options/all/')

        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)
    else:
        form = OptionAdd(instance=option)
        referer = get_referer(request, 'cookies-times')
    
    context = {
        'form': form,
        'option': option,
        'referer': referer if request.method == 'GET' else None
    }

    return render(request, 'products/cakes_options_add.html', context)


def cakes_options_delete(request, pk):
    if request.method == 'POST':
        referer = request.POST.get('redirect_url', '/manager/cakes-options/all/')
    else:
        referer = get_referer(request, 'cookies-products')

    option = get_object_or_404(Options, id=pk)
    try:
        option.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    except ProtectedError:
        # 홀케이크 등록 뷰 완성하고 테스트 필요
        messages.error(request, '해당 옵션은 현재 사용중으로 삭제할 수 없습니다.')

    return redirect(referer)


def cakes_schedules(request):
    schedules = Schedules.objects.all().order_by('name', 'start_date', 'start_time')
    page_obj = get_paginated_objects(request, schedules)
    
    context = {'schedules': page_obj}

    return render(request, 'products/cakes_schedules.html', context)


def cakes_schedules_view(request, pk):
    schedule = get_object_or_404(Schedules, id=pk)
    is_being_used = CakeSchedules.objects.filter(schedule=schedule).exists()
    referer = get_referer(request, 'cookies-products')
    context = {'schedule': schedule, 'referer': referer, 'is_being_used': is_being_used}

    return render(request, 'products/cakes_schedules_view.html', context)


def cakes_schedules_add_and_edit(request, pk=None):
    schedule = get_object_or_404(Schedules, id=pk) if pk else None
    selected_days = schedule.days if pk else None   # 수정 페이지에서 미리 선택된 요일 비트마스킹값 넘겨주기 (JS 처리용)

    if request.method == 'POST':
        form = ScheduleAdd(request.POST, instance=schedule)
        redirect_url = request.POST.get('redirect_url', '/manager/cakes-schedules/')


        if form.is_valid():
            form.save()
            messages.success(request, '성공적으로 저장 되었습니다.')
            return redirect(redirect_url)
        
    else:
        form = ScheduleAdd(instance=schedule)
        referer = get_referer(request, 'cookies-times')
    
    context = {
        'form': form,
        'schedule': schedule,
        'selected_days': selected_days,
        'referer': referer if request.method == 'GET' else None
    }

    return render(request, 'products/cakes_schedules_add.html', context)


def cakes_schedules_delete(request, pk):
    # 뷰 페이지에서 삭제용 redirect url
    if request.method == 'POST':
        referer = request.POST.get('redirect_url', '/manager/cakes-schedules/')
    # 목록 페이지에서 삭제용 redirect url
    else:
        referer = get_referer(request, 'cakes-schedules')

    schedule = get_object_or_404(Schedules, id=pk)
    try:
        schedule.delete()
        messages.success(request, '성공적으로 삭제 되었습니다.')
    except ProtectedError:
        messages.error(request, '해당 픽업시간은 현재 사용중으로 삭제할 수 없습니다.')

    return redirect(referer)


# 테스트용: 추후 삭제 필요
def test(request):
    # request.POST.getlist('days')
    if request.method == 'POST':
        form = BitDaysForm(request.POST)
        if form.is_valid():
            schedule_obj = form.save(commit=False)

            str_days = request.POST.get('selected_days').strip()
            lst_days = list(map(int, str_days.split())) # ['1', '2', '10'] --> [1, 2, 10]
            bitmask = 0
            for elem in lst_days:
                bitmask |= 1 << elem
            
            schedule_obj.days = bitmask
            form.save()
            return redirect('test')
    else:
        form = BitDaysForm()
        test_form = TestForm()
        objs = BitDays.objects.all().order_by('pk')

    context = {
        'objs': objs,
        'form': form,
        'test_form': test_form,
    }

    return render(request, 'products/test.html', context)

def test2(request):
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            print('폼이 벨리드함')
            print(test_form.data)

            days = test_form.cleaned_data['days']
            print(days)


        else:
            print('폼이 벨리드 하지 못함')
            print(test_form.errors)
            print(test_form.data)
    else:
        test_form = TestForm()
    
    form = BitDaysForm()
    objs = BitDays.objects.all().order_by('pk')

    context = {
        'objs': objs,
        'form': form,
        'test_form': test_form,
    }

    return render(request, 'products/test.html', context)
    