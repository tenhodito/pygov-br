# -*- coding: utf-8 -*-
from pygov_br.camara_deputados import cd
import responses


@responses.activate
def test_legislative_body_all():
    xml_response = """
    <orgaos>
        <orgao sigla="CAPADR "/>
        <orgao sigla="CCJC "/>
    </orgaos>
    """
    expected_list = [{'sigla': 'CAPADR'}, {'sigla': 'CCJC'}]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ObterOrgaos',
        body=xml_response, status=200)
    assert cd.legislative_bodies.all() == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_legislative_body_roles():
    xml_response = """
    <cargosOrgaos>
        <cargo id="1" descricao="Presidente"/>
        <cargo id="2" descricao="1º Vice-Presidente"/>
    </cargosOrgaos>
    """
    expected_list = [{'id': 1, 'descricao': 'Presidente'},
                     {'id': 2, 'descricao': u'1\xc2\xba Vice-Presidente'}]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ListarCargosOrgaosLegislativosCD',
        body=xml_response, status=200)
    assert cd.legislative_bodies.roles() == expected_list
    assert len(responses.calls) == 1
