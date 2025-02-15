from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Task, Person, StatusModel, Pc, TaskSection


class LoginUserForm(AuthenticationForm):
    # email = forms.CharField(label='Емайл', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
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
        self.fields["section"] = forms.ModelChoiceField(label="Категория задач",
                                                        queryset=TaskSection.objects.all())
        if "instance" in kwargs and kwargs["instance"].creator:
            self.fields["creator"].disabled = True

    class Meta:
        model = Task
        fields = ["title", "note", "is_visible", "creator", "executor", "section"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "note": forms.Textarea(attrs={"cols": 60, "rows": 10}),

        }


class EditTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"] = forms.ModelChoiceField(label="Назначен",
                                                         queryset=Person.objects.filter(is_executer=True))
        self.fields["creator"] = forms.ModelChoiceField(label="Создан", queryset=Person.objects.all())
        self.fields["section"] = forms.ModelChoiceField(label="Категория задач",
                                                        queryset=TaskSection.objects.all())
        if "instance" in kwargs and kwargs["instance"].creator:
            self.fields["creator"].disabled = True

    class Meta:
        model = Task
        fields = ["title", "note", "is_visible", "status", "creator", "executor", "section"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "note": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }


class TaskListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["executor"] = forms.ModelChoiceField(label="Назначена", required=False,
                                                         queryset=Person.objects.filter(is_executer=True))
        self.fields["creator"] = forms.ModelChoiceField(label="Создана", required=False,
                                                        queryset=Person.objects.all())
        self.fields["status"] = forms.ModelChoiceField(label="Статус", required=False,
                                                       queryset=StatusModel.objects.all(),
                                                       )
        self.fields["section"] = forms.ModelChoiceField(label="Категория задач", required=False,
                                                       queryset=TaskSection.objects.all(),
                                                       )

    class Meta:
        model = Task
        fields = ["creator", "executor", "status", "section"]


class PcListForm(forms.Form):
    sort_form = forms.TypedChoiceField(label="Сортировать по", required=False,
                                       choices=[('title', 'По названию'),
                                                ('telefon_number', 'По номеру телефона'),
                                                ('ip', 'По ip'),
                                                ('rdb_user', 'По RDB логину'),
                                                ('email', 'По email')])
