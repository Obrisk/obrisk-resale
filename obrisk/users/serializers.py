from rest_framework import serializers
from obrisk.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'password']

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
