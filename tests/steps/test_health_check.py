from pytest_bdd import given, scenario, then, when


@scenario(
    "testing/features/health_check.feature",
    "Application responds to health check",
)
def test_health_check():
    pass


@given("the application is running")
def app_running():
    pass


@when("I request the admin login page", target_fixture="response")
def request_admin(client):
    return client.get("/admin/login/")


@then("I receive a successful response")
def check_response(response):
    assert response.status_code == 200
