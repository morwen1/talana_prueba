from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from .serializers import UserSerializer , UserCreate
from django.contrib.auth import password_validation , authenticate
from talana_prueba.competition.models import CompetitionTicketModel

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_permissions (self) :

        permission_classes = []
        if self.action == 'create' :

            permission_classes = [IsAdminUser , ]
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
        ticket = CompetitionTicketModel.objects.create(
            contestant_user= user 
        )
        ticket.save()
        return Response(UserSerializer(user).data ,200)