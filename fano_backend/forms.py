from django import forms
from .models import Songs, Member, Blog, VideoGallery
from ckeditor.fields import RichTextFormField


class NewSongForm(forms.ModelForm):

    class Meta:
        model = Songs
        fields = ['cover_art', 'music', 'title']
        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Song Title',
                                            'required': 'true'}),
            'cover_art': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),
            'music': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),
        }

    # def clean(self):
    #     cleaned_data = super(NewSongForm, self).clean()
    #     file = cleaned_data.get('music', False)
    #
    #     if not file.content_type in ["audio/mpeg", "audio/mp4", "audio/ogg", 'audio/mp3']:
    #         raise forms.ValidationError('Audio file not understood')
    #
    #     return cleaned_data


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = ['facebook', 'instagram', 'address', 'phone', 'about_me', 'profession', 'avatar']
        widgets = {
            'facebook': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                               'placeholder': 'EG: https://www.facebook.com/ideathinkers'}),
            'instagram': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                                'placeholder': 'EG: https://www.instagram.com/ideathinkers'}),
            'address': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                              'placeholder': 'Enter Address', }),
            'phone': forms.TextInput(attrs={'type': 'number', 'class': 'form-control',
                                            'placeholder': 'Enter Phone Number', 'required': 'true'}),
            'about_me': forms.Textarea(attrs={'type': 'text', 'class': 'form-control',
                                              'placeholder': 'Tell us about yourself in 300 Words or less', }),
            'profession': forms.TextInput(attrs={'type': 'text', 'class': 'form-control',
                                                 'placeholder': 'Enter Profession', }),
            'avatar': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),
        }


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = ['title', 'context', 'image', 'music']

        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter Blog Title'}),
            'context': RichTextFormField(),
            'image': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),
            'music': forms.ClearableFileInput(attrs={'type': 'file', 'class': 'form-control'}),

        }
    
    # def clean(self):
    #     cleaned_data = super(BlogForm, self).clean()
    #     file = cleaned_data.get('music', False)
    #
    #     if not file.content_type in ["audio/mpeg", "audio/mp4", "audio/ogg", 'audio/mp3']:
    #         raise forms.ValidationError('Audio file not understood')
    #
    #     return cleaned_data


class VideoForm(forms.ModelForm):

    class Meta:
        model = VideoGallery
        fields = ['title', 'link']

        widgets = {
            'title': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter Title'}),
            'link': forms.TextInput(attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Enter ID'}),
        }
