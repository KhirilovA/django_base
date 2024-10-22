from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db import models

from users.forms import  ProfileForm, AddFriendForm
from users.models import UserFriends

User = get_user_model()


class ProfileEditView(UpdateView):
    form_class = ProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('edit_profile')

    def get_object(self, queryset=None):
        return self.request.user.profile


class FriendListView(LoginRequiredMixin, ListView):
    model = UserFriends
    template_name = 'users/friends_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        user = self.request.user
        accepted_friends = UserFriends.objects.filter(
            (models.Q(user=user) | models.Q(friend=user)),
            status='accepted'
        )
        pending_requests = UserFriends.objects.filter(friend=user, status='pending')

        return {
            'accepted_friends': accepted_friends,
            'pending_requests': pending_requests
        }


class FriendUpdateView(LoginRequiredMixin, UpdateView):
    model = UserFriends
    fields = []
    template_name = 'users/friend_update.html'

    def post(self, request, *args, **kwargs):
        friend_request = get_object_or_404(UserFriends, pk=self.kwargs['pk'])
        action = request.POST.get('action')

        if action == 'accept':
            friend_request.accept()
        elif action == 'block':
            friend_request.block()

        return redirect('friends_list')


class FriendsAddView(LoginRequiredMixin, ListView):
    template_name = 'users/friends_add.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        created_friends = UserFriends.objects.filter(
            (models.Q(user=user) | models.Q(friend=user))
        )

        friend_ids = created_friends.values_list('friend', flat=True).distinct()

        user_ids = created_friends.values_list('user', flat=True).distinct()

        exclude_ids = list(friend_ids) + list(user_ids) + [user.id]
        queryset = User.objects.exclude(id__in=exclude_ids)

        return queryset

    def post(self, request, *args, **kwargs):
        form = AddFriendForm(request.POST)
        if form.is_valid():
            user_id_to_add = form.cleaned_data['user_id']
            friend = User.objects.get(id=user_id_to_add)
            UserFriends.objects.get_or_create(user=request.user, friend=friend)
            return redirect('friends_add')
        return redirect('friends_add')
