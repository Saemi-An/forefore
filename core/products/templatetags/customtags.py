from django import template

register = template.Library()


# 천단위 콤마
@register.filter
def intcomma(value):
    return "{:,}".format(int(value))


# DB에 이미지명 앞에 cookies/ 떼어주기
@register.filter
def drop_upload_to(value):  # cookies/0_고구마휘낭시에.jpg
    return str(value).split('cookies/')[1]
