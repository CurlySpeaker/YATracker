from django import forms


class UpdateProjectForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea)
    description = forms.CharField(label="Description", widget=forms.Textarea)


class AddTaskForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.Textarea)
    info = forms.CharField(label="Info", widget=forms.Textarea)

