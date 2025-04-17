from django import forms

# List of US states for dropdown
US_STATES = [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
    ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'),
    ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
    ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
    ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
    ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
    ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
    ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
    ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
]

# Vehicle type choices
DESCRIPTION_CHOICES = [
    ('SEMI TRUCK', 'SEMI TRUCK'),
    ('STRAIGHT TRUCK', 'STRAIGHT TRUCK'),
    ('TRUCK', 'TRUCK'),
    ('TRAILER', 'TRAILER'),
]

class CompanyInfoForm(forms.Form):
    company_name = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.ChoiceField(choices=US_STATES)
    zip = forms.CharField(max_length=10)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 px-3 py-2'
            })

class TrackInvoiceForm(forms.Form):
    description = forms.ChoiceField(choices=DESCRIPTION_CHOICES)
    make = forms.CharField(max_length=100)
    model = forms.CharField(max_length=100)
    VIN = forms.CharField(
        max_length=17,
        min_length=17,
        help_text='Must be exactly 17 characters',
        error_messages={
            'min_length': 'VIN must be exactly 17 characters.',
            'max_length': 'VIN must be exactly 17 characters.'
        }
    )
    year = forms.CharField(max_length=4)
    mileage = forms.IntegerField(min_value=0)
    total_sum = forms.DecimalField(max_digits=10, decimal_places=2)
    fee = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            widget.attrs.update({
                'class': 'w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-200 focus:ring-opacity-50 px-3 py-2'
            })
