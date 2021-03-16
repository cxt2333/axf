# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/15 23:54

from django_filters import rest_framework as filters

from axf import settings
from home.models import AxfOrder


class OrderFilter(filters.FilterSet):
    o_status = filters.CharFilter(field_name='o_status', method='filter_by_status')

    class Meta:
        model = AxfOrder
        fields = ['o_status']

    def filter_by_status(self, queryset, name, value):
        # 未付款
        if value == 'not_pay':
            return queryset.filter(o_status=settings.ORDER_STATUS_NOT_PAY)
        # 未发货
        elif value == 'not_send':
            return queryset.filter(o_status=settings.ORDER_STATUS_NOT_SEND)
        return queryset
