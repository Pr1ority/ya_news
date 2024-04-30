import pytest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.urls import reverse

from pytest_django.asserts import assertRedirects


User = get_user_model()


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', ('id_for_args',)),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    ),
)
def test_pages_availability(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK)
    ),
)
@pytest.mark.parametrize(
    'name',
    ('news:edit', 'news:delete'),
)
def test_availability_for_comment_edit_and_delete(parametrized_client, name,
                                                  expected_status, comment):
    url = reverse(name, args=(comment.id,))
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name',
    (
        ('news:delete'),
        ('news:edit'),
    ),
)
def test_redirect_for_anonymous_client(name, client, comment):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.id,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
