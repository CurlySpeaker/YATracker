from django import forms


class PasswordChangeForm(forms.Form):

    old_password = forms.CharField(label="New Password", required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(label="New Password", required=True, widget=forms.PasswordInput)
    password_repeat = forms.CharField(label="Repeat Password", required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        password_repeat = cleaned_data.get('password_repeat')

        if new_password != password_repeat:
            self.add_error(
                'password_repeat',
                "Passwords don't match"
            )

        return cleaned_data
