# -*- coding: utf-8 -*-
from pygov_br.camara_deputados import cd
from datetime import datetime
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


@responses.activate
def test_legislative_body_schedule():
    xml_response = """
    <pauta orgao="CDC" dataInicial="01/01/2012" dataFinal="30/04/2012">
        <reuniao>
            <comissao>CDC</comissao>
            <proposicoes>
                <proposicao>
                    <sigla>PL 1762/2011</sigla>
                </proposicao>
                <proposicao>
                    <sigla>PL 1390/2012</sigla>
                </proposicao>
            </proposicoes>
        </reuniao>
        <reuniao>
            <comissao>CDC</comissao>
            <proposicoes>
                <proposicao>
                    <sigla>PL 1762/2011</sigla>
                </proposicao>
                <proposicao>
                    <sigla>PL 1390/2012</sigla>
                </proposicao>
            </proposicoes>
        </reuniao>
    </pauta>
    """
    expected_list = [
        {'comissao': 'CDC',
         'proposicoes': {'proposicao': [{'sigla': 'PL 1762/2011'},
                                        {'sigla': 'PL 1390/2012'}]}},
        {'comissao': 'CDC',
         'proposicoes': {'proposicao': [{'sigla': 'PL 1762/2011'},
                                        {'sigla': 'PL 1390/2012'}]}}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ObterPauta',
        body=xml_response, status=200)
    result_list = cd.legislative_bodies.schedule(1, '10/10/2010', '10/10/2010')
    assert result_list == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_legislative_body_schedule_dict():
    xml_response = """
    <pauta orgao="CDC" dataInicial="01/01/2012" dataFinal="30/04/2012">
        <reuniao>
            <comissao>CDC</comissao>
            <proposicoes>
                <proposicao>
                    <sigla>PL 1762/2011</sigla>
                </proposicao>
                <proposicao>
                    <sigla>PL 1390/2012</sigla>
                </proposicao>
            </proposicoes>
        </reuniao>
    </pauta>
    """
    expected_list = [
        {'comissao': 'CDC',
         'proposicoes': {'proposicao': [{'sigla': 'PL 1762/2011'},
                                        {'sigla': 'PL 1390/2012'}]}}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ObterPauta',
        body=xml_response, status=200)
    result_list = cd.legislative_bodies.schedule(1, '10/10/2010', '10/10/2010')
    assert result_list == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_legislative_body_schedule_with_datetime():
    xml_response = """
    <pauta orgao="CDC" dataInicial="01/01/2012" dataFinal="30/04/2012">
        <reuniao>
            <comissao>CDC</comissao>
            <proposicoes>
                <proposicao>
                    <sigla>PL 1762/2011</sigla>
                </proposicao>
                <proposicao>
                    <sigla>PL 1390/2012</sigla>
                </proposicao>
            </proposicoes>
        </reuniao>
        <reuniao>
            <comissao>CDC</comissao>
            <proposicoes>
                <proposicao>
                    <sigla>PL 1762/2011</sigla>
                </proposicao>
                <proposicao>
                    <sigla>PL 1390/2012</sigla>
                </proposicao>
            </proposicoes>
        </reuniao>
    </pauta>
    """
    expected_list = [
        {'comissao': 'CDC',
         'proposicoes': {'proposicao': [{'sigla': 'PL 1762/2011'},
                                        {'sigla': 'PL 1390/2012'}]}},
        {'comissao': 'CDC',
         'proposicoes': {'proposicao': [{'sigla': 'PL 1762/2011'},
                                        {'sigla': 'PL 1390/2012'}]}}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ObterPauta',
        body=xml_response, status=200)
    result_list = cd.legislative_bodies.schedule(1, datetime.now(),
                                                 datetime.now())
    assert result_list == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_legislative_body_types():
    xml_response = """
    <tipoOrgaos>
        <tipoOrgao id="81000" descricao="Bancada"/>
        <tipoOrgao id="1000" descricao="Sociedade Civil"/>
    </tipoOrgaos>
    """
    expected_list = [
        {'id': 81000, 'descricao': 'Bancada'},
        {'id': 1000, 'descricao': 'Sociedade Civil'},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/ListarTiposOrgaos',
        body=xml_response, status=200)
    assert cd.legislative_bodies.types() == expected_list
    assert len(responses.calls) == 1
