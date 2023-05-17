from unittest.mock import AsyncMock, MagicMock
from urllib.parse import urlencode
from bovine.clients import lookup_account_with_webfinger


from behave import given, when, then
from behave.api.async_step import async_run_until_complete


@given("Webfinger response")
def load_webfinger_response(context):
    context.response = context.text
    context.response_status_code = 200


@given("Webfinger response with {status_code:d}")
def load_webfinger_response_with_status(context, status_code):
    context.response = ""
    context.response_status_code = status_code


@when('Looking up "{account}"')
@async_run_until_complete
async def test_lookup(context, account):
    session = MagicMock()
    response_mock = AsyncMock()
    session.get.return_value = response_mock
    response_mock.__aenter__.return_value = response_mock

    response_mock.text.return_value = context.response
    response_mock.status = context.response_status_code

    # FIXME !!! bovine doesn't do what we need yet.
    account = account.removeprefix("acct:")

    context.result = await lookup_account_with_webfinger(session, account)

    session.get.assert_called_once()

    args = session.get.call_args

    context.request_url = args.args[0] + "?" + urlencode(args.kwargs["params"])


@then('Lookup at "{url}"')
def verify_lookup_url(context, url):
    assert context.request_url == url


@then('ActivityPub Object Id is "{id}"')
def verify_resulting_id(context, id):
    assert context.result == id


@then("None is returned")
def verify_result_is_none(context):
    assert context.result is None
