from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User,VIA_PHONE,VIA_EMAIL
from .utils import validate_email_or_phone

class SignUp(serializers.ModelSerializer):
    auth_type = serializers.CharField(required=False,read_only=True)
    auth_status = serializers.CharField(required=False,read_only=True)

    def __init__(self,*args,**kwargs):
        super(SignUp,self).__init__(*args,**kwargs)
        self.fields['email_phone']=serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('auth_type','auth_status')

    def validate(self,data):
        user_inp = data.get('email_phone')
        emf = validate_email_or_phone(user_inp)

        if emf == 'email':
            data = {
                'auth_type':VIA_EMAIL,
                'email':user_inp
            }
        elif emf == 'phone':
            data = {
                'auth_type': VIA_PHONE,
                'phone_number': user_inp
            }
        else:
            data = {
                'status':False,
                'message':'Validation Error'
            }
            raise ValidationError(data)
        return data