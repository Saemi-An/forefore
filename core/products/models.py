from django.db import models


# =================================== 공통 ===================================
class Sales(models.Model):

    class Meta:
        verbose_name_plural = '판매 상태'
        db_table = 'Sales'

    on_sale = models.BooleanField(default=False)

    # def __str__(self):
    #     return '판매중' if self.on_sale else '판매 종료'


# =================================== 구움과자 ===================================
class Products(models.Model):

    class Meta:
        verbose_name_plural = '구움과자 상품'
        db_table = 'Products'

    class Cookie_Categories(models.IntegerChoices):
        financier = 1, '휘낭시에'
        cakepiece = 2, '조각케이크'
        scone = 3, '스콘'
        todaysmenu = 4, '오늘의 메뉴'

    category = models.PositiveIntegerField(choices=Cookie_Categories.choices)
    name = models.CharField(max_length=100)  # 30
    price = models.PositiveIntegerField()
    cmt = models.CharField(max_length=1000, blank=True)  # 100
    img = models.ImageField(upload_to='cookies')

    def __str__(self):
        return self.name


class Cookies(models.Model):

    class Meta:
        verbose_name_plural = '구움과자 판매'
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
            category_num = self.product.category
            total = Cookies.objects.filter(product__category=category_num).count()
            self.index = (100 * category_num) + 1 + total

            # if self.product.category == 1:
            #     total = Cookies.objects.filter(product__category=1).count()
            #     self.index = 101 + total

            # elif self.product.category == 2:
            #     total = Cookies.objects.filter(product__category=2).count()
            #     self.index = 201 + total

            # elif self.product.category == 3:
            #     total = Cookies.objects.filter(product__category=3).count()
            #     self.index = 301 + total

            # else:
            #     total = Cookies.objects.filter(product__category=4).count()
            #     self.index = 401 + total
            

        # [시즌 종료] 상태라면, current_stock은 null ------------------------------------------------
        if self.status == 3:
            self.total = 0
            self.safe = 0
            self.current = 0

        # 판매중(status=1)에 현재재고가 0이 되면, 예약 마감(status=2)로 변경 ------------------------------------------------
        if self.status == 1 and self.current == 0:
            self.status = 2

        super().save(*args, **kwargs)  # 상태 변경 후 다시 저장

    def __str__(self):
        return f'{self.pk} | {self.product.name} | 인덱스: {self.index}'


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
        return f'{self.id} | {self.name[:7]} | {self.selected}'


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
class Options(models.Model):

    class Meta:
        verbose_name_plural = '홀케이크 옵션'
        db_table = 'Options'

    class OptionTypes(models.IntegerChoices):
        size = 1, '호수'
        add_fruite = 2, '과일 추가'
        mix_fruite = 3, '과일 믹스'
        change_cream = 4, '생크림 변경'
        change_sheet = 5, '시트 변경'
        choco_glassage = 6, '초코 글라사쥬'

    type = models.PositiveIntegerField(choices=OptionTypes.choices)
    name = models.CharField(max_length=100)  # 10(폼 유효성 검사시 프론트 너비 참고해서 재지정 필요)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.name}, {self.price}원'


class Schedules(models.Model):

    class Meta:
        verbose_name_plural = '홀케이크 스케줄'
        db_table = 'Schedules'

    class SchedulesDays(models.IntegerChoices):
        # name = value, 'label'
        mon = 0, '월요일'
        tue = 1, '화요일'
        wed = 2, '수요일'
        thu = 3, '목요일'
        fri = 4, '금요일'
        sat = 5, '토요일'
        sun = 6, '일요일'
        
        @classmethod
        def to_bit(cls, day):
            return 1 << day

    class SchedulesInterval(models.IntegerChoices):
        twenty = 20, '20분'
        thirty = 30, '30분'

    name = models.CharField(max_length=100)  # 10(폼 유효성 검사시 프론트 너비 참고해서 재지정 필요)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.PositiveIntegerField()
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()
    interval = models.IntegerField(choices=SchedulesInterval.choices)

    def get_days_display(self):
        return [
            label for day, label in self.SchedulesDays.choices
            if (self.days & self.SchedulesDays.to_bit(day)) != 0
        ]
    
    def __str__(self):
        return self.name

class Cakes(models.Model):

    class Meta:
        verbose_name_plural = '홀케이크 판매'
        db_table = 'Cakes'

    class CakesDisplay(models.IntegerChoices):
        hidden = 0, '상품 숨김'
        exposed = 1, '상품 노출'
        closed = 2, '상품 노출 [예약 마감]'
        season_out = 3, '상품 노출 [시즌 종료]'

    index = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)  # 30
    cmt = models.CharField(max_length=1000, blank=True)  # 100
    img = models.ImageField(upload_to='cakes')
    display = models.PositiveIntegerField(choices=CakesDisplay.choices)
    options = models.ManyToManyField(Options, through='CakeOptions')
    schedules = models.ManyToManyField(Schedules, through='CakeSchedules')

    def save(self, *args, **kwargs):
        self.clean()
        
        # 새상품 등록시에만 index 자동 부여 ------------------------------------------------
        if self._state.adding:
            total = Cakes.objects.all().count()
            self.index = total + 1
        
        super().save(*args, **kwargs)  # 상태 변경 후 다시 저장

    def __str__(self):
        return self.name


class CakeOptions(models.Model):

    class Meta:
        db_table = 'CakeOptions'
    
    cake = models.ForeignKey(Cakes, on_delete=models.CASCADE)
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'케이크: {self.cake.name}, {self.cake.pk} / 옵션들: {self.option.name}'   # 이거 출력 어떻게됨?

class CakeSchedules(models.Model):

    class Meta:
        db_table = 'CakeSchedules'
    
    cake = models.ForeignKey(Cakes, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedules, on_delete=models.CASCADE)
    

# 장고 어드민 테스트용
class BitDays(models.Model):

    class Meta:
        verbose_name_plural = '테스트용 스케줄'
        db_table = 'BitDays'

    class BitDaysEnum(models.IntegerChoices):
        # name = value, 'label'
        mon = 0, '월요일'
        tue = 1, '화요일'
        wed = 2, '수요일'
        thu = 3, '목요일'
        fri = 4, '금요일'
        sat = 5, '토요일'
        sun = 6, '일요일'

        @classmethod
        def to_bit(cls, day):
            return 1 << day
        
        @classmethod
        def from_label(cls, label):
            for member in cls:
                if member.label == label:
                    return member
            raise ValueError(f'{label}: 요일이 정확하지 않습니다.')

        @classmethod
        def resolve(cls, item):
            if isinstance(item, cls):   # mon --> enum 키 반환
                return item
            if isinstance(item, str):   # '월요일' --> enum 키 반환
                try:
                    return cls[item]
                except KeyError:
                    return cls.from_label(item)
            if isinstance(item, int):   # 0 --> enum 키 반환
                return cls(item)
            raise ValueError(f'{item}: 요일이 정확하지 않습니다.')

    name = models.CharField(max_length=100)
    days = models.PositiveIntegerField()

    def add_days(self, lst_days):
        for elem in lst_days:
            enum_day = self.BitDaysEnum.resolve(elem)
            self.days |= self.BitDaysEnum.to_bit(enum_day)
    
    def remove_days(self, lst_days):
        for elem in lst_days:
            enum_day = self.BitDaysEnum.resolve(elem)
            self.days &= ~self.BitDaysEnum.to_bit(enum_day)
    
    def has_days(self, lst_days):
        return all(
            (self.days & self.BitDaysEnum.to_bit(self.BitDaysEnum.resolve(elem))) != 0
            for elem in lst_days
        )

    def set_days(self, lst_days):
        self.days = 0
        self.add_days(lst_days)

    def get_days_display(self):
        return [
            label for day, label in self.BitDaysEnum.choices
            if (self.days & self.BitDaysEnum.to_bit(day)) != 0
        ]
    
    def __str__(self):
        return f'{self.name}, {self.days}'