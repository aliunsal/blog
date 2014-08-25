from django import forms


class UserRegister(forms.Form):
    user_name = forms.CharField(max_length=100, error_messages="")
    email = forms.EmailField(error_messages="")
    password = forms.PasswordInput()


class UserProfile(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    avatar = forms.ImageField()
    email = forms.EmailField()


class UserPost(forms.Form):
    title = forms.CharField(max_length=250)
    content = forms.CharField(widget=forms.Textarea)
    picture = forms.ImageField()
