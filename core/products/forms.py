from django import forms
from .models import Products, Times

class ProductAdd(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'
        widgets = {
            'category' : forms.Select(attrs={'class': 'md-reg add_md-reg_class_to_options'}),
            'name' : forms.TextInput(attrs={'class': 'md-reg', 'placeholder': '입력해 주세요.'}),
            'price' : forms.NumberInput(attrs={'class': 'md-reg', 'placeholder': '입력해 주세요.'}),
            'cmt' : forms.Textarea(attrs={'rows': 3, 'class': 'md-reg', 'placeholder': '입력해 주세요.'}),
            'img' : forms.ClearableFileInput(attrs={'id': 'fileUpload', 'class': 'display-none'}),
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
        exclude = ('selected', )
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'md-reg', 'placeholder': '입력해 주세요.'}),
            'start' : forms.Select(
                choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'end' : forms.Select(
                choices=[('', '선택')] + [(i, f'{i}시') for i in range(10, 20)],
                attrs={'class': 'md-reg add_md-reg_class_to_options'}
                ),
            'interval' : forms.Select(attrs={'class': 'md-reg add_md-reg_class_to_options'}),
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
