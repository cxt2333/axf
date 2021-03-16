# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/11 23:53

from django_filters import rest_framework as filters
from home.models import AxfGoods


class GoodsFilter(filters.FilterSet):
    typeid = filters.CharFilter(field_name='categoryid')
    childcid = filters.CharFilter(field_name='childcid', method='filter_child_type')
    order_rule = filters.CharFilter(field_name='order_rule', method='order_good')

    class Meta:
        model = AxfGoods
        fields = ['categoryid']

    def filter_child_type(self, queryset, name, value):
        # value大于0，进行子类过滤
        if int(value) > 0:
            return queryset.filter(childcid=int(value))
        # 如果value等于0，没子类
        return queryset

    def order_good(self, queryset, name, value):
        if value == '1':
            queryset = queryset.order_by('price')
        elif value == '2':
            queryset = queryset.order_by('-price')
        elif value == '3':
            queryset = queryset.order_by('productnum')
        elif value == '4':
            queryset = queryset.order_by('-productnum')

        return queryset