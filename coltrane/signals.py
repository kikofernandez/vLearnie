from django.db.models import signals
from django.contrib.comments import Comment

from community.models import *

import datetime

def moderate_comment(sender, instance, **kwargs):
    if not instance.id:
        entry = instance.content_object
        #delta = datetime.datetime.now() - entry.pub_date
        delta = datetime.date.today() - entry.pub_date
        if delta.days > 30:
            instance.is_public = False
            
signals.pre_save.connect(moderate_comment, sender=Comment)