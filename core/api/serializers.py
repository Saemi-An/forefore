from rest_framework import serializers

from core.products.models import Cookies, Products, Sales


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class CookiesSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(many=False)

    class Meta:
        model = Cookies
        fields = '__all__'

class SalesCookieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sales
        fields = '__all__'