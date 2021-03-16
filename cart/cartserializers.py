# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/14 14:17
from rest_framework import serializers

from home.models import AxfGoods, AxfCart
from market.markserializers import GoodsSerializer


class CartAddSerializer(serializers.Serializer):
    goodsid = serializers.CharField(required=True)
    token = serializers.CharField()

    def validate_goodsid(self, value):
        value = int(value)
        the_goods = AxfGoods.objects.filter(pk=value).first()
        if not the_goods:
            raise serializers.ValidationError('商品不存在')
        return value

    def validate_token(self, data):
        if not data:
            raise serializers.ValidationError('token不存在')
        return data


class CartSerializer(serializers.ModelSerializer):
    # 关联序列化
    c_goods = GoodsSerializer()

    class Meta:
        model = AxfCart
        fields = '__all__'
