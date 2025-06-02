from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.db.models.deletion import ProtectedError

from .models import Sale, Products, Cookies, Times, Pickups
from .forms import ProductAdd, TimeAdd

def cookies(request):
    sale = Sale.objects.get_or_create(id=1)   # 테스트 필요
    cookies = Cookies.objects.all().order_by('index')

    context = {
        'sale': sale,
        'cookies': cookies,
    }

    return render(request, 'products/cookies.html', context)


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
            messages.success(request, "성공적으로 저장 되었습니다.")
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
            messages.success(request, "성공적으로 저장 되었습니다.")
            return redirect('cookies_products_view', pk=product.id)

    context = {'form': form, 'product': product}

    return render(request, 'products/cookies_products_add.html', context)

def cookies_products_delete(request, pk):
    product = get_object_or_404(Products, id=pk)
    try:
        product.delete()
        messages.success(request, "성공적으로 삭제 되었습니다.")
    except ProtectedError:
        messages.error(request, "해당 상품은 현재 판매중으로 삭제할 수 없습니다.")
        # 유저가 주문서 작성 도중에 삭제하는 경우 - 예외처리 필요
        # get()으로 인스턴스 조회한 다음 분기처리 필요(4번)

    return redirect('cookies_products')


def cookies_times(request):
    times = Times.objects.all().order_by('pk')
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
            messages.success(request, "성공적으로 저장 되었습니다.")
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
            messages.success(request, "성공적으로 저장 되었습니다.")
            return redirect('cookies_times_view', pk=time.id)
        
    context = {'form': form, 'time': time}

    return render(request, 'products/cookies_times_add.html', context)

def cookies_times_delete(request, pk):
    time = get_object_or_404(Times, id=pk)
    try:
        time.delete()
        messages.success(request, "성공적으로 삭제 되었습니다.")
    except ProtectedError:
        messages.error(request, "해당 픽업시간은 현재 사용중으로 삭제할 수 없습니다.")

        # 유저가 주문서 작성 도중에 삭제하는 경우 - 삭제 못하게 막아둠

    return redirect('cookies_times')