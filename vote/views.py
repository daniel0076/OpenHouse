from django.shortcuts import render
from .models import Participant,Vote
from ipware.ip import get_real_ip,get_ip
from django.db import IntegrityError
import datetime
def vote(request):
    if request.POST:
        ip = get_ip(request)
        if ip is not None:
            participant_id = request.POST['participant']
            participant = Participant.objects.get(id=participant_id)
            vote = Vote(participant=participant,ip=ip,date=datetime.date.today())
            try:
                vote.save()
            except IntegrityError as e:
                error_msg = "每人一天限投一票"
    participants = Participant.objects.all()
    return render(request,'vote.html',locals())
                
def index(request):
    return render(request,'index.html',locals())
