from django.shortcuts import render
from django.views.generic import ListView, CreateView

from coop.messaging.forms import MessagingForm
from coop.messaging.models import Message


class Messaging(CreateView):
    form_class = MessagingForm
    success_url = "/"
    template_name = 'messaging.html'

    def form_valid(self, form):
        request = self.request
        f = form.save(commit=False)
        f.request = form.cleaned_data.get('request')
        f.note = form.cleaned_data.get('note')
        f.message_from_id = request.user.id
        # TODO - determine 'to' depending on request_task
        f.message_to_id = 1
        f.save()
        return render(request, 'home.html', {'message': 'Request created.'})


class MessagesList(ListView):
    model = Message
    context_object_name = 'message_list'
    paginate_by = 10
    ordering = ['-created']

    def get_queryset(self):
        return Message.objects.filter(message_to=self.request.user.id)
