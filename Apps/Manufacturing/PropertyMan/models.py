from django.db import models
from django.utils.translation import ugettext as _
from Apps.Manufacturing.const import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import signals
# Create your models here.


class Role_user_man(models.Model):
	user = models.OneToOneField(User)
	access_level = models.CharField(max_length=30, choices=LEVEL_AKSES_CHOICES, verbose_name='Level Akses')
	intern_occupation = models.CharField(max_length=30, blank=True, null=True)
	intern_date_register = models.DateField(auto_now_add=True)
	department = models.CharField(max_length=30, choices=STACHOLDER, verbose_name='Stacholder', blank=True, null=True)
	
	class Meta:
		verbose_name = 'Hak Akses'
		verbose_name_plural = 'Hak Akses'
		ordering = ['id']
		
	def __unicode__(self):
		return "%s" % self.user
		
def create_user_profile(sender, instance, created, **kwargs):  
	if created == True: 
		profile, created = Role_user_man.objects.get_or_create(user=instance)
        
post_save.connect(create_user_profile, sender=User)
