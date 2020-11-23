"""
Test data module
 """
from collections import namedtuple
import io
import random
import string

Template = namedtuple('Template', ['file_name', 'data'])


template = Template(
    file_name='autotest_template.yaml',
    data='''
 -  id: 1
    label: 'test1'
    link: 'https://ya.ru/'
 -  id: 2
    label: 'test2'
    link: 'https://yandex.ru/'
    depends: 1
'''
)
