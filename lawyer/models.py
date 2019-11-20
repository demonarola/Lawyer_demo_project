from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.conf import settings
from django.core.validators import RegexValidator
# from django.contrib.postgres.fields import ArrayField
# Create your models here.


# title_valid = '^[A-Za-z]+|,| |/|{2}[a-z0-9]{1,30}'
# title_review = '^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$'

class State(models.Model):
    state_name = models.CharField(max_length=400,null=True,blank=True)

    def __str__(self):
        return self.state_name


class Lawyer(models.Model):
    YEAR = (
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
    address1 = models.CharField(max_length=400,blank=False,null=False,validators=[
        RegexValidator(regex='(^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$',message='Enter Valid Address1')
    ])
    address2 = models.CharField(max_length=400,blank=False,null=False,validators=[
        RegexValidator(regex='(^[A-Za-z0-9]+|,| |/|[A-Za-z]+)+[A-Za-z0-9]+|,| |$',message='Enter Valid Address2')
    ])
    city = models.CharField(max_length=128,blank=False,null=False,validators=[
        RegexValidator(regex='[A-Za-z]{2}[a-z]+$',message='City should only contain letters and mustcontains atleast 2 chracters..')
    ])
    state = models.ForeignKey(State,on_delete=models.CASCADE,null=False,blank=False)
    zipcode = models.CharField(max_length=128,blank=False,null=False,validators=[
        RegexValidator(regex='^[0-9]{6}$',message='Enter Valid Zipcode')
    ])
    phone_number = models.CharField(max_length=128,blank=False,null=False,validators=[
        RegexValidator(regex='^[6|7|8|9]+[0-9]{9}$',message='Enter 10 digit number')
    ])
    license_in = models.ForeignKey(State,on_delete=models.CASCADE,blank=False,null=False,related_name='license_id')
    license_id = models.CharField(max_length=128,blank=False,null=False,validators=[
        RegexValidator(regex='^[A-Za-z0-9]*$',message='Enter Valid License Id')
    ])
    year_admitted = models.CharField(choices=YEAR,max_length=128,blank=False,null=False,)
    profile_image = models.ImageField(upload_to='profile_images',blank=False,null=False,)
    

    
    def __str__(self):
        return self.user.username



class Practice_area(models.Model):
    practice = models.CharField(max_length=128,blank=True, null=True)
    
    def __str__(self):
        return self.practice

    class Meta:
        verbose_name_plural = 'Practice Area'


class  Sub_practice_area(models.Model):  
    practice_id = models.ForeignKey(Practice_area,on_delete=models.CASCADE, blank=True, null=True)
    practice_type = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.practice_type

    class Meta:
        verbose_name_plural = 'Sub Practice Area'


class Lawyer_practice_area(models.Model):
    lawyer_id = models.ForeignKey(Lawyer,on_delete=models.CASCADE,null=True,blank=True)
    practice_area = models.ForeignKey(Practice_area,on_delete=models.CASCADE,blank=True,null=True)
    sub_practice_area = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.sub_practice_area


class Review_Lawyer(models.Model):
    lawyer_id = models.ForeignKey(Lawyer,on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(max_length=228, blank=False, null=False)
    review = models.CharField(max_length=5000, blank=False, null=False)
    rating = models.IntegerField(blank=False)
    date = models.DateField(blank=False, null=False,auto_now_add=True)

    def __str__(self):
        return self.lawyer_id.user.username

    class Meta:
        verbose_name_plural = 'Review Lawyer'

