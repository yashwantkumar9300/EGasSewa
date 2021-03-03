
from django import forms
from app.models import DealerRgistration,DealerAddress,District

class DealerForms(forms.ModelForm):
    genders = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    gender = forms.ChoiceField(choices=genders)
    class Meta:
        model = DealerRgistration
        fields = "__all__"
        widgets = {"dob":forms.SelectDateWidget}

class DealerAddressForm(forms.ModelForm):
    class Meta:
        model = DealerAddress
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address_dict'].queryset = District.objects.none()

        if 'address_state' in self.data:
            try:
                country_id = int(self.data.get('address_state'))
                self.fields['address_dict'].queryset = District.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['address_dict'].queryset = self.instance.country.city_set.order_by('name')