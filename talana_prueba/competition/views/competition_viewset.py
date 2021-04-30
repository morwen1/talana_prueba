
#DJANGO
from django.db.models import Prefetch

#DJANGODRF(
from rest_framework.mixins import (
    ListModelMixin , 
    RetrieveModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import (
    IsAuthenticated ,IsAuthenticatedOrReadOnly , 
    IsAdminUser , IsAuthenticatedOrReadOnly
    )
from rest_framework.decorators import action
from rest_framework.response import Response

#SERIALZER 
from talana_prueba.competition.serializers import CompetitionTickeSerializer as competition_serializer
#MODEL
from talana_prueba.competition.models import CompetitionTicketModel as competition

#tasks 
from talana_prueba.competition.task import EventTask


class CompetitionViewset(ListModelMixin , RetrieveModelMixin ,GenericViewSet):

    serializer_class = competition_serializer

    def get_permissions(self) :
        permissions_classes=[]
        if self.action == 'my_state' : 
            permissions_classes = [IsAuthenticated , ]
        if self.action in ['list' , 'retrieve' , 'winner']:
            permissions_classes = [IsAuthenticatedOrReadOnly ,]
        if self.action == 'start_event' : 
            permissions_classes = [ IsAuthenticated , IsAdminUser ,]
       
        return [permission() for  permission in permissions_classes ]


    def get_queryset(self):
        if self.action == 'my_state' : 
            queryset = competition.objects.filter(contestant_user = self.request.user).last()

        if self.action in ['list' , 'retrieve']:
                    

            queryset = competition.objects.all().order_by("-created_at")
            #prefetch para evitar problemas de n+1 en las request y asi hacer las consultas mas rapidas
            queryset.prefetch_related(
                Prefetch("contestant_user")
            )

        
        if self.action == 'winner' :
            queryset = competition.objects.filter(status='winner').last()


        return queryset 

    
    @action(detail=False , methods= ['GET'])
    def winner(self, request):
        """
        /api/competition/winner/

        return the winner 
        """
        queryset = self.get_queryset()
        #import pdb ; pdb.set_trace()
        datar = self.serializer_class(queryset).data
        return Response(data= datar, status = 200)

         

    @action(detail=False , methods=['GET'])
    def my_state (self ,  request ) :
        """
        /api/competition/my_state/
        return information of the user logged only
        """
        queryset = self.get_queryset()
        datar = self.serializer_class(queryset).data
        #import pdb ; pdb.set_trace()
        return Response(data= datar, status = 200)


    @action(detail=False , methods=['POST'])
    def start_event(self , request) : 
        """
        /api/competition/start_event/
        initiate async task to choice a winner 
        only admin
        """
        EventTask.apply_async()
        return Response(data={"msg":"event started "}, status=200)
