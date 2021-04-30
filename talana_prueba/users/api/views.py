from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser , IsAuthenticated ,AllowAny
from .serializers import UserSerializer , UserCreate ,AccountVerificationSerializer , serializers
from django.contrib.auth import password_validation , authenticate
from talana_prueba.competition.models import CompetitionTicketModel

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_permissions (self) :

        permission_classes = []
        if self.action in ['register' , 'verify'] :

            permission_classes = [AllowAny]
        
        else :
            permission_classes = [IsAuthenticated , ]

        return [p() for p in  permission_classes]


    def get_serializer_class(self):

        if self.action == 'register':
            serializer_class = UserCreate
        else :
            serializer_class = UserSerializer

        return serializer_class


    def validate(self , data):
        #import pdb; pdb.set_trace()
        password = data['password']

        password_validation.validate_password(password)


        return data




    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'])
    def verify(self, request , *args , **kwargs):
        """
        /api/users/verify/
        Account verification.
        """
        if "token" in self.request.query_params.keys() :
            request.data['token'] = self.request.query_params['token']
        else :
            request.data['token'] = ''


        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulations your account is verified and you now participating in the event c: !!'}
 
        return Response(data, status=status.HTTP_200_OK)


    
    @action(detail=False , methods=['post'])
    def register(self , request):
        """
            /api/users/register/
            add user and create ticket to event
        """

        get_serializer  = self.get_serializer_class()
        serializer = get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(UserSerializer(user).data ,200)