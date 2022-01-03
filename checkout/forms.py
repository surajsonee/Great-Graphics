from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    """
    Customer Order Form
    """
    class Meta:
        """Meta data"""
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    # overwrite init
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # super is default init
        super().__init__(*args, **kwargs)
        # placeholders dictionary
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        # cursor will start in the full name field
        # when the user loads the page.
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    # adding a star to the placeholder if
                    # it's a required field on the model.
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # css class - stripe-style-input
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # remove form field labels
            self.fields[field].label = False
