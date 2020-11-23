"""
Upload template: Upload your template file
URL: /api/v1/templates
Method: PUT
Data Params: Content-type: Form-data
Required: file=[file]
Optional: data=[json]
ex: data={"tmpl_id":"my_custom_id"}
"""
import json
from pathlib import Path

from jsonschema import validate
import pytest

import config
import conftest
import test_data
import tools

METHOD = ('PUT', 'templates')


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

    def send_request(self, payload=None):
        files = [('file', (self.template.file_name, self.template.data, 'application/octet-stream'))]
        self.response = tools.send_request(
            METHOD[0],
            config.api_url + METHOD[1],
            payload=payload,
            files=files,
            headers={}
        )

    def after(self):
        self.templates_from_server = list(Path(config.template_files_path).glob('**/autotest*.*'))

    def test_response(self, fixture):
        self = fixture
        assert self.response.status_code == 201
        validate(self.response.json_data, schema=conftest.message_schema)
        assert self.response.json_data['message'] == 'Template successfully uploaded. ' \
                                                     'tmpl_id={}'.format(self.template_id)

    def test_templates_from_server(self, fixture):
        self = fixture
        assert len(self.templates_from_server) == 1
        assert Path(self.templates_from_server[0]).stem == self.template_id
        with open(self.templates_from_server[0], 'r') as f:
            assert f.read() == self.template.data


class TestPositive(Base):
    @pytest.fixture(scope='class',
                    params=[
                        'without tmpl_id',
                        'with tmpl_id',
                    ])
    def fixture(self, request):
        self.test_case = request.param
        self.before()
        self.send_request()
        self.after()
        yield self

    def send_request(self, payload=None):
        if self.test_case == 'without tmpl_id':
            payload = None
        elif self.test_case == 'with tmpl_id':
            self.template_id = 'autotest_template_01'
            payload = {
                'data': json.dumps({'tmpl_id': self.template_id}).encode()
            }
        super().send_request(payload)


class TestBadRequest(Base):
    @pytest.fixture(scope='class',
                    params=[
                        'No file part',
                        'No file',
                        'Not allowed file type',
                    ])
    def fixture(self, request):
        self.test_case = request.param
        self.before()
        self.send_request()
        self.after()
        yield self

    def send_request(self, payload=None):
        if self.test_case == 'No file part':
            files = []
        elif self.test_case == 'No file':
            files = [('file', ('', ''))]
        elif self.test_case == 'Not allowed file type':
            files = [('file', (self.template.file_name + 'qwe', self.template.data, 'application/octet-stream'))]
        self.response = tools.send_request(
            METHOD[0],
            config.api_url + METHOD[1],
            payload=payload,
            files=files,
            headers={}
        )

    def test_response(self, fixture):
        self = fixture
        assert self.response.status_code == 400
        validate(self.response.json_data, schema=conftest.message_schema)
        if self.test_case == 'No file part':
            assert self.response.json_data['message'] == 'No file part in the request'
        elif self.test_case == 'No file':
            assert self.response.json_data['message'] == 'No file selected for uploading'
        elif self.test_case == 'Not allowed file type':
            assert self.response.json_data['message'] == "Allowed file types are {'yml', 'yaml'}"
        else:
            assert False, 'unknown test_case'

    def test_templates_from_server(self, fixture):
        self = fixture
        assert len(self.templates_from_server) == 0
