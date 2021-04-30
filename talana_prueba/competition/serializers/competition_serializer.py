#DJANGO
#DJANGODRF
from rest_framework import serializers 
#MODELS  
from talana_prueba.competition.models import CompetitionTicketModel
from talana_prueba.users.models import User





class UserTicketCompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields  = [ "username" ,"email" ]





class CompetitionTickeSerializer(serializers.ModelSerializer):
    contestant_user = UserTicketCompetitionSerializer(read_only= True)
    class Meta:
        model = CompetitionTicketModel
        fields = ['contestant_user' , 'status']
    
