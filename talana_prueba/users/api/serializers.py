
# Django
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import password_validation , authenticate
from talana_prueba.competition.models import CompetitionTicketModel


# Utilities
import jwt



#TASK
from talana_prueba.users.tasks import send_confirmation_email

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
        send_confirmation_email.apply_async(({"user_pk": user.pk} ,None )
            ,
            countdown=2 
            )
       
        return user









class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        #import pdb ; pdb.set_trace() 
        user = User.objects.get(email=payload['user'])
        user.is_verified = True
        ticket = CompetitionTicketModel.objects.create(
            contestant_user= user 
        )
        ticket.save()
        user.save()
