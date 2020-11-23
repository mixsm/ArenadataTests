"""
List templates: List all currently uploaded templates
URL: /api/v1/templates
Method: GET
"""
from pathlib import Path

from jsonschema import validate
import pytest

import config
import conftest
import test_data
import tools

METHOD = ('GET', 'templates')
# bug: the method returns all types of files


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
        template = test_data.template
        with open(Path().joinpath(config.template_files_path, template.file_name), 'w') as f:
            f.write(template.data)
        path = Path(config.template_files_path)
        self.templates = [Path(f).stem for f in list(path.glob('*.yml')) + list(path.glob('*.yaml'))]

    def send_request(self):
        self.response = tools.send_request(
            METHOD[0],
            config.api_url + METHOD[1]
        )

    def after(self):
        pass

    def test_response(self, fixture):
        self = fixture
        assert self.response.status_code == 200
        validate(self.response.json_data, schema=conftest.templates_shema)
        assert len(self.response.json_data['templates']) == len(self.templates)
        templates_from_response = sorted(self.response.json_data['templates'])
        for i, template in enumerate(sorted(self.templates)):
            assert templates_from_response[i] == template


class TestPositive(Base):
    pass



