from django import forms
from django.forms import TextInput, NumberInput, URLInput, FileInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class CustomAuthForm(AuthenticationForm):
    """
    Login Form
    """
    username = forms.CharField(widget=TextInput(attrs={'name': 'username', 'class': 'form-control',
                                                       'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'name': 'password', 'class': 'form-control',
                                                           'type': 'password', 'placeholder': 'Password'}))


class SignUpForm(forms.Form):

    first_name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                        'type': 'text', 'id': 'f-name',
                                                                        'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                       'type': 'text', 'id': 'l_name',
                                                                       'placeholder': 'Enter Last Name'}))
    username = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'text', 'id': 'username',
                                                                      'placeholder': 'Enter Username'}))
    email = forms.EmailField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                    'type': 'email', 'id': 'email',
                                                                    'placeholder': 'Enter Email'}))
    phone = forms.CharField(required=True, widget=NumberInput(attrs={'class': 'form-control',
                                                                    'type': 'number', 'id': 'phone',
                                                                    'placeholder': 'Enter Phone Number'}))

    facebook = forms.CharField(required=False, widget=URLInput(attrs={'class': 'form-control',
                                                                     'type': 'url', 'id': 'facebook',
                                                                     'placeholder': 'Enter your Facebook URL'}))
    instagram = forms.CharField(required=False, widget=URLInput(attrs={'class': 'form-control',
                                                                      'type': 'url', 'id': 'instagram',
                                                                      'placeholder': 'Enter your Instagram URL'}))

    address = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                    'type': 'text', 'id': 'address',
                                                                    'placeholder': 'Enter Address'}))
    password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                     'type': 'password', 'id': 'password',
                                                                     'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                              'type': 'password',
                                                                              'id': 'confirm_password',
                                                                              'placeholder': 'Enter Password Again'}))
    track = forms.FileField(required=True, widget=FileInput(attrs={'class': 'form-control',
                                               'type': 'file',
                                               'id': 'track',
                                               'placeholder': ''}))

    avatar = forms.ImageField(required=True, widget=FileInput(attrs={'class': 'form-control',
                                                                   'type': 'file',
                                                                   'id': 'track',
                                                                   'placeholder': ''}))

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password = cleaned_data.get('password')
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        confirm_password = cleaned_data.get('confirm_password')
        file = cleaned_data.get('track', False)
        errors = []


        try:
            User.objects.get(username=username)
            username_error = ({"username": 'This username is already taken'})
            errors.append(username_error)
        except User.DoesNotExist:
            pass

        try:
            User.objects.get(email=email)
            email_error = ({"email": 'A user already exist with this email'})
            errors.append(email_error)
        except User.DoesNotExist:
            pass

        # if file.size > 7340032:
        #     raise forms.ValidationError({"Track": 'Audio file too large. Upload file less than 7MB'})
        #
        # if file.content_type not in ["audio/mpeg", "audio/mp4", "audio/ogg", 'audio/mp3', 'audio/basic', 'audio/mid',
        #                              'audio/ogg']:
        #     raise forms.ValidationError({"Track": 'Audio file not understood'})

        if password != confirm_password:
            password_error = ({
                'password': 'The two password didn\'t match'
            })
            errors.append(password_error)

        if len(errors) > 0:
            raise forms.ValidationError(errors)
        
        return cleaned_data

