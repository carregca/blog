from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    # Honeypot: los humanos no ven este campo, los bots suelen completarlo.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={
        "tabindex": "-1",
        "autocomplete": "off",
    }))

    class Meta:
        model = Comment
        fields = ["name", "body"]
        labels = {"name": "Nombre", "body": "Comentario"}
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Cómo te llamás", "maxlength": 60}),
            "body": forms.Textarea(attrs={
                "placeholder": "Escribí tu comentario…",
                "rows": 5,
                "maxlength": 1000,
            }),
        }

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detectado.")
        return ""
