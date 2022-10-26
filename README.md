# Test Automation

## Getting Started
* [Pytest](https://github.com/pytest-dev/pytest) testing framework
* [Requests](https://github.com/psf/requests) HTTP library for API automation
* [Selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py) Selenium library for UI automation
* [Html-report](https://github.com/prashanth-sams/pytest-html-reporter) Pytest-html-report for report generation  
* [Virtualenv](https://github.com/pypa/virtualenv) (optional) for creating isolated virtual environments


## Install Virtual Environment
```bash
# install virtualenv
$ sudo pip install virtualenv

# test your installation
$ virtualenv --version

# create a virtual env.
$ virtualenv <your_virtual_env_name>

# activate virtual env.
$ source <virtualenv_dir/bin/activate>
```
## Deactivate / Delete Virtual Environment
#### Note:
* Deactivate virtual env before proceeding to delete

```bash
# deactivate virtual env.
$ deactivate

# delete virtual env
$ sudo rm -rf <your_virtual_env_name>
```

## Setup

```bash
$ source <virtualenv_dir/bin/activate>

$ pip install -r requirements.txt
```


## Building Rest API Endpoints
    To build the REST API Endpoints. Go to lib folder
    
    1. Create API class with Endpoint definitions 
    2. Use params for passing form data, if needed
    3. Use params with json.dumps(payload_data), if needed

```python
    # ~/lib/api/rest/sample_api/sample_api.py
       
    class SampleAPI(object):
    
         def sample_get(self):
            """
            This method is to call the /sample_get/ endpoint
            :return: sample get response
            """
            response = self.get("sample_get/")
            return response    
```

## API Client Configuration
    To make client configurations, 

    1. Add service details in services.YAML
        - Add service name in accepted services
        - Configure all service details like below format 
```Yaml
accepted_services:
  - 'sample_service'
services:
  sample_service:
    service_name: 'sample_service'
    api:
      scheme: 'https'
      port: ''
      base_path: '/'                   # ex: https://reqres.in/
      content_type: 'application/json'
      accept: 'application/json'
      hostname: 'reqres.in'
```
    2. Go to REST folder for API in lib
        - Create client config using RESTClient class
        - Import SampleAPI class and add it with config
        - Read services.YAML using ServiceConfig
        - Config details, pass on REST super class

```python

from lib.api.rest_client import RestClient
from tools import ServiceConfig
from lib.api.rest.sample_api.sample_api import SampleAPI

class SampleAPIconfig(RestClient, SampleAPI):
    """
    SERVICE_NAME holds the name of accepted services 
    present in api_services.YAML file
    """
    SERVICE_NAME = 'sample_service'

    def __init__(self, config={}):
        service_config = ServiceConfig()
        service = service_config.get_service_config\
            (service_name=SampleAPIconfig.SERVICE_NAME)
        api_config = service['api']

        config['hostname'] = api_config['hostname']
        config['scheme'] = api_config['scheme']
        my_config = dict(**config,
                         port=api_config['port'],
                         base_path=api_config['base_path'],
                         content_type=api_config['content_type'],
                         accept=api_config['accept']
                         )
        super(RestClient, self).__init__(my_config)
```
## API TestCase Creation
    To Create Testcases for API. 
    Create a folder in tests/functional/api/<Test_folder>
    
```python
# ~tests/test_cases/api/sample_api/test_sample_api.py

import http
import pytest
from lib.api.rest.sample_api_config import SampleAPIconfig


class TestSampleApi:

    client = SampleAPIconfig()

    data = {
        "name": "morpheus",
        "job": "leader"
    }

    @pytest.mark.run(order=1)
    def test_execute_read_call(self):
        response = self.client.read_call(path_param="2")
        assert http.HTTPStatus.OK == response.status_code, \
            "200 status code received in GET call"

```
## Running API Tests
* All sample tests:
```bash
$ cd tests

  To Run without logs

$ pytest --capture=no ./test_cases/api/sample_api_postive/

  To Run with logs
 
$ pytest ./test_cases/api/sample_api_postive/
```

## Building UI Page objects
    To build the UI Page objects. Go to lib folder
    
    1. Create Page object class with locators, actions definitions 

```python
# ~/lib/page_objects/sample_ui/sample_ui.py
from selenium.webdriver.common.by import By
from lib.ui.base_page import BasePage


class SampleUi(BasePage):
    URL = "https://www.google.com/"

    search_input = (By.CSS_SELECTOR, '[name="q"]')
    search_btn = (By.XPATH, '(//input[@role="button"])[2]')

    def load(self, driver):
        super(SampleUi, self).load()

    def enter_search_input(self, input_data):
        self.input_text(self.search_input, input_data)

    def click_search_btn(self):
        self.click(self.search_btn)
```

## UI TestCase Creation
    To Create Testcases for UI. 
    Create a folder in tests/test_cases/ui/<Testing_type>/<UI_flow_name>
    1. Place UI test cases according to functional, integration cases in folder.

```python
# ~tests/Test_cases/ui/functional/sample_ui/test_sample_ui.py

import pytest
from lib.ui.sample_ui.sample_ui import SampleUi


class TestSampleUI:

    @pytest.fixture
    def initialisation(self, driver):
        self.driver = driver
        self.sample_obj = SampleUi(self.driver)
        self.sample_obj.load(self.driver)

    def test_search_google(self, initialisation):
        self.sample_obj.enter_search_input("Testing")
        self.sample_obj.click_search_btn()

    def test_search_google_fail_case(self, initialisation):
        self.sample_obj.enter_search_input("Testing")
        self.sample_obj.click_search_btn()
        assert 1 == 2, "UI Test fails Screenshot taken and attached"
```

## Running UI Tests
* All sample UI tests:
 
```bash
$ cd tests

  To Run without logs

$ pytest --capture=no ./test_cases/ui/sample_ui/

  To Run with logs
 
$ pytest ./test_cases/ui/sample_ui

  To Run a particular case using marker using testcase id
  
$ pytest -m mapped_test_case_id ./test_cases/ui/sample_ui/<test_ui_case>.py
  
  To Run a particular case using function name
 
$ pytest -k  <function_name> ./test_cases/ui/sample_ui/<test_ui_case>.py
```
## Scope of fixtures
Scope of the fixtures refers the execution level of that fixture method
Five scopes of fixtures are **function, class, module, package** and **session**

For example: 
* If the fixture scope is declared as "**function**", then the fixture method will be executed for the function level. 
i.e) The fixture method will be executed for the function and when the execution of function is completed, 
then the fixture usage will be destroyed and re-initialised itself.   

Similar for the other scopes that fixture function will be destroyed adn re-initialised based on their scopes. 

### Note:
In this framework, the default scope of the driver is set at function.
We can modify the scope, by mentioning the SCOPE=**scope_value** as env variable

```bash
$ SCOPE=<scope> pytest <test_suite_path>
```

## Report Generation

* Reports will be generated after every execution
* Reports can be find in below names 
* Report name: **Dashboard** report - pytest_html_report.html  
* Report name: **Normal** report - test_report.html
* In dashboard report, we can able to see the test suite, cases, executed time, screenshot for UI failures
* In normal report, we can able to see the logs present in test cases
* Report can be generated in customised way also,

```bash
  To export a dashboard report add --html-report=<report_name>.html
  Report path is optional, we can use only report name

$ cd tests/
 
$ pytest --html-report=./<report_path>/<report_name>.html ./test_cases/ui/sample_ui/<test_ui_case>.py
  
  To export a normal report add --html=<report_name>.html
 
$ pytest --html=./<report_path>/<report_name>.html ./test_cases/ui/sample_ui/<test_ui_case>.py

  Customised Auto generating Report file name can be given as 
  
$ REPORT_NAME="<report_name>" pytest <test_suite_path> 
```

### Note: 
* If the execution terminated manually, reports won't be generated.
* Everytime on test case execution the reports will be created based on current **date** and execution **start time**
* Auto Report file path tests/reports/year_<current_year>/month_<current_month>/date_<current_date>/<report_name_with_timestamp>.html
* Use customize report with unique name for saving test report file.

## Coverage Report

```bash
# Run pytest with coverage and save report in coverage file  
$ coverage run -m pytest <test_case_folder_path>

# Run pytest with coverage and append report in existing coverage file
$ coverage run -a -m pytest <test_case_folder_path>

# To export coverage as html report, use below commands
$ coverage html -i <test_case_path_1> <test_case_path_2>
```
* Folder name - "**htmlcov**" will be created on tests folder
* Open **index.html** for coverage report
* Use **.coveragerc** file to omit the unwanted files