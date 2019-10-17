from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
# Create your models here.



class State(models.Model):
    state_name = models.CharField(max_length=400,null=True,blank=True)

    def __str__(self):
        return self.state_name


class Lawyer(models.Model):
    STATE = (
        ('2019', '2019'),
        ('2018', '2018'),
        ('2017', '2017'),
        ('2016', '2016'),
        ('2015', '2015'),
        ('2014', '2014'),
        ('2013', '2013'),
        ('2012', '2012'),
        ('2011', '2011'),
        ('2010', '2010'),
        ('2009', '2009'),
        ('2008', '2008'),
        ('2007', '2007'),
        ('2006', '2006'),
        ('2005', '2005'),
        ('2004', '2004'),
        ('2003', '2003'),
        ('2002', '2002'),
        ('2001', '2001'),
        ('2000', '2000'),
        
    )
    
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address1 = models.CharField(max_length=400,blank=True,null=True)
    address2 = models.CharField(max_length=400,blank=True,null=True)
    city = models.CharField(max_length=128,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=True,blank=True)
    zipcode = models.CharField(max_length=128,blank=True,null=True)
    phone_number = models.CharField(max_length=128,blank=True,null=True)
    license_in = models.CharField(max_length=128,blank=True,null=True)
    license_id = models.CharField(max_length=128,blank=True,null=True)
    year_admitted = models.CharField(choices=STATE,max_length=128,blank=True,null=True)
    profile_image = models.ImageField(upload_to='profile_images',blank=True)
    
    def __str__(self):
        return self.user.username

