from .models import UserModel
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class UserModelSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)

    class Meta:
        model = UserModel
        fields = ['id','username','first_name', 'last_name', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        user = UserModel.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # Check if 'password' is in validated_data, indicating a password update
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        # If 'password' is not present, perform a regular update
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance
