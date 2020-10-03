import os
import pytest
from unittest.mock import MagicMock
from heroku.heroku import Heroku

class TestHerokuClient:

    def test_api_key_is_taken_from_environment_variable(self):
        os.environ['HEROKU_API_KEY'] = '123-123-123'
        heroku = Heroku()
        assert heroku.api_key == '123-123-123'

    def test_api_key_can_be_explicitly_set(self):
        heroku = Heroku(api_key='ABC-ABC')
        assert heroku.api_key == 'ABC-ABC'

    def test_default_headers_are_set(self):
        os.environ['HEROKU_API_KEY'] = '999-999-999'
        heroku = Heroku()
        expected = {
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer 999-999-999',
            'Content-Type': 'application/json'
        }
        assert set(expected.items()).issubset(
            set(heroku.session.headers.items())
        )

    def test_default_headers_are_set_with_passed_API_key(self):
        heroku = Heroku(api_key='ABC-ABC-ABC')
        expected = {
            'Accept': 'application/vnd.heroku+json; version=3',
            'Authorization': 'Bearer ABC-ABC-ABC',
            'Content-Type': 'application/json'
        }
        assert set(expected.items()).issubset(
            set(heroku.session.headers.items())
        )

    def test_calling_the_get_method_calls_requests_get_method(self):
        heroku = Heroku()
        heroku.session.get = MagicMock(return_value={})
        heroku.get('endpoint/foo', params={})

        heroku.session.get.assert_called_with('endpoint/foo',  params={})

    def test_calling_the_post_method_calls_requests_post_method(self):
        heroku = Heroku()
        heroku.session.post = MagicMock(return_value={})
        heroku.post('endpoint/foo', data={})

        heroku.session.post.assert_called_with('endpoint/foo', data={})

    def test_calling_the_patch_method_calls_requests_patch_method(self):
        heroku = Heroku()
        heroku.session.patch = MagicMock(return_value={})
        heroku.patch('endpoint/foo', data={})

        heroku.session.patch.assert_called_with('endpoint/foo', data={})

    def test_calling_the_put_method_calls_requests_put_method(self):
        heroku = Heroku()
        heroku.session.put = MagicMock(return_value={})
        heroku.put('endpoint/foo', data={})

        heroku.session.put.assert_called_with('endpoint/foo', data={})

    def test_calling_the_delete_method_calls_requests_delete_method(self):
        heroku = Heroku()
        heroku.session.delete = MagicMock(return_value={})
        heroku.delete('endpoint/foo')

        heroku.session.delete.assert_called_with('endpoint/foo')
