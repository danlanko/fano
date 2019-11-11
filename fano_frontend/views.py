from django.views import generic
from .forms import SignUpForm
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from fano_backend.models import Member
from .forms import CustomAuthForm
from django.core.exceptions import ValidationError
from fano_backend.models import FanoArtist, Gallery, VideoGallery, Blog, Events, GalleryCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from fano_backend.models import Songs
import requests

# Create your views here.


class Homepage(generic.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['fano_artist'] = FanoArtist.objects.all()
        context['gallery'] = Gallery.objects.all()
        context['blog'] = Blog.objects.all().order_by('-id')[:3]
        context['video'] = VideoGallery.objects.all()
        context['event'] = Events.objects.all()
        context['gallery_cat'] = GalleryCategory.objects.all()
        return context


def contact_form(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    message = request.POST['message']

    recaptcha_response = request.POST.get('g-recaptcha-response')

    data = {
        'secret': '6LcasrYUAAAAALXobzE4ZWx_w1qh0AQ5uPpSC7Qp',
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    ''' End reCAPTCHA validation '''

    if result['success']:
        messages.success(request, 'Thank you %s, you message has been received' % name)
        message = render_to_string('emails/emails.html', {
            'type': 'contact_form',
            'name': name,
            'phone': phone,
            'email': email,
            'message': message,
        })
        mail_subject = 'New Contact Form from Fano Website'
        to_email = 'info@fano.ng'
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = 'html'
        send_email.send()
    else:
        messages.error(request, 'Invalid reCAPTCHA. Please try again.')

    return redirect('homepage')


class Login(generic.FormView):
    template_name = 'registration/login.html'
    form_class = CustomAuthForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = authenticate(username=username, password=password)
            login(self.request, user)
        except:
            raise ValidationError('Error, Login Credentials Incorrect')

        return super(Login, self).form_valid(form)


class SignUp(generic.FormView):
    form_class = SignUpForm
    success_url = reverse_lazy('sign_up')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        with transaction.atomic():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            facebook = form.cleaned_data['facebook']
            instagram = form.cleaned_data['instagram']
            address = form.cleaned_data['address']
            track = self.request.FILES['track']
            avatar = self.request.FILES['avatar']
            password = form.cleaned_data['password']

            new_user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password,
                is_active=False
            )

            new_member = Member.objects.create(
                user_id=new_user.id,
                phone=phone,
                facebook=facebook,
                instagram=instagram,
                address=address,
                track=track,
                avatar=avatar
            )
            new_member.save()

            messages.success(self.request, 'You registration has been submitted. We will review and get back to you')
        return super(SignUp, self).form_valid(form)


class BlogDetail(generic.DetailView):
    model = Blog
    template_name = 'single_blog.html'
    slug_url_kwarg = 'blog_slug'


class Artist(generic.ListView):
    model = Member
    template_name = 'artist_list.html'
    queryset = Member.objects.filter(user__is_active=True, user__is_staff=False, is_admin=False)


class ArtistDetail(generic.DetailView):
    model = Member
    template_name = 'artist_detail.html'
    pk_url_kwarg = 'member_id'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetail, self).get_context_data(**kwargs)
        context['artist_song'] = Songs.objects.filter(owner=self.object.user_id)
        return context
