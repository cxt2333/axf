from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from cart.CartPermissions import CartPermission
from cart.MyAuthentications import CartAuthentication
from cart.cartserializers import CartAddSerializer, CartSerializer
from home.models import *

# Create your views here.
from user.util import token_confirm


class CartAddView(CreateAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = CartAddSerializer
    # 用户认证
    authentication_classes = CartAuthentication,
    # 用户认证授权
    permission_classes = CartPermission,

    def create(self, request, *args, **kwargs):
        # 生成序列化器
        serializer = self.get_serializer(data=request.data)
        # 验证
        if serializer.is_valid():
            # 使用身份认证验证
            # # 判断token是否存在或过期
            # token = serializer.data.get('token')
            # try:
            #     uid = token_confirm.confirm_validate_token(token)
            # except Exception as e:
            #     print(e)
            #     return Response({
            #         'code': 1006,
            #         'msg': 'token失效',
            #         'data': {'user_info': serializer.errors},
            #     })
            # # 判断用户是否存在
            # try:
            #     user = AxfUser.objects.get(pk=uid)
            # except Exception as e:
            #     print(e)
            #     return Response({
            #         'code': 1006,
            #         'msg': '用户不存在',
            #         'data': {'user_info': serializer.errors},
            #     })
            user = request.user
            # 在购物车里找到用户记录
            carts = AxfCart.objects.filter(c_user=user)
            # 获取商品id
            goodsid = serializer.data.get('goodsid')
            # 获取商品
            the_good = AxfGoods.objects.get(pk=goodsid)
            # 判断购物车是否有相同商品
            carts = carts.filter(c_goods=the_good)
            # 购物车有该商品
            if carts.exists():
                # 商品数量加1
                cart = carts.first()
                cart.c_goods_num += 1
                cart.save()
            # 没有该商品
            else:
                cart = AxfCart()
                cart.c_goods_num = 1
                cart.c_goods = the_good
                cart.c_user = user
                cart.c_is_select = 1
                cart.save()
            return Response({
                'code': 200,
                'msg': '添加成功',
                'data': {'c_goods_num': cart.c_goods_num},
            })
        return Response({
            'code': 1006,
            'msg': '商品不存在',
            'data': {'user_info': serializer.errors},
        })


class CartListView(ListAPIView):
    queryset = AxfCart.objects.all()
    serializer_class = CartSerializer
    # 用户认证(要逗号)
    authentication_classes = CartAuthentication,
    # 用户认证授权(要逗号)
    permission_classes = CartPermission,

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # 过滤用户购物车记录
        queryset = queryset.filter(c_user=request.user)
        queryset = self.filter_queryset(queryset)

        # 计算总价
        total = 0
        for rec in queryset:
            print(rec.c_goods_num, rec.c_goods.price)
            total += rec.c_goods_num * rec.c_goods.price
        print(total)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'msg': '查询成功',
            'data':{
                'title': '购物车',
                'is_all_select': True,
                'total_price': total,
                'carts': serializer.data
            }
        })
