from pygov_br.base import ClientWrapper, Client
from pygov_br.exceptions import ClientError, ClientServerError
from pygov_br.camara_deputados.deputy import DeputyClient
from xml.etree.ElementTree import fromstring, ElementTree
import datetime
import pytest
import responses


def test_client_wrapper_with_class():
    wrapper = ClientWrapper(deputy_client=DeputyClient)
    assert isinstance(wrapper.deputy_client, DeputyClient)


def test_client_wrapper_with_instance():
    wrapper = ClientWrapper(deputy_client=DeputyClient())
    assert isinstance(wrapper.deputy_client, DeputyClient)


def test_client_instance():
    client = Client('host', timeout=10)
    assert client.host == 'host'
    assert client.timeout == 10


@responses.activate
def test_client_get():
    responses.add(responses.GET, 'http://mock.com/path',
                  body='data', status=200)
    response = Client('http://mock.com/')._get('path')

    assert len(responses.calls) == 1
    assert response == 'data'


@responses.activate
def test_client_get_with_host():
    responses.add(responses.GET, 'http://mocktest.com/path',
                  body='data', status=200)
    response = Client('http://mock.com/')._get('path',
                                               host='http://mocktest.com/')

    assert len(responses.calls) == 1
    assert response == 'data'


@responses.activate
def test_client_get_error_404():
    responses.add(responses.GET, 'http://mock.com/path',
                  body='not found', status=404)
    with pytest.raises(ClientError, message='[404]: None'):
        Client('http://mock.com/')._get('path')

    assert len(responses.calls) == 1


@responses.activate
def test_client_get_error_500():
    responses.add(responses.GET, 'http://mock.com/path',
                  body='service unavailable', status=503)
    with pytest.raises(ClientServerError):
        Client('http://mock.com/')._get('path')

    assert len(responses.calls) == 1


def test_xml_attributes_to_list():
    xml_string = """
    <parent>
        <child id="1" description="test 1"/>
        <child id="2" description="test 2"/>
        <child id="3" description="test 3"/>
        <child id="4" description="test 4"/>
    </parent>
    """
    expected_list = [
        {'id': '1', 'description': 'test 1'},
        {'id': '2', 'description': 'test 2'},
        {'id': '3', 'description': 'test 3'},
        {'id': '4', 'description': 'test 4'},
    ]
    client = Client('http://mock.com/')
    result_list = client._xml_attributes_to_list(xml_string, 'child')
    assert result_list == expected_list


def test_tree_attributes_to_list():
    xml_string = """
    <grandparent>
        <parent>
            <child id="1" description="test 1"/>
            <child id="2" description="test 2"/>
            <child id="3" description="test 3"/>
            <child id="4" description="test 4"/>
        </parent>
    </grandparent>
    """
    expected_list = [
        {'id': '1', 'description': 'test 1'},
        {'id': '2', 'description': 'test 2'},
        {'id': '3', 'description': 'test 3'},
        {'id': '4', 'description': 'test 4'},
    ]
    element_tree = ElementTree(fromstring(xml_string))
    client = Client('http://mock.com/')
    result_list = client._tree_attributes_to_list(element_tree, 'parent')
    assert result_list == expected_list


def test_make_dict_from_tree():
    xml_string = """
    <parent>
        <child>Test1</child>
        <child>Test2</child>
        <child>Test3</child>
    </parent>
    """
    expected_dict = {
        'parent': {
            'child': ['Test1', 'Test2', 'Test3']
        }
    }
    client = Client('http://mock.com/')
    etree = ElementTree(fromstring(xml_string))
    result_dict = client._make_dict_from_tree(etree.getroot())
    assert result_dict == expected_dict


def test_make_dict_from_empty_tree():
    etree = ElementTree()
    client = Client('http://mock.com/')
    expected_dict = {}
    assert client._make_dict_from_tree(etree.getroot()) == expected_dict


def test_safe_str_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element('String')) == str


def test_safe_int_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element('1')) == int


def test_safe_float_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element('1.2')) == float


def test_safe_bool_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element('True')) == bool
    assert type(client._safe_element('False')) == bool
    assert type(client._safe_element('true')) == bool
    assert type(client._safe_element('false')) == bool


def test_safe_list_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element([1, 2])) == list


def test_safe_dict_element():
    client = Client('http://mock.com/')
    assert type(client._safe_element({'key1': 'value'})) == dict


def test_safe_datetime_element():
    client = Client('http://mock.com/')
    assert isinstance(client._safe_element('10:30'), datetime.time)
    assert isinstance(client._safe_element('10:30:40'), datetime.time)
    assert isinstance(client._safe_element('10/10/2000'), datetime.date)
    assert isinstance(client._safe_element('10/10/2000 10:00'),
                      datetime.datetime)
    assert isinstance(client._safe_element('10/10/2000 10:00:12'),
                      datetime.datetime)


def test_safe_dict():
    client = Client('http://mock.com/')
    test_dict = {
        'int': '1',
        'float': '1.2',
        'str': 'string',
        'bool': 'True',
        'list': ['1', '2'],
        'dict': {'key': 'value'},
        'date': '10/10/2010',
    }
    expected_dict = {
        'int': 1,
        'float': 1.2,
        'str': 'string',
        'bool': True,
        'list': [1, 2],
        'dict': {'key': 'value'},
        'date': datetime.date(2010, 10, 10),
    }
    assert client._safe(test_dict) == expected_dict


def test_safe_list():
    client = Client('http://mock.com/')
    test_list = ['1', '1.2', 'string', 'True', ['1', '2'],
                 {'key': 'value'}, '10/10/2010']
    expected_list = [1, 1.2, 'string', True, [1, 2], {'key': 'value'},
                     datetime.date(2010, 10, 10)]
    assert client._safe(test_list) == expected_list


def test_safe_element():
    client = Client('http://mock.com/')
    assert type(client._safe('1')) == int
    assert type(client._safe('1.2')) == float
    assert type(client._safe('string')) == str
    assert type(client._safe('10:20')) == datetime.time
    assert type(client._safe('10:20:40')) == datetime.time
    assert type(client._safe('10/10/2010')) == datetime.date
    assert type(client._safe('10/10/2010 10:10')) == datetime.datetime
    assert type(client._safe('10/10/2010 10:10:20')) == datetime.datetime
