from django import forms


class UpdateProjectForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea)
    description = forms.CharField(label="Description", widget=forms.Textarea)


class AddTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea)
    info = forms.CharField(label="Info", widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        info = cleaned_data.get('info')

        if len(title) > 128 and len(info) > 256:
            self.add_error(
                None,
                "Too long text fields"
            )

        return cleaned_data

