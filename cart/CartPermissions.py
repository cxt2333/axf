# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/14 23:46
from rest_framework.permissions import BasePermission

from home.models import AxfUser


class CartPermission(BasePermission):
    def has_permission(self, request, view):
        # 登录用户返回True,未登录用户返回False
        return isinstance(request.user, AxfUser)
