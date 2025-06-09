from django.test import TestCase  # noqa: F401

from .models import Times
# Create your tests here.

def generate_times():
    for i in range(300):
        test = Times(name='테스트용', start=10, end=12, interval=20)
        test.save()