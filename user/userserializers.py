# coding:utf-8
# 学校：闽江学院
# 编写人：陈端倪
# 开发时间：2021/3/12 18:29
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from home.models import AxfUser


# 用户序列化器
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AxfUser
        fields = '__all__'


# 用户注册序列化器
class UserRegisterSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True)
    u_password = serializers.CharField(min_length=3, max_length=12,
                                       error_messages={
                                           'max_length': '最大长度不超过12个字符',
                                           'min_length': '最小长度不能少于3个字符'
                                       })
    u_password2 = serializers.CharField(min_length=3, max_length=12,
                                        error_messages={
                                            'max_length': '最大长度不超过12个字符',
                                            'min_length': '最小长度不能少于3个字符'
                                        })
    u_email = serializers.EmailField(required=True)

    # 验证用户是否唯一
    def validate_u_username(self, attrs):
        user = AxfUser.objects.filter(u_username=attrs).first()
        if user:
            raise serializers.ValidationError({'u_username': '用户名已经存在'})
        return attrs

    # 全局验证
    def validate(self, attrs):
        password = attrs.get('u_password')
        u_password2 = attrs.get('u_password2')
        if password != u_password2:
            raise serializers.ValidationError({'u_password': '两次密码不一致'})
        return attrs

    # 添加用户
    def create(self, validated_data):
        user = AxfUser()
        password = validated_data.get('u_password')
        # 对密码加密
        password = make_password(password)
        user.u_username = validated_data.get('u_username')
        user.u_password = password
        user.u_email = validated_data.get('u_email')
        user.is_active = 1  # 已激活
        user.is_delete = 0  # 未删除
        user.save()
        return user


# 登录序列化器
class LoginSerializer(serializers.Serializer):
    u_username = serializers.CharField(required=True)
    u_password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('u_username')
        password = attrs.get('u_password')

        # 判断用户是否存在
        user = AxfUser.objects.filter(u_username=username)
        # .exists()判断是否存在
        if not user.exists():
            raise serializers.ValidationError({'u_username': '用户不存在'})
        # 验证通过用户存在
        user = user.first()
        # 验证密码，check_password(明文密码，签名密码)，相等放回true，否则放回False
        if not check_password(password, user.u_password):
            raise serializers.ValidationError({'invalid': '用户名或密码错误'})
        return attrs