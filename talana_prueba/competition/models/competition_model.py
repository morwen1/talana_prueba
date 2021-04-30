#DJANGO
from django.db import models 
#MODELS 
from talana_prueba.utils.abstract_model import AbstractPruebaModel
from talana_prueba.users.models import User




choices_status = [
    ("winner","winner")
]

class CompetitionTicketModel (AbstractPruebaModel):
    contestant_user = models.ForeignKey(User , on_delete=models.DO_NOTHING  )
    status = models.CharField(
        max_length=100 , 
        help_text= "status: winner or none" , 
        choices=choices_status , null=True
        )
    event_date = models.DateField(auto_now=True)
    notified = models.BooleanField(default=False , help_text="if status == winner notified == true")
    