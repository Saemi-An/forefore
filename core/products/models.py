from django.db import models

# =================================== 공통 ===================================
class Sale(models.Model):

    class Meta:
        verbose_name_plural = '판매 상태'
        db_table = 'Sale'

    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return '판매중' if self.on_sale else '판매 종료'


# =================================== 구움과자 ===================================
class Products(models.Model):
    class Meta:
        verbose_name_plural = '구움과자 상품'
        db_table = 'Products'

    class Cookie_Categories(models.IntegerChoices):
        financier = 0, '휘낭시에'
        cakepiece = 1, '조각케이크'
        scone = 2, '스콘'
        todaysmenu = 3, '오늘의 메뉴'

    category = models.PositiveIntegerField(choices=Cookie_Categories.choices)
    name = models.CharField(max_length=100)   # 30
    price = models.PositiveIntegerField()
    cmt = models.CharField(max_length=1000, blank=True)   # 100
    img = models.ImageField(upload_to='cookies')

    def __str__(self):
        return self.name


class Cookies(models.Model):

    class Meta:
        verbose_name_plural = '구움과자'
        db_table = 'Cookies'

    class Cookie_Status(models.IntegerChoices):
        waiting = 0, '판매 대기중'
        on_sale = 1, '판매중'
        sold_out = 2, '재고 소진'
        out = 3, '시즌 종료'

    status = models.PositiveIntegerField(choices=Cookie_Status.choices)
    total = models.PositiveIntegerField()
    safe = models.PositiveIntegerField()
    current = models.PositiveIntegerField()
    index = models.PositiveIntegerField(unique=True)
    product = models.OneToOneField(Products, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        self.clean()

        # 새상품 등록시에만 index 자동 부여 ------------------------------------------------
        if self._state.adding:
            self.index = Cookies.objects.exclude(status=3).count() + 1

            # if self.product.category == Products.Cookie_Categories.financier:
            #     total = Cookies.objects.filter(product__category=Products.Cookie_Categories.financier).count()
            #     if total == 0:
            #         self.index = 101
            #     else:
            #         self.index = 101 + total

            # elif self.product.category == Products.Cookie_Categories.cakepiece:
            #     total = Cookies.objects.filter(product__category=Products.Cookie_Categories.cakepiece).count()
            #     if total == 0:
            #         self.index = 201
            #     else:
            #         self.index = 201 + total

            # elif self.product.category == Products.Cookie_Categories.scone:
            #     total = Cookies.objects.filter(product__category=Products.Cookie_Categories.scone).count()
            #     if total == 0:
            #         self.index = 301
            #     else:
            #         self.index = 301 + total

            # else:
            #     total = Cookies.objects.filter(product__category=Products.Cookie_Categories.todaysmenu).count()
            #     if total == 0:
            #         self.index = 401
            #     else:
            #         self.index = 401 + total

        # [시즌 종료] 상태라면, current_stock은 null ------------------------------------------------
        # if self.status == 3:
        #     self.total = None
        #     self.safe = None
        #     self.current = None

        # 판매중(status=1)에 현재재고가 0이 되면, 예약 마감(status=2)로 변경 ------------------------------------------------
        # if self.status == 1 and self.current == 0:
        #     self.status = 2

        super().save(*args, **kwargs)  # 상태 변경 후 다시 저장

    def __str__(self):
        return f'{self.index} | {self.product.name}'


class Times(models.Model):
    class Meta:
        verbose_name_plural = '구움과자 픽업시간'
        db_table = 'Times'

    class Cookie_Interval(models.IntegerChoices):
        twenty = 20, '20분'
        thirty = 30, '30분'

    name = models.CharField(max_length=50)
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    interval = models.IntegerField(choices=Cookie_Interval.choices)
    selected = models.BooleanField(default=False)

    # 픽업시간 10 ~ 19시
    # end는 start보다 작을 수 없음
    # 픽업시간 템플릿이 <구움과자 판매> 페이지에서 픽업시간으로 사용중인 경우, 삭제 불가
    def __str__(self):
        return f'{self.name}'


class Pickups(models.Model):

    class Meta:
        verbose_name_plural = '구움과자 픽업 테이블'
        db_table = 'Pickups'

    str_time = models.CharField(max_length=5)  # 12:00 형식의 str(5자) 제한
    reserved = models.BooleanField(default=False)
    time = models.ForeignKey(Times, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.str_time} / {self.reserved} / 참조: {self.time}'


# =================================== 홀케이크 ===================================
