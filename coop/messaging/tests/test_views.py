import pytest

from coop.accounts.models import User
from coop.messaging.models import MessageTaskChoice
from coop.messaging.forms import MessagingForm

from django import urls


@pytest.mark.django_db
def test_task_list(client, authenticated_user):
    url = urls.reverse('messaging:msg_list', args=(authenticated_user.id,))
    resp = client.get(url)
    assert resp.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'task, note, validity',
    [(MessageTaskChoice.choices()[0], "Coop Test Form Creation", True),
     ])
def test_message_form(client, authenticated_user, task, note, validity):
    user = User.objects.get(email=authenticated_user)
    form = MessagingForm(data={'task': task[0], 'note': note})
    f = form.save(commit=False)
    assert form.is_valid() is validity
    f.message_from_id = user.pk
    f.message_to_id = user.pk
    f.save()
    url = urls.reverse('messaging:msg_list', args=(user.pk,))
    resp = client.get(url)
    assert b'Coop Test Form Creation' in resp.content
