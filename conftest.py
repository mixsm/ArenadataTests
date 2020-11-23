"""
Common fixtures and schemas
"""
import pytest
from selenium import webdriver


message_schema = {
    'type': 'object',
    'properties': {
        'message': {'type': 'string'},
    },
    'required': ['message']
}

templates_shema = {
    'type': 'object',
    'properties': {
        'templates': {'type': 'array'},
    },
    'required': ['templates']
}


@pytest.fixture(scope='module')
def init_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    yield driver
    driver.close()
