from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response

# Create your views here.
from home.models import AxfUser
from user.userserializers import UserSerializer, UserRegisterSerializer, LoginSerializer
from user.util import token_confirm


class UserShowView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        # 获取token
        token = request.query_params.get('token')
        print(token)
        try:
            uid = token_confirm.confirm_validate_token(token)
        except Exception as e:
            print(e)
            return Response({
                'code': 107,
                'msg': 'token失效，请重新登录',
                'data': {},
            })

        try:
            user = AxfUser.objects.get(pk=uid)
        except Exception as e:
            print(e)
            return Response({
                'code': 107,
                'msg': '用户不存在',
                'data': {},
            })

        # 存在用户，序列化
        serializer = UserSerializer(user)
        return Response({
            'code': 200,
            'msg': '用户查询成功',
            'data': {'user_info': serializer.data},
            'orders_not_pay_num': 0,  # 待付款
            'orders_not_send_num': 0  # 待收货
        })


class UserRegisterView(GenericAPIView):
    queryset = AxfUser.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request):
        # 反向序列化
        serializer = self.get_serializer(data=request.data)
        # 验证
        if serializer.is_valid():
            # 保存
            user = serializer.save()
            print(user)
            return Response({
                'code': 200,
                'msg': '注册成功',
                'data': {'user_id': user.id}
            })
        return Response({
            'code': 105,
            'msg': '注册失败',
            'data': {'info': serializer.errors}
        })


class UserLoginView(CreateAPIView):
    queryset = AxfUser
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证通过，
        if serializer.is_valid():
            username = serializer.data.get('u_username')
            user = AxfUser.objects.filter(u_username=username).first()
            # 生成token
            token = token_confirm.generate_validate_token(user.id)
            return Response({
                'code': status.HTTP_200_OK,
                'msg': '登录成功',
                'data': {'user_id': user.id, 'token': token}
            })
        # 验证没通过
        else:
            print(serializer.errors)
            return Response({
                'code': 1004,
                'msg': '账号或密码错误',
                'data': {'info': serializer.errors, 'token': '1'}
            })
