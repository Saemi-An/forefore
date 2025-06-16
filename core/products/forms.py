from datetime import date

from django import forms

from .models import Sales
from .models import Products, Times, Cookies
from .models import Options, Schedules, Cakes
from .models import BitDays

class ProductAdd(forms.ModelForm):

    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'md-reg add_md-reg_class_to_options'}),
            'name': forms.TextInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'cmt': forms.Textarea(attrs={
                'rows': 3,
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'img': forms.ClearableFileInput(attrs={
                'id': 'fileUpload',
                'class': 'display-none'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # category 드롭다운 기본값 커스텀
        choices = self.fields['category'].choices
        if choices and choices[0][0] == '':
            self.fields['category'].choices = [('', '선택해 주세요.')] + list(choices[1:])

        # html 속성 커스텀
        self.fields['category'].required = False
        self.fields['name'].required = False
        self.fields['price'].required = False
        # self.fields['price'].widget.attrs.pop('min', None)   # 이거 왜 뺐었지?
        self.fields['img'].required = False

    # 유효성 검사
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category == '':
            raise forms.ValidationError('필수 입력값 입니다.')
        return category

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name is None or name == '':
            raise forms.ValidationError('필수 입력값 입니다.')
        elif len(name) > 30:
            raise forms.ValidationError('공백포함 최대 30자까지 입력이 가능합니다.')
        return name

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price != 0 and not price:
            raise forms.ValidationError('필수 입력값 입니다.')
        return price

    def clean_cmt(self):
        cmt = self.cleaned_data.get('cmt')
        if len(cmt) > 100:
            raise forms.ValidationError('공백포함 최대 100자까지 입력이 가능합니다.')
        return cmt

    def clean_img(self):
        img = self.cleaned_data.get('img')
        if img is None or (isinstance(img, str) and img == ''):
            # None 이거나(or)
            # img 필드가 공백 문자열일 경우 required 에러메세지
            raise forms.ValidationError('필수 입력값 입니다.')
        return img


class TimeAdd(forms.ModelForm):

    class Meta:
        model = Times
        exclude = ('selected',)
        widgets = {
            'name':
                forms.TextInput(attrs={
                    'class': 'md-reg',
                    'placeholder': '입력해 주세요.'
                }),
            'start':
                forms.Select(
                    choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                    attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'end':
                forms.Select(
                    choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                    attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'interval':
                forms.Select(attrs={'class': 'md-reg add_md-reg_class_to_options'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # interval 드롭다운 기본값 커스텀
        choices = self.fields['interval'].choices
        if choices and choices[0][0] == '':
            self.fields['interval'].choices = [('', '선택해 주세요.')] + list(choices[1:])

        # html 속성 커스텀
        self.fields['name'].required = False
        self.fields['start'].required = False
        self.fields['end'].required = False
        self.fields['interval'].required = False

    # 유효성 검사
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name is None or name == '':
            raise forms.ValidationError('필수 입력값 입니다.')
        elif len(name) > 30:
            raise forms.ValidationError('공백포함 최대 30자까지 입력이 가능합니다.')
        return name

    def clean_interval(self):
        interval = self.cleaned_data.get('interval')
        if interval == '':
            raise forms.ValidationError('필수 입력값 입니다.')
        return interval

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end:
            if start >= end:
                self.add_error('start', '시작 시간과 마감 시간을 확인해 주세요.')
        else:
            self.add_error('start', '필수 입력값 입니다.')


class CookieAdd(forms.ModelForm):

    class Meta:
        model = Cookies
        exclude = (
            'current',
            'index',
        )
        widgets = {
            'product': forms.Select(attrs={
                'class': 'md-reg add_md-reg_class_to_options',
                'id': 'selectProduct'
            }),
            'status': forms.Select(attrs={
                'class': 'md-reg add_md-reg_class_to_options',
                'id': 'selectStatus'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.',
                'id': 'inputTotal'
            }),
            'safe': forms.NumberInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.',
                'id': 'inputSafe'
            })
        }

    # 모달이라 유효성 검사는 JS로

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # product 드롭다운 기본값 커스텀
            # form에 registered 값 함께 넘김 --> html에서 option 값만 수동 렌더링
        self.fields['product'].empty_label = '선택해 주세요.'
        used_ids = set(Cookies.objects.values_list('product_id', flat=True))
        self.registered = used_ids

        # status 드롭다운 기본값 커스텀
        status_choices = self.fields['status'].choices
        # self.fields['status'].empty_label = '선택해 주세요.'
        if status_choices and status_choices[0][0] == '':
            self.fields['status'].choices = [('', '선택해 주세요.')] + list(status_choices[1:])

        # html 속성 커스텀
        self.fields['product'].required = False
        self.fields['status'].required = False
        self.fields['total'].required = False
        self.fields['safe'].required = False

        # 구움과자 판매상태
        sales = Sales.objects.get(id=1).on_sale

        if sales:
            self.fields['status'].choices = [('', '선택해 주세요.'), (Cookies.Cookie_Status.on_sale, '판매중'), (Cookies.Cookie_Status.sold_out, '재고 소진')]

            # existing_classes_from_total = self.fields['total'].widget.attrs.get('class', '')
            # self.fields['total'].widget.attrs['class'] = f'{existing_classes_from_total} no-input'
            
            # existing_classes_from_safe = self.fields['safe'].widget.attrs.get('class', '')
            # self.fields['safe'].widget.attrs['class'] = f'{existing_classes_from_safe} no-input'

        else:
            self.fields['status'].choices = [('', '선택해 주세요.'), (Cookies.Cookie_Status.waiting, '판매 대기중'), (Cookies.Cookie_Status.out, '시즌 종료')]


# ==============================================================
# *************************** 홀케이크 ***************************
# ==============================================================

class CakeAdd(forms.ModelForm):
    class Meta:
        model = Cakes
        exclude = ('index', )
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'cmt': forms.Textarea(attrs={
                'rows': 3,
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'img': forms.ClearableFileInput(attrs={
                'id': 'fileUpload',
                'class': 'display-none'
            }),
            'display': forms.Select(attrs={
                'class': 'md-reg add_md-reg_class_to_options'
            }),
            # 'options': forms.CheckboxSelectMultiple(
            #     attrs={'class': 'visually-hidden'},
            #     choices=Options.objects.all().order_by('type', 'price', 'name')
            # ),
            'schedules': forms.CheckboxSelectMultiple(
                attrs={'class': 'visually-hidden'},
                choices=Schedules.objects.all().order_by('name', 'start_date', 'start_time')
            )
        }       

    # 커스텀
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['cmt'].required = False
        self.fields['img'].required = False        
        self.fields['display'].required = False
        self.fields['options'].required = False
        self.fields['schedules'].required = False

        # display 드롭다운 기본값 커스텀
        display_choices = self.fields['display'].choices
        if display_choices and display_choices[0][0] == '':
            self.fields['display'].choices = [('', '선택해 주세요.')] + list(display_choices[1:])

    # 유효성 검사
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        cmt = cleaned_data.get('cmt')
        img = cleaned_data.get('img')
        display = cleaned_data.get('display')
        options = cleaned_data.get('options')
        schedules = cleaned_data.get('schedules')

        if not name:
            self.add_error('name', '필수 입력값 입니다.')

        if len(cmt) > 30:
            self.add_error('cmt', '공백포함 최대 30자까지 입력이 가능합니다.')

        if img is None or (isinstance(img, str) and img == ''):
            self.add_error('img', '필수 입력값 입니다.')

        if display == "":
            self.add_error('display', '필수 입력값 입니다.')

        if not options:
            self.add_error('options', '필수 입력값 입니다.')

        if not schedules:
            self.add_error('schedules', '필수 입력값 입니다.')

class OptionAdd(forms.ModelForm):

    class Meta:
        model = Options
        fields = '__all__'
        widgets = {
            'type': forms.Select(attrs={
                'class': 'md-reg add_md-reg_class_to_options'
            }),
            'name': forms.TextInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'md-reg',
                'placeholder': '입력해 주세요.'
            })
        }

    # 커스텀
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['type'].required = False
        self.fields['name'].required = False
        self.fields['price'].required = False

        # type 드롭다운 기본값 커스텀
        choices = self.fields['type'].choices
        if choices and choices[0][0] == '':
            self.fields['type'].choices = [('', '선택해 주세요.')] + list(choices[1:])

    # 유효성 검사
    def clean(self):
        cleaned_data = super().clean()
        type = cleaned_data.get('type') 
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')

        if not type:
            self.add_error('type', '필수 입력값 입니다.')
        if not name:
            self.add_error('name', '필수 입력값 입니다.')
        if not price:
            self.add_error('price', '필수 입력값 입니다.')


class ScheduleAdd(forms.ModelForm):
    class Meta:
        model = Schedules
        fields = '__all__'
        widgets = {
            'name':
                forms.TextInput(attrs={
                    'class': 'md-reg',
                    'placeholder': '입력해 주세요.'
                }),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'md-reg'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'md-reg'}),
            'days': forms.HiddenInput(attrs={'id': 'hiddenDaysInput'}),
            'start_time':
                forms.Select(
                    choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                    attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'end_time':
                forms.Select(
                    choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                    attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'interval': forms.Select(attrs={'class': 'md-reg add_md-reg_class_to_options'})
            }
    
    # 커스텀
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['start_date'].required = False
        self.fields['end_date'].required = False        
        self.fields['days'].required = False
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False    
        self.fields['interval'].required = False    
        
        # interval 드롭다운 기본값 커스텀
        choices = self.fields['interval'].choices
        if choices and choices[0][0] == '':
            self.fields['interval'].choices = [('', '선택해 주세요.')] + list(choices[1:])

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        days = cleaned_data.get('days')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        interval = cleaned_data.get('interval')

        # name 필드
        if not name:
            self.add_error('name', '필수 입력값 입니다.')
        elif len(name) >= 30:
            self.add_error('name', '공백 포함 최대 30자 까지 입력 가능합니다.')
        
        # start_date, end_date 필드
        if not start_date:
            self.add_error('start_date', '필수 입력값 입니다.')
        elif not end_date:
            self.add_error('end_date', '필수 입력값 입니다.')
        elif end_date < date.today():
            self.add_error('end_date', '마지막 날짜가 예약이 불가능한 과거 입니다.')
        elif start_date > end_date:
            self.add_error('start_date', '시작 날짜와 마지막 날짜를 확인해 주세요.')

        # days 필드
        if not days:
            self.add_error('days', '필수 입력값 입니다.')
            
        # start_time, end_time 필드
        if not start_time:
            self.add_error('start_time', '필수 입력값 입니다.')
        elif not end_time:
            self.add_error('end_time', '필수 입력값 입니다.')
        elif start_time > end_time:
            self.add_error('start_time', '시작 시간과 마감 시간을 확인해 주세요.')
            
        # interval 필드
        if not interval:
            self.add_error('interval', '필수 입력값 입니다.')
        



# 장고 어드민용
class SchedulesForm(forms.ModelForm):
    
    days = forms.MultipleChoiceField(
        choices = Schedules.SchedulesDays.choices,
        widget = forms.CheckboxSelectMultiple,
        required = False,
    )

    class Meta:
        model = Schedules
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 기존 인스턴스의 비트마스크 값을 읽어 체크박스 초기값 설정
        # 현재 인스턴스의 비트마스크에 포함된 요일들의 value list를 만들어 days 필드의 초기값으로 넣음
        if self.instance and self.instance.pk:
            self.initial['days'] = [
                day.value for day in Schedules.SchedulesDays
                if self.instance.days & (1 << day.value)   # 해당 요일이 비트마스크에 포함되어 있는가
            ]
    
    def clean(self):
        cleaned_data = super().clean()
        selected_days = cleaned_data.get('days', [])
        # 선택된 요일을 비트마스크로 변환하여 저장
        bitmask = 0
        for day in selected_days:
            bitmask |= (1 << int(day))
        cleaned_data['days'] = bitmask   # 비트마스크 값으로 변환된 정수(bitmask)를 모델의 'days' 필드에 저장
        return cleaned_data

# ------------------------------- 테스트용, 추후 삭제 필요

# 장고 어드민 테스트용
class BitDaysForm(forms.ModelForm):
    
    days = forms.MultipleChoiceField(
        choices = BitDays.BitDaysEnum.choices,
        widget = forms.CheckboxSelectMultiple,
        required = False,
        label = '요일 선택'
    )

    class Meta:
        model = BitDays
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 기존 인스턴스의 비트마스크 값을 읽어 체크박스 초기값 설정
        # 현재 인스턴스의 비트마스크에 포함된 요일들의 value list를 만들어 days 필드의 초기값으로 넣음
        if self.instance and self.instance.pk:
            self.initial['days'] = [
                day.value for day in BitDays.BitDaysEnum
                if self.instance.days & (1 << day.value)   # 해당 요일이 비트마스크에 포함되어 있는가
            ]
    
    def clean(self):
        cleaned_data = super().clean()
        selected_days = cleaned_data.get('days', [])
        # 선택된 요일을 비트마스크로 변환하여 저장
        bitmask = 0
        for day in selected_days:
            bitmask |= (1 << int(day))
        cleaned_data['days'] = bitmask   # 비트마스크 값으로 변환된 정수(bitmask)를 모델의 'days' 필드에 저장
        return cleaned_data

# 테스트용. 추후 삭제 필요
class TestForm(forms.ModelForm):
    class Meta:
        model = BitDays
        fields = '__all__'
        widgets = {
            'days': forms.HiddenInput()
        }
    
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '')
        selected_days = cleaned_data.get('days', [])
        print(selected_days)
        print(type(selected_days))

        if not name:
            self.add_error('name', '필수 입력값 입니다.')

        # if selected_days:
        #     # 선택된 요일을 비트마스크로 변환하여 저장
        #     bitmask = 0
        #     for day in selected_days:
        #         bitmask |= (1 << int(day))
        #     cleaned_data['days'] = bitmask   # 비트마스크 값으로 변환된 정수(bitmask)를 모델의 'days' 필드에 저장
        # else:
        #     self.add_error('days', '필수 입력값 입니다.')
