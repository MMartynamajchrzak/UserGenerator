from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r"^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$",
                             message='First input country code eg.(+48), then the number.')

gender = [
    ('female', 'Female'),
    ('male', 'Male'),
]
