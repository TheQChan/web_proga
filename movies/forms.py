from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=30,
        help_text="Только русские буквы и пробелы",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "id_username"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "id": "id_email"}),
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "id_password1"}
        ),
        help_text="Пароль должен содержать минимум 8 символов.",
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "id": "id_password2"}
        ),
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.fullmatch(r"^[А-Яа-яЁё\s]+$", username):
            raise forms.ValidationError(
                "Имя пользователя должно содержать только русские буквы."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Пароли должны совпадать.")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
