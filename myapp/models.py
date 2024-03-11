import random
import uuid
from datetime import datetime,timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
REGULAR,SUPPORT,ADMIN = ('regular','support','admin')

NEW,CODE_VERIFY,DONE,IMAGE = ('new','code_verify','done','image')

VIA_PHONE,VIA_EMAIL = ('via_phone','via_email')


class User(BaseModel,AbstractUser):
    USER_ROLES = (
        (REGULAR,REGULAR),
        (SUPPORT,SUPPORT),
        (ADMIN,ADMIN)
    )

    AUTH_STEP = (
        (NEW,NEW),
        (CODE_VERIFY,CODE_VERIFY),
        (DONE,DONE),
        (IMAGE,IMAGE)
    )

    AUTH_TYPE = (
        (VIA_PHONE,VIA_PHONE),
        (VIA_EMAIL,VIA_EMAIL)
    )

    auth_type = models.CharField(max_length=255,choices=AUTH_TYPE)
    auth_status = models.CharField(max_length=255,choices=AUTH_STEP,default=NEW)
    user_role = models.CharField(max_length=255,choices=USER_ROLES,default=REGULAR)
    phone_number = models.CharField(max_length=13,unique=True,null=True,blank=True)
    email = models.CharField(max_length=255,unique=True,null=True,blank=True)
    image = models.ImageField(upload_to='user/images',null=True,blank=True)
    bio = models.CharField(max_length=255,null=True,blank=True)


    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def check_username(self):
        if not self.username:
            temp_username = f'telegram.{str(uuid.uuid4()).split('-')[-1]}'
            while User.objects.filter(username=temp_username).exists():
                temp_username = f'{temp_username}{random.randint(1,10)}'
            self.username = temp_username

    def check_pass(self):
        if not self.password:
            temp_password = f'telegram.{str(uuid.uuid4()).split('-')[-1]}'
            self.password = temp_password

    def check_hash(self):
        if not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)


    def save(self,*args,**kwargs):
        self.check_username()
        self.check_pass()
        self.check_hash()

        super(User,self).save(*args,**kwargs)

class UserCodeVerify(BaseModel):

    AUTH_TYPE = (
        (VIA_PHONE,VIA_PHONE),
        (VIA_EMAIL,VIA_EMAIL)
    )

    auth_type = models.CharField(max_length=255,choices=AUTH_TYPE)
    code = models.CharField(max_length=6)
    is_confirmed = models.BooleanField(default=False)
    expire_time = models.DateTimeField(null=True,blank=True)
    user = models.OneToOneField('myapp.User',on_delete=models.CASCADE,related_name='confirmation_codes')

    def __str__(self):
        return f'{self.user.username} {self.code}'

    def save(self,*args,**kwargs):
        if self.auth_type == VIA_EMAIL:
            self.expire_time = datetime.now() + timedelta(minutes=5)
        elif self.auth_type == VIA_PHONE:
            self.expire_time = datetime.now() + timedelta(minutes=2)

        super(UserCodeVerify,self).save(*args, **kwargs)
