from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Pickups, Times

# @receiver(post_save, sender=Times)
# def create_pickup_instances(sender, instance, created, **kwargs):

#     if not created:  # 기존에 있는 인스턴스에 대해

#         with transaction.atomic():

#             # TIME 인스턴스를 수정시, selected 여부에 상관없이 무조건 PICKUP에서 삭제
#             Pickups.objects.filter(time_id=instance).delete()

#             # selected = True일때, PICKUP 인스턴스 생성
#             if instance.selected:
#                 start_time = instance.start
#                 end_time = instance.end
#                 interval = instance.interval

#                 # 시간 생성 로직
#                 all_pickup_times = list(Pickups.objects.all().values_list('time', flat=True))  # 중복검사용
#                 current_time = start_time * 60  # 시작시간을 분으로 변환
#                 end_time_in_minutes = end_time * 60  # 종료시간을 분으로 변환

#                 while current_time <= end_time_in_minutes:
#                     hour = current_time // 60
#                     minute = current_time % 60

#                     time_str = f'{hour:02}:{minute:02}'
#                     if time_str not in all_pickup_times:  # 중복 시간 없을 때에만 생성
#                         Pickups.objects.create(str_time=time_str, time=instance)
#                     current_time += interval
