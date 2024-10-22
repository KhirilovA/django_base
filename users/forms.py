from django import forms

from users.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['birth_date', 'bio', 'timezone', 'country']


class AddFriendForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
