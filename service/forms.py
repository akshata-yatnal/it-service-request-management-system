from django import forms
from .models import Ticket, Comment
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'title',
            'description',
            'category',
            'priority',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Allow assignment only to support staff
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)


# Create the Comment form

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content',]

# Make assignment possible
class TicketAssignmentForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            'assigned_to',
        ]

# Change ticket status
class TicketStatusForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['status',]

# Add or update ticket resolution
class TicketResolutionForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['resolution',]