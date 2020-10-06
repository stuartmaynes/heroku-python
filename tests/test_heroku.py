import os
import pytest
from requests import Response
from heroku.heroku import Heroku

@pytest.fixture()
def heroku_mock(mocker):
    # Given
    heroku = Heroku()
    mocker.patch.object(heroku, 'request')
    return heroku

@pytest.fixture()
def heroku_session_mock(mocker):
    # Given
    heroku = Heroku()
    mocker.patch.object(heroku.session, 'request')
    return heroku


class MockResponse():

    status_code = 200

    def json(self):
        return []


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

    def test_calling_the_get_method_calls_requests_method(self, heroku_mock):
        #  When
        heroku_mock.get('endpoint/foo', params={})
        # Then
        heroku_mock.request.assert_called_with('GET', 'endpoint/foo',  params={})

    def test_calling_the_post_method_calls_requests_method(self, heroku_mock):
        #  When
        heroku_mock.post('endpoint/foo', data={})
        # Then
        heroku_mock.request.assert_called_with('POST', 'endpoint/foo', data={})

    def test_calling_the_patch_method_calls_requests_method(self, heroku_mock):
        #  When
        heroku_mock.patch('endpoint/foo', data={})
        # Then
        heroku_mock.request.assert_called_with('PATCH', 'endpoint/foo', data={})

    def test_calling_the_put_method_calls_requests_method(self, heroku_mock):
        #  When
        heroku_mock.put('endpoint/foo', data={})
        # Then
        heroku_mock.request.assert_called_with('PUT', 'endpoint/foo', data={})

    def test_calling_the_delete_method_calls_requests_method(self, heroku_mock):
        #  When
        heroku_mock.delete('endpoint/foo')
        # Then
        heroku_mock.request.assert_called_with('DELETE', 'endpoint/foo')

    def test_return_value_the_http_verb_method(self, heroku_session_mock):
        heroku_session_mock.get('endpoint/foo', params={})
        heroku_session_mock.session.request.assert_called_with(
            'GET', 'endpoint/foo', params={}
        )

        heroku_session_mock.post('endpoint/foo', data={})
        heroku_session_mock.session.request.assert_called_with(
            'POST', 'endpoint/foo', data={}
        )

        heroku_session_mock.patch('endpoint/foo', params={})
        heroku_session_mock.session.request.assert_called_with(
            'PATCH', 'endpoint/foo', params={}
        )

        heroku_session_mock.put('endpoint/foo', data={})
        heroku_session_mock.session.request.assert_called_with(
            'PUT', 'endpoint/foo', data={}
        )

        heroku_session_mock.delete('endpoint/foo')
        heroku_session_mock.session.request.assert_called_with(
            'DELETE', 'endpoint/foo'
        )

    def test_json_method_is_called_on_returned_response(self, mocker):
        mock_response = MockResponse()
        mocker.patch.object(mock_response, 'json', lambda: [{'key': 'value'}])

        heroku = Heroku()
        mocker.patch.object(heroku.session, 'request', lambda x, y: mock_response)

        assert heroku.get('endpoint/foo') == [{'key': 'value'}]
