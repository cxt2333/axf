# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/14 21:36
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException

from home.models import AxfUser
from user.util import token_confirm


class CartAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 获取token
        token = request.data.get('token', None) or request.query_params.get('token', None)
        try:
            uid = token_confirm.confirm_validate_token(token)
        except Exception as e:
            # print(e)
            # raise APIException({'code': 1006, 'msg': 'token失效', 'data': {}, })
            return
        # 判断用户是否存在
        try:
            user = AxfUser.objects.get(pk=uid)
        except Exception as e:
            # print(e)
            # raise APIException({'code': 1006, 'msg': '用户不存在', 'data': {}, })
            return
        # 验证成功
        return user, token
