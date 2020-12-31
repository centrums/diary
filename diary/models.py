import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import ModelForm

# Create your models here.
class Entry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank = False, null = False)
    content = models.TextField(blank = False, null = False)
    pub_date = models.DateTimeField('date published')
    edit_date = models.DateTimeField('date edited')
    
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'content']
        
    def clean(self):
 
        # data from the form is fetched using super function
        super(EntryForm, self).clean()
         
        # extract the title and content field from the data
        title = self.cleaned_data.get('title')
        content = self.cleaned_data.get('content')
 
        # conditions to be met for the title length
        if len(title) > 100:
            self._errors['title'] = self.error_class([
                'Maximum 100 characters allowed for title'])
        if len(content) <10:
            self._errors['content'] = self.error_class([
                'Content should contain a minimum of 10 characters'])
 
        # return any errors if found
        return self.cleaned_data

