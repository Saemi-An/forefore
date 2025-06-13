from django import template
from datetime import date

register = template.Library()

# 천단위 콤마
@register.filter
def intcomma(value):
    return "{:,}".format(int(value))

# DB에 이미지명 앞에 cookies/ 떼어주기
@register.filter
def drop_upload_to(value):  # cookies/0_고구마휘낭시에.jpg
    return str(value).split('cookies/')[1]

# DB에 이미지명 앞에 cakes/ 떼어주기
@register.filter
def drop_upload_to_cake(value):  # cakes/2_딸기우유생크림케이크.jpg
    return str(value).split('cakes/')[1]

# 비트마스킹 표현
@register.filter
def get_days_from_bitmask(bitmask: int) -> str:
    days = [
        (0, '월'),
        (1, '화'),
        (2, '수'),
        (3, '목'),
        (4, '금'),
        (5, '토'),
        (6, '일'),
    ]

    result = [label for value, label in days if bitmask & (1 << value)]
    return ', '.join(result)

# 한국식 날짜 표현
@register.filter
def format_date(date_obj: date) -> str:
    # return date_obj.strftime('%Y년 %m월 %d일')   # 2025년 01월 01일
    year_short = str(date_obj.year)[2:]   # '2025' -> '25'
    return f"{year_short}년 {date_obj.month}월 {date_obj.day}일"