from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from home.homeserializers import *
from home.models import *


class HomeListView(GenericAPIView):
    """
    get:
    获取首页数据
    """
    queryset = AxfWheel
    serializer_class = WheelSerializer

    def get(self, request):
        # 数据查询
        wheel_queryset = AxfWheel.objects.all()
        nav_queryset = AxfNav.objects.all()
        mustbuy_queryset = AxfMustbuy.objects.all()
        shop_queryset = AxfShop.objects.all()
        mainshow_queryset = AxfMainshow.objects.all()

        # 序列化
        wheel_data = WheelSerializer(wheel_queryset, many=True)
        nav_data = NavSerializer(nav_queryset, many=True)
        mustbuy_data = MustBuySerializer(mustbuy_queryset, many=True)
        shop_data = ShopSerializer(shop_queryset, many=True)
        mainshow_data = MainShowSerializer(mainshow_queryset, many=True)

        return Response({
            'code': 200,
            'msg': '请求成功',
            'data': {
                'main_wheels': wheel_data.data,
                'main_navs': nav_data.data,
                'main_mustbuys': mustbuy_data.data,
                'main_shops': shop_data.data,
                'main_shows': mainshow_data.data
            }
        })
