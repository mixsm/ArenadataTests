from pathlib import Path

import pytest
import yaml

import config
import test_data
import tools


class TestWithoutTemplates:
    @pytest.fixture(scope='class')
    def fixture(self, init_driver):
        tools.delete_templates()
        self.driver = init_driver
        self.driver.get(config.main_page_url)
        return self

    def test_page(self, fixture):
        self = fixture
        assert self.driver.title == 'Awesome Test APP'
        element = self.driver.find_element_by_xpath(r'//h3')
        assert element.text == 'No template uploaded or your template is empty...'


class TestWithTemplate:
    @pytest.fixture(scope='class')
    def fixture(self, init_driver):
        tools.delete_templates()
        template = test_data.template
        self.yaml_template = yaml.safe_load(template.data)
        with open(Path().joinpath(config.template_files_path, 'current', 'template.yaml'), 'w') as f:
            f.write(template.data)
        self.driver = init_driver
        self.driver.get(config.main_page_url)
        return self

    def test_page(self, fixture):
        self = fixture
        assert self.driver.title == 'Awesome Test APP'
        for t in self.yaml_template:
            template_id = t['id']
            element = self.driver.find_element_by_id(template_id)
            assert element.text == t['label']
            assert element.get_attribute('href') == t.get('link')
