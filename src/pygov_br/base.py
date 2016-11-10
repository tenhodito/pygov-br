# -*- coding: utf-8 -*-
from distutils.util import strtobool
from xml.etree.ElementTree import fromstring, ElementTree
from pygov_br.exceptions import ClientError, ClientServerError
from datetime import datetime
from inspect import isclass
import logging
import requests
import sys

if sys.version_info < (3, 0):
    from urlparse import urljoin
else:
    from urllib.parse import urljoin

log = logging.getLogger('pygov_br.client')


class ClientWrapper(object):
    """Base class to client wrapper."""

    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if isclass(kwargs[key]):
                value = kwargs[key]()
            else:
                value = kwargs[key]
            setattr(self, key, value)


class Client(object):
    """Base class to interact with API."""

    def __init__(self, host, timeout=None):
        self.host = host
        self.timeout = timeout

    def _get(self, path, **kwargs):
        return self._request('GET', path, kwargs)

    def _request(self, verb, path, params):
        host = params.pop('host', None)
        if host:
            url = urljoin(host, path)
        else:
            url = urljoin(self.host, path)

        response = requests.request(verb, url, params=params,
                                    timeout=self.timeout)
        log.debug('Response [{}]: {}'.format(response.status_code,
                                             repr(response.text)))

        if not response.ok:
            msg = "[{}]: {}".format(response.status_code, response.reason)
            if 400 <= response.status_code < 500:
                raise ClientError(msg, response=response)
            else:
                raise ClientServerError(msg + response.text, response=response)

        return response.text

    def _xml_attributes_to_list(self, xml_string, xml_tag):
        element_list = []
        element_tree = ElementTree(fromstring(xml_string.encode('utf-8')))
        for element in element_tree.findall(xml_tag):
            element_list.append(element.attrib)
        return element_list

    def _tree_attributes_to_list(self, element_tree, parent):
        elements = element_tree.find(parent)
        elements_list = []
        for child in elements.getchildren():
            elements_list.append(child.attrib)
        return elements_list

    def _xml_to_dict(self, xml_string):
        etree = ElementTree(fromstring(xml_string.encode('utf-8')))
        return self._make_dict_from_tree(etree.getroot())

    def _make_dict_from_tree(self, element_tree):
        def internal_iter(tree, accum):
            if tree is None:
                return accum

            if tree.getchildren():
                accum[tree.tag] = {}
                for each in tree.getchildren():
                    result = internal_iter(each, {})
                    if each.tag in accum[tree.tag]:
                        if not isinstance(accum[tree.tag][each.tag], list):
                            accum[tree.tag][each.tag] = [
                                accum[tree.tag][each.tag]
                            ]
                        accum[tree.tag][each.tag].append(result[each.tag])
                    else:
                        accum[tree.tag].update(result)
            else:
                accum[tree.tag] = tree.text

            return accum

        return internal_iter(element_tree, {})

    def _safe(self, element):
        if isinstance(element, list):
            safe_element = self._safe_list(element)
        elif isinstance(element, dict):
            safe_element = self._safe_dict(element)
        else:
            safe_element = self._safe_element(element)
        return safe_element

    def _safe_dict(self, dictionary):
        for key in dictionary.keys():
            dictionary[key] = self._safe_element(dictionary[key])

        return dictionary

    def _safe_element(self, element):
        if self._is_digit(element):
            safe_element = int(element)
        elif self._is_float(element):
            safe_element = float(element)
        elif self._is_bool(element):
            safe_element = bool(strtobool(element))
        elif isinstance(element, dict):
            safe_element = self._safe_dict(element)
        elif isinstance(element, list):
            safe_element = self._safe_list(element)
        else:
            safe_element = self._to_date_or_default(element)
        return safe_element

    def _safe_list(self, data_list):
        for index, element in enumerate(data_list):
            data_list[index] = self._safe_element(element)
        return data_list

    def _is_float(self, string):
        try:
            float(string)
            return True
        except (ValueError, TypeError):
            return False

    def _is_digit(self, string):
        try:
            int(string)
            return True
        except (ValueError, TypeError):
            return False

    def _is_bool(self, string):
        try:
            strtobool(string)
            return True
        except (ValueError, TypeError, AttributeError):
            return False

    def _to_date_or_default(self, string):
        final_value = None
        date_formats = {
            '%d/%m/%Y': 'date',
            '%d/%m/%Y %H:%M:%S': None,
            '%d/%m/%Y %H:%M': None,
            '%H:%M': 'time',
            '%H:%M:%S': 'time'
        }
        for date_format in date_formats.keys():
            try:
                final_value = datetime.strptime(string, date_format)
                if date_formats[date_format]:
                    get_date_type = getattr(final_value,
                                            date_formats[date_format])
                    final_value = get_date_type()
                break
            except (ValueError, TypeError):
                final_value = string.strip() if string else None
        return final_value
