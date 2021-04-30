from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation , authenticate


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]

        




class UserCreate(serializers.Serializer):
    email = serializers.EmailField(
        validators = [UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=17 )
    def validate(self , data):
        #import pdb; pdb.set_trace()
        password = data['password'] 
        phone = data['phone'] 
        if password  == ''   :
            raise serializers.ValidationError('password is required')
        else: 
            password_validation.validate_password(password)
        if phone  == ''   :
            raise serializers.ValidationError('phone is required')
        
        
        
        return data

    def create(self , data) : 
        #
        
        user = User.objects.create_user(**data)
        user.save()
       
        return user