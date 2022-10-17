from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank = True)
    title = models.CharField(max_length= 200)
    #title is for the headline with limited words etc
    description = models. TextField(null=True, blank = True)
    #text field is like filling text in a box, a message smt
    complete = models.BooleanField(default=False)
    # a true/false field
    create =  models.DateTimeField(auto_now_add = True)
    # tự động nhập thời gian etc 

    def __str__(self):
        return self.title
    #set the default value to title 
    class Meta:
        #sắp xếp theo thứ tự complete vì nếu nó xong thì cho nó cút xuống dưới
        #vì k cần phải để ý tới nó nữa 
        ordering = ['complete']
    