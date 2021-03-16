from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from axf import settings
from home.models import *
# Create your views here.
from market.goodfilters import GoodsFilter
from market.markserializers import GoodTypeSerializer, GoodsSerializer


class GoodTypeListView(APIView):
    def get(self, request):
        # 获取商品类型
        queryset = AxfFoodtype.objects.all()
        # 序列化
        goodtype_serializer = GoodTypeSerializer(queryset, many=True)
        return Response({
            'code': 200,
            'msg': '请求成功',
            'data': goodtype_serializer.data
        })


class GoodListView1(APIView):
    def get(self, request, *args, **kwargs):
        # 获取类型参数
        tid = request.query_params.get('typeid')
        # 参数获取的类型都是字符串，用int()转化类型
        # 商品列表
        good_list = AxfGoods.objects.filter(categoryid=int(tid))
        # 过滤子类商品
        childcid = int(request.query_params.get('childcid', 0))
        if childcid > 0:
            good_list = good_list.filter(childcid=childcid)
        print(good_list)
        # 对结果排序
        order_rule = request.query_params.get('order_rule', 0)
        if order_rule == '1':
            good_list = good_list.order_by('price')
        elif order_rule == '2':
            good_list = good_list.order_by('-price')
        elif order_rule == '3':
            good_list = good_list.order_by('productnum')
        elif order_rule == '4':
            good_list = good_list.order_by('-productnum')

        # 序列化
        good_serializer = GoodsSerializer(good_list, many=True)

        # 商品分类子列表
        goodtype = AxfFoodtype.objects.filter(typeid=int(tid)).first()
        childtypenames = goodtype.childtypenames
        childtypenames = childtypenames.split('#')
        childtypenames = [value.split(':') for value in childtypenames]
        childtypenames = [{'child_name': elem[0], 'child_value': elem[1]} for elem in childtypenames]
        return Response({
            'code': 200,
            'msg': '查询成功',
            'data': {
                'goods_list': good_serializer.data,
                'order_rule_list': settings.ORDER_RULE_LIST,
                'foodtype_childname_list': childtypenames,
            },
        })


class GoodListView(ListAPIView):
    queryset = AxfGoods.objects.all()
    serializer_class = GoodsSerializer
    # 过滤器
    filter_class = GoodsFilter

    # 过滤器重写
    def list(self, request, *args, **kwargs):
        # filter_queryset调用过滤器对查询结果集进行过滤
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # 获取类型参数
        tid = request.query_params.get('typeid')
        # 商品分类子列表
        goodtype = AxfFoodtype.objects.filter(typeid=int(tid)).first()
        childtypenames = goodtype.childtypenames
        childtypenames = childtypenames.split('#')
        childtypenames = [value.split(':') for value in childtypenames]
        childtypenames = [{'child_name': elem[0], 'child_value': elem[1]} for elem in childtypenames]
        return Response({
            'code': 200,
            'msg': '查询成功',
            'data': {
                'goods_list': serializer.data,
                'order_rule_list': settings.ORDER_RULE_LIST,
                'foodtype_childname_list': childtypenames,
            },
        })
