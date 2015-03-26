from django import forms

class PersonalDataForm(forms.Form):
    FirstName = forms.CharField(label='Vorname')
    LastName = forms.CharField(label='Nachname')

class AddressForm(forms.Form):
    Name = forms.CharField(label='Name')
    Street = forms.CharField(label='Straße')
    City = forms.CharField(label='PLZ / Stadt')

