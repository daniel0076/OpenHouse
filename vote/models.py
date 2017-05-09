from django.db import models

class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(u'姓名',max_length=10)
    theme = models.CharField(u'主題',max_length=100)
    video = models.CharField(u'影片',max_length=100)
    school = models.CharField(u'學校',max_length=20)
    department = models.CharField(u'系級',max_length=20)
    intro = models.TextField()
    def get_votes(self):
        votes = sum([1 for i in Vote.objects.all() if i.participant.id == self.id])
        return votes
    class Meta:
        managed = True
        verbose_name = u"參賽者"
        verbose_name_plural = u"參賽者"
        
    
class Vote(models.Model):
    ip = models.CharField(max_length=40)
    date = models.DateField()
    participant = models.ForeignKey(Participant)
    class Meta:
        unique_together = ("ip", "date")
