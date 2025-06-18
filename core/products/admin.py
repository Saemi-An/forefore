from django.contrib import admin

from .models import Sales
from .models import Products, Times, Cookies
from .models import Options, Schedules, Cakes, CakeOptions, CakeSchedules
# from .forms import SchedulesForm

# from .models import BitDays
# from .forms import BitDaysForm

# 공통
admin.site.register(Sales)
# 구움과자
admin.site.register(Products)
admin.site.register(Times)
admin.site.register(Cookies)
# 홀케이크
admin.site.register(Options)
admin.site.register(Schedules)

# @admin.register(Schedules)
# class SchedulesAdmin(admin.ModelAdmin):
#     form = SchedulesForm
#     list_display = ('id', 'name', 'start_date', 'end_date', 'get_days_display', 'days', 'start_time', 'end_time', 'interval')

admin.site.register(Cakes)
admin.site.register(CakeOptions)
admin.site.register(CakeSchedules)

# @admin.register(BitDays)
# class BitDaysAdmin(admin.ModelAdmin):
#     form = BitDaysForm
#     list_display = ('id', 'days', 'get_days_display')