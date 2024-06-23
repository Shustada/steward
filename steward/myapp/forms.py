from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Feedback, Recognition, Grievance, Organization, WorkAddress
import requests

class OrganizationSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class WorkerSignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    organization_name = forms.CharField()
    address = forms.CharField()

    class Meta:
        model = Profile
        fields = ['organization_name', 'address']

    def clean_address(self):
        address = self.cleaned_data.get('address')
        organization_name = self.cleaned_data.get('organization_name')

        # Validate the address using the Google Places API
        validated_address, latitude, longitude = self.validate_address(address)

        if not validated_address:
            raise forms.ValidationError("Invalid address.")

        # Get or create the organization
        organization, created = Organization.objects.get_or_create(name=organization_name)

        # Check if the address already exists
        work_address, created = WorkAddress.objects.get_or_create(
            address=validated_address,
            organization=organization,
            defaults={'latitude': latitude, 'longitude': longitude}
        )

        return work_address

    def validate_address(self, address):
        api_key = 'AIzaSyA_SxDKGSuYaTRIeGfu6d0D3wfq1pKF7as'
        response = requests.get(
            f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json',
            params={
                'input': address,
                'inputtype': 'textquery',
                'fields': 'formatted_address,geometry',
                'key': api_key
            }
        )
        response_data = response.json()

        if not response_data.get('candidates'):
            return None, None, None

        result = response_data['candidates'][0]
        validated_address = result['formatted_address']
        latitude = result['geometry']['location']['lat']
        longitude = result['geometry']['location']['lng']

        return validated_address, latitude, longitude

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['content', 'private']

class RecognitionForm(forms.ModelForm):
    class Meta:
        model = Recognition
        fields = ['content', 'private']

class GrievanceForm(forms.ModelForm):
    class Meta:
        model = Grievance
        fields = ['content', 'private']
