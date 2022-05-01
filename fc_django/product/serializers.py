from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__' # 이렇게 하면 자동으로 모델 안에 있는 모든 필드들을 가져온다.