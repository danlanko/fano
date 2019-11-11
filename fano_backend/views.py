from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .models import Member, Songs, Blog, VideoGallery
from .forms import NewSongForm, UpdateProfileForm, BlogForm, VideoForm
from django.db import transaction
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.


def login_redirect(request):
    return redirect('member_profile', request.user.member.id, request.user.id)


class MemberList(LoginRequiredMixin, generic.ListView):
    raise_exception = True
    model = Member
    queryset = Member.objects.all().order_by('-id').exclude(user__is_superuser=True, is_admin=True)


class MemberProfile(LoginRequiredMixin, generic.DetailView):
    raise_exception = True
    model = Member
    pk_url_kwarg = 'member_id'
    template_name = 'fano_backend/urser_profile.html'

    def get_context_data(self, **kwargs):
        context = super(MemberProfile, self).get_context_data(**kwargs)
        context['user_songs'] = Songs.objects.filter(owner=self.kwargs['user_id']).order_by('-id')
        return context


class UpdateProfile(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'fano_backend/update_profile.html'
    raise_exception = True,
    model = Member
    form_class = UpdateProfileForm
    pk_url_kwarg = 'member_id'

    def test_func(self):
        return int(self.kwargs['user_id']) == int(self.request.user.id)

    def get_success_url(self):

        return reverse('member_profile', kwargs={'member_id': self.kwargs['member_id'], 'user_id': self.kwargs['user_id']})

    def form_valid(self, form):
        messages.success(self.request, 'Update successful')
        return super(UpdateProfile, self).form_valid(form)


def user_has_access(user):
    return Member.objects.get(user=user).is_admin


@user_passes_test(user_has_access)
def deactivate_member(request, user_id):
    member = User.objects.get(id=user_id)
    member.is_active = False
    member.save()
    messages.success(request, 'You have deactivated a member account')
    return redirect('member_list')


@user_passes_test(user_has_access)
def activate_member(request, user_id):
    member = User.objects.get(id=user_id)
    member.is_active = True
    member.save()

    message = render_to_string('emails/emails.html', {
        'type': 'activate_account',
        'name': member.last_name + ' ' + member.first_name,
    })
    mail_subject = 'FANO Account Activated'
    to_email = member.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()

    messages.success(request, 'You have activated a member account')
    return redirect('member_list')


@user_passes_test(user_has_access)
def delete_member(request, user_id):
    user = User.objects.get(id=user_id)
    member = Member.objects.get(user_id=user_id)
    member.delete()
    user.delete()
    messages.success(request, 'You have deleted a member account')
    return redirect('member_list')


class NewSong(LoginRequiredMixin, generic.CreateView):
    raise_exception = True
    model = Songs
    template_name = 'fano_backend/new_song.html'
    form_class = NewSongForm
    success_url = reverse_lazy('new_song')

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.owner = self.request.user
            form.save()

            messages.success(self.request, 'New song added to successfully')
        return super(NewSong, self).form_valid(form)


class SongList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    raise_exception = True
    model = Songs
    template_name = 'fano_backend/song_list.html'
    success_url = reverse_lazy('new_song')

    def get_queryset(self):
        queryset = Songs.objects.filter(owner=self.request.user)
        return queryset

    def test_func(self):

        if Member.objects.get(user=self.request.user).is_admin:
            return True

        try:
            if Songs.objects.filter(owner=self.request.user).exists():
                for item in Songs.objects.filter(owner=self.request.user):
                    if item.owner == self.request.user:
                        return True
                return True

            else:
                return True

        except Songs.DoesNotExist:
            return True


class UpdateSongs(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    raise_exception = True
    model = Songs
    template_name = 'fano_backend/new_song.html'
    success_url = reverse_lazy('song_list')
    pk_url_kwarg = 'song_id'
    form_class = NewSongForm

    def test_func(self):
        members = Member.objects.get(user=self.request.user)
        for item in Songs.objects.filter(owner=self.request.user):
            if item.owner == self.request.user:
                return True
        if members.is_admin:
            return True

    def form_valid(self, form):
        messages.success(self.request, 'Update was successful')
        return super(UpdateSongs, self).form_valid(form)


def delete_song(request, song_id):
    query = Songs.objects.get(id=song_id)
    query.delete()
    messages.success(request, 'Item was deleted successfully')
    return redirect('song_list')


class BlogView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Blog
    raise_exception = True
    template_name = 'fano_backend/new_blog.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'New blog post added successfully')
        return super(BlogView, self).form_valid(form)

    def test_func(self):
        return Member.objects.get(user=self.request.user).is_admin


class BlogList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Blog
    raise_exception = True
    template_name = 'fano_backend/blog_list.html'

    def get_queryset(self):
        query = Blog.objects.all().order_by('-id')
        return query

    def test_func(self):
        return Member.objects.get(user=self.request.user).is_admin


class BlogUpdate(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Blog
    raise_exception = True
    template_name = 'fano_backend/new_blog.html'
    slug_url_kwarg = 'slug'
    form_class = BlogForm
    success_url = reverse_lazy('blog_list')

    def form_valid(self, form):
        form.instance.edited_by = self.request.user
        messages.success(self.request, 'Blog post has been updated successfully')
        return super(BlogUpdate, self).form_valid(form)

    def test_func(self):
        return Member.objects.get(user=self.request.user).is_admin


@user_passes_test(user_has_access)
def delete_blog(request, blog_id):
    query = Blog.objects.get(id=blog_id)
    query.delete()
    messages.success(request, 'Item was deleted successfully')
    return redirect('blog_list')


class EmbedVideo(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = VideoGallery
    raise_exception = True
    template_name = 'fano_backend/embed_video.html'
    form_class = VideoForm
    success_url = reverse_lazy('embed_video')

    def form_valid(self, form):
        messages.success(self.request, 'Video embedded successfully')
        return super(EmbedVideo, self).form_valid(form)

    def test_func(self):
        return Member.objects.get(user=self.request.user).is_admin


class VideoList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = VideoGallery
    raise_exception = True
    template_name = 'fano_backend/video_list.html'

    def test_func(self):
        return Member.objects.get(user=self.request.user).is_admin


@user_passes_test(user_has_access)
def delete_video(request, video_id):
    query = VideoGallery.objects.get(id=video_id)
    query.delete()
    messages.success(request, 'Item was deleted successfully')
    return redirect('video_list')


def proceed_payment(request, user_id):
    user = User.objects.get(id=user_id)
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    message = render_to_string('emails/emails.html', {
        'type': 'sign_up_form',
        'name': first_name + ' ' + last_name,
    })
    mail_subject = 'Welcome to Fano'
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = 'html'
    send_email.send()
    messages.success(request, 'Payment Instruction has been sent to member')

    return redirect('member_list')

