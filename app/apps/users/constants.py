from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",
                             message='First input country code eg.(+48), then the number.')

gender = [
    ('female', 'Female'),
    ('male', 'Male'),
]

fields = ['gender', 'first_name', 'last_name', 'country', 'city',
          'email', 'username', 'phone']
longer_path = {'first_name': 'first',
               'last_name': 'last',
               'country': 'country',
               'city': 'city',
               'username': 'username'}

second_parameter = {'first_name': 'name',
                    'last_name': 'name',
                    'country': 'location',
                    'city': 'location',
                    'username': 'login'}

shorter_path = ['gender', 'email', 'phone']
