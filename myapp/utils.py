import re
from rest_framework.validators import ValidationError

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
phone_pattern = r'^\+998\d{9}$'


def validate_email_or_phone(value):

    if re.match(email_pattern, value) is not None:
        return 'email'
    elif re.match(phone_pattern, value) is not None:
        return 'phone'
    else:
        data = {
            'status':False,
            'message':'Validation Error'
        }
        raise ValidationError(data)
