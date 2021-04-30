


#PYTHON
import random
from datetime import timedelta

# DJANGO
from config import celery_app
from celery.decorators import task
from django.db.models import Q

#MODELS 
from talana_prueba.competition.models import CompetitionTicketModel as competition



@task(name="EventTask",  soft_time_limit=timedelta(minutes=1).seconds, time_limit=timedelta(minutes=1).seconds)
def EventTask():
    if len(competition.objects.filter(status='winner')) == 0 :

        contestant = competition.objects.all()

        tickets = [ i[0] for i in contestant.values_list("id") ] 
        winner = None
        last_ticket = len(tickets)
        random.shuffle(tickets)
        iterations = 10 
        for i in range(10):
            winner = random.randint(0 , last_ticket)

        winner = contestant.get(id=winner)
        winner.status  = 'winner'
        winner.save()
        print(f"winner!! {winner}")
    
    else :
        print("winner exist")
