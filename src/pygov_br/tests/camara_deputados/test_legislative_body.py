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


@responses.activate
def test_legislative_body_members():
    xml_response = """
    <orgao nome="Comissão de Defesa do Consumidor">
        <membros>
            <Presidente>
                <nome>Marco Tebaldi</nome>
            </Presidente>
            <PrimeiroVice-Presidente>
                <nome>Nelson Marchezan Junior</nome>
            </PrimeiroVice-Presidente>
            <SegundoVice-Presidente>
                <nome>Marcos Rotta</nome>
            </SegundoVice-Presidente>
            <TerceiroVice-Presidente>
                <nome>Maria Helena</nome>
            </TerceiroVice-Presidente>
            <membro>
                <nome>Antônio Jácome</nome>
            </membro>
            <membro>
                <nome>Celso Russomanno</nome>
            </membro>
        </membros>
    </orgao>
    """
    expected_dict = {
        'Presidente': {'nome': 'Marco Tebaldi'},
        'PrimeiroVice-Presidente': {'nome': 'Nelson Marchezan Junior'},
        'SegundoVice-Presidente': {'nome': 'Marcos Rotta'},
        'TerceiroVice-Presidente': {'nome': 'Maria Helena'},
        'membro': [{'nome': u'Ant\xc3\xb4nio J\xc3\xa1come'},
                   {'nome': 'Celso Russomanno'}]
    }
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ObterMembrosOrgao',
        body=xml_response, status=200)
    assert cd.legislative_bodies.members(1) == expected_dict
    assert len(responses.calls) == 1
