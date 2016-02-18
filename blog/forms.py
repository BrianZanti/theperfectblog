from django import forms


class UserForm(forms.Form):
    username = forms.CharField(max_length=20, label="Username")
    password = forms.CharField(max_length=100, widget = forms.PasswordInput, label="Password")
    retypepassword = forms.CharField(max_length=100, widget = forms.PasswordInput, label="Retype Password")

class BlogForm(forms.Form):
    title = forms.CharField(max_length=160)
    body = forms.CharField(max_length=1000, widget=forms.Textarea)

class CommentForm(forms.Form):
    body = forms.CharField(max_length=160, widget=forms.Textarea)
