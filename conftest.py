import copy
import logging
import os
from os.path import join, dirname
import requests
import json
import pytest
from dotenv import load_dotenv

logger = None
pytest_id = []
pytest_status = []
pytest_id_value = None
AUTH_TOKEN = None
PREFIX_TICKET_VALUE = None
JIRA_DOMAIN = None
PASS_STATUS_TRANSITION = None
FAIL_STATUS_TRANSITION = None


def set_up_logging(config):
    global logger

    try:
        level = config.getoption('log-level'),
    except ValueError as e:
        level = logging.DEBUG

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)


def pytest_configure(config):
    set_up_logging(config)


def pytest_collection_modifyitems(session, config, items):
    """
    This hook is called after all tests have been collected.
    We can modify that list.
    """
    global pytest_id, pytest_id_value

    for pytest_test in copy.copy(items):
        if hasattr(pytest_test, 'callspec') and 'ticket_id' in pytest_test.callspec.params:
            pytest_id.append(str(pytest_test.callspec.params['ticket_id']))

    pytest_id_value = get_pytest_id(len(pytest_id))
    get_env_values()


def get_env_values():
    global AUTH_TOKEN, PREFIX_TICKET_VALUE, JIRA_DOMAIN, PASS_STATUS_TRANSITION, FAIL_STATUS_TRANSITION

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
    PREFIX_TICKET_VALUE = os.environ.get("PREFIX_TICKET_VALUE")
    JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN")
    PASS_STATUS_TRANSITION = os.environ.get("PASS_STATUS_TRANSITION")
    FAIL_STATUS_TRANSITION = os.environ.get("FAIL_STATUS_TRANSITION")


def setup_module(module):
    print("\n")
    logger.info("Running setup for MODULE [%s]" % module.__name__)


def teardown_module(module):
    print("\n")
    logger.info("Running teardown for MODULE [%s]" % module.__name__)


def get_pytest_id(length):
    for i in range(length):
        yield pytest_id[i]


@pytest.mark.hookwrapper(tryfirst=True)
def pytest_runtest_makereport(item):
    """
    This is called as each test ends
    """
    outcome = yield
    result = outcome.get_result()

    log_file = "test_results.log"
    if result.when == "call":
        try:
            with open(log_file, "a") as f:
                f.write(result.nodeid + "   " + result.outcome + "   " + str(result.duration)+"\n")
            ticket_id = next(pytest_id_value)
            if ticket_id in result.nodeid:
                send_results_to_jira(result, ticket_id)
            elif ticket_id not in result.nodeid:
                ticket_id = f"{PREFIX_TICKET_VALUE}"+(result.nodeid.replace("_", "-")).split(f"{PREFIX_TICKET_VALUE}")[1][:-1]
                send_results_to_jira(result, ticket_id)
        except Exception as e:
            print("Error", e)
            pass


def send_results_to_jira(result, ticket_id):
    # If testcase status is skipped, then it belongs to XFail condition, which got failed
    testcase = {"passed": "Passed", "failed": "Failed", "skipped": "Xfailed"}
    jira_api_endpoint = ".atlassian.net/rest/api/2/issue"

    testcase_comment = f"{ticket_id} - Testcase is " + str(testcase[result.outcome])
    comment_url = f"https://{JIRA_DOMAIN}{jira_api_endpoint}/{ticket_id}/comment"

    payload = json.dumps({"body": testcase_comment})
    headers = {
        'Authorization': F'Basic {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Below post call is used to add the comment on JIRA tickets
    # URL : https://testautomatejira..atlassian.net/rest/api/2/issue/{ticket_id}/comment"
    requests.request("POST", comment_url, headers=headers, data=payload)

    # Below post call is to make transition for the JIRA tickets
    # URL : https://testautomatejira..atlassian.net/rest/api/2/issue/{ticket_id}/transitions"
    transition_url = f"https://{JIRA_DOMAIN}{jira_api_endpoint}/{ticket_id}/transitions"
    apply_transition_to_jira_tickets(transition_url, headers=headers, status=result.outcome)


def apply_transition_to_jira_tickets(transition_url, headers, status):
    method = "POST"
    if status == "passed":
        transition_payload_failed = json.dumps({"transition": {"id": f"{PASS_STATUS_TRANSITION}"}})
        requests.request(method, transition_url, headers=headers, data=transition_payload_failed)
    elif status in ["failed", "skipped"]:
        transition_payload_failed = json.dumps({"transition": {"id": f"{FAIL_STATUS_TRANSITION}"}})
        requests.request(method, transition_url, headers=headers, data=transition_payload_failed)
