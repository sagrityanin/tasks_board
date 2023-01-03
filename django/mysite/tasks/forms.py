from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from .models import Task, Person


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        current_user = kwargs.get("current_user")
        super().__init__(*args)
        self.fields["executor"] = forms.ModelChoiceField(label="Назначен",
                                                         queryset=Person.objects.filter(is_executer=True))
        self.fields["creator"] = forms.ModelChoiceField(label="Задача создана",
                                                        initial=Person.objects.get(user=current_user),
                                                        queryset=Person.objects.filter(user=current_user))
        if "instance" in kwargs and kwargs["instance"].creator:
            self.fields["creator"].disabled = True

    class Meta:
        model = Task
        fields = ["title", "note", "is_visible", "creator", "executor"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "note": forms.Textarea(attrs={"cols": 60, "rows": 10}),

        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return title


class EditTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"] = forms.ModelChoiceField(label="Назначен",
                                                         queryset=Person.objects.filter(is_executer=True))
        self.fields["creator"] = forms.ModelChoiceField(label="Создан", queryset=Person.objects.all())
        if "instance" in kwargs and kwargs["instance"].creator:
            self.fields["creator"].disabled = True

    class Meta:
        model = Task
        fields = ["title", "note", "is_visible", "status", "creator", "executor"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "note": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return title
