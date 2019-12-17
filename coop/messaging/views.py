from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView

from coop.messaging.forms import MessagingForm
from coop.messaging.models import Message, MessageStatusChoice


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
        status = MessageStatusChoice.choices()[0][0]  # status = OPEN
        return Message.objects.filter(message_to=self.request.user.id, status=status)


class MessagesDelete(DeleteView):
    model = Message
    # success_url = reverse_lazy('messaging:msg_list')

    def get_success_url(self):
        return reverse_lazy('messaging:msg_list', args=(self.request.user.id,))

    def get_queryset(self):
        pk = self.kwargs.get(self.pk_url_kwarg)
        return Message.objects.filter(pk=pk)
