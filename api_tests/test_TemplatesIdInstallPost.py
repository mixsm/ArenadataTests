"""
Install template: Install previously loaded template file
URL: /api/v1/templates/:tmpl_id/install
Method: POST
URL Params:
Required: tmpl_id=[string]
"""
from pathlib import Path

from jsonschema import validate
import pytest

import config
import conftest
import test_data
import tools

METHOD = ('POST', 'templates/{id}/install')


class Base:
    """
    Base class
    """
    @pytest.fixture(scope='class')
    def fixture(self):
        self.test_case = None
        self.before()
        self.send_request()
        self.after()
        yield self

    def before(self):
        tools.delete_templates()
        self.template = test_data.template
        self.template_id = Path(self.template.file_name).stem
        with open(Path().joinpath(config.template_files_path, self.template.file_name), 'w') as f:
            f.write(self.template.data)

    def send_request(self, payload=None):
        self.response = tools.send_request(
            METHOD[0],
            config.api_url + METHOD[1].format(id=self.template_id)
        )

    def after(self):
        self.templates_from_server = list(Path(config.template_files_path).glob('current/template.*'))

    def test_response(self, fixture):
        self = fixture
        assert self.response.status_code == 200
        validate(self.response.json_data, schema=conftest.message_schema)
        assert self.response.json_data['message'] == 'Template with tmpl_id={} successfully ' \
                                                     'installed!'.format(self.template_id)

    def test_templates_from_server(self, fixture):
        self = fixture
        assert len(self.templates_from_server) == 1
        with open(self.templates_from_server[0], 'r') as f:
            assert f.read() == self.template.data


class TestPositive(Base):
    pass


class TestNotFound(Base):
    def before(self):
        tools.delete_templates()
        self.template = test_data.template
        self.template_id = Path(self.template.file_name).stem

    def test_response(self, fixture):
        self = fixture
        assert self.response.status_code == 404
        validate(self.response.json_data, schema=conftest.message_schema)
        assert self.response.json_data['message'] == 'No template with tmpl_id={} found!'.format(self.template_id)

    def test_templates_from_server(self, fixture):
        self = fixture
        assert len(self.templates_from_server) == 0
