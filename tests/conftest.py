import pytest

try:
    from tests._private_vcr import scrub_request
    from tests._private_vcr import scrub_response as custom_scrub_response
except ImportError:

    def scrub_request(request):
        return request

    def custom_scrub_response(response):
        return response


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [
            "authorization",
            "host",
            "set-cookie",
        ],
        "before_record_request": scrub_request,
        "before_record_response": scrub_response,
    }


def scrub_response(response):
    response["headers"].pop("set-cookie", None)
    response["headers"].pop("date", None)
    response["headers"].pop("cookie", None)
    return custom_scrub_response(response)


def pytest_recording_configure(config, vcr):
    vcr.before_record_request = scrub_request
