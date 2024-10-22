from django.urls import path

from users.views import (
    ProfileEditView,
    FriendListView,
    FriendUpdateView,
    FriendsAddView,
)


urlpatterns = [
    path('edit_profile/', ProfileEditView.as_view(), name='edit_profile'),
    path('friends/', FriendListView.as_view(), name='friends_list'),
    path('friends/update/<int:pk>/', FriendUpdateView.as_view(), name='friend_update'),
    path('friends/add/', FriendsAddView.as_view(), name='friends_add'),
]