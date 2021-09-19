from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r"^\+?1?\d{8,15}$",
                             message='First input country code eg.(+48), then the number.')

gender = [
    ('F', 'Female'),
    ('M', 'Male'),
]
