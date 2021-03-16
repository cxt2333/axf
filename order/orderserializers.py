# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/15 17:13
from rest_framework import serializers
from home.models import AxfOrder, AxfOrdergoods
from market.markserializers import GoodsSerializer


class OrderGoodsSerializer(serializers.ModelSerializer):
    o_goods = GoodsSerializer()
    class Meta:
        model = AxfOrdergoods
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfOrder
        fields = '__all__'

    def to_representation(self, instance):
        # 调用父类方法获取序列化后的数据
        data = super().to_representation(instance)
        order_goods = instance.goods.all()
        serializer = OrderGoodsSerializer(order_goods,many=True)
        data['order_goods_info'] = serializer.data
        return data
