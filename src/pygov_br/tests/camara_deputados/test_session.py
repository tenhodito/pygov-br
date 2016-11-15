# -*- coding: utf-8 -*-
from pygov_br.camara_deputados import cd
from datetime import datetime
import responses


@responses.activate
def test_session_speeches():
    xml_response = """
    <sessoesDiscursos>
        <sessao>
            <codigo>321.2.54.O</codigo>
            <fasesSessao>
                <faseSessao>
                    <descricao>Homenagem</descricao>
                    <discursos>
                        <discurso>
                            <orador>
                                <nome>MAURO BENEVIDES (PRESIDENTE)</nome>
                            </orador>
                            <txtIndexacao>RECURSOS APOIO.</txtIndexacao>
                        </discurso>
                        <discurso>
                            <orador>
                                <nome>MAURO BENEVIDES (PRESIDENTE)</nome>
                            </orador>
                            <txtIndexacao>APOIO RECURSOS.</txtIndexacao>
                        </discurso>
                    </discursos>
                </faseSessao>
            </fasesSessao>
        </sessao>
    </sessoesDiscursos>
    """
    expected_list = [
        {'codigo': '321.2.54.O',
         'fasesSessao': {'faseSessao': {
             'descricao': 'Homenagem',
             'discursos': {'discurso': [
                 {'orador': {'nome': 'MAURO BENEVIDES (PRESIDENTE)'},
                  'txtIndexacao': 'RECURSOS APOIO.'},
                 {'orador': {'nome': 'MAURO BENEVIDES (PRESIDENTE)'},
                  'txtIndexacao': 'APOIO RECURSOS.'}
             ]}}
         }}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'ListarDiscursosPlenario',
        body=xml_response, status=200)
    assert cd.sessions.speeches('10/10/2010', '10/10/2010') == expected_list
    datetime_result = cd.sessions.speeches(
        datetime(2010, 10, 10), datetime(2010, 10, 10))
    assert datetime_result == expected_list
    assert len(responses.calls) == 2


@responses.activate
def test_session_speeches_multiple_sessions():
    xml_response = """
    <sessoesDiscursos>
        <sessao>
            <codigo>321.2.54.O</codigo>
            <fasesSessao>
                <faseSessao>
                    <descricao>Homenagem</descricao>
                    <discursos>
                        <discurso>
                            <orador>
                                <nome>MAURO BENEVIDES (PRESIDENTE)</nome>
                            </orador>
                            <txtIndexacao>RECURSOS APOIO.</txtIndexacao>
                        </discurso>
                    </discursos>
                </faseSessao>
            </fasesSessao>
        </sessao>
        <sessao>
            <codigo>321.2.54.O</codigo>
            <fasesSessao>
                <faseSessao>
                    <descricao>Homenagem</descricao>
                    <discursos>
                        <discurso>
                            <orador>
                                <nome>MAURO BENEVIDES (PRESIDENTE)</nome>
                            </orador>
                            <txtIndexacao>RECURSOS APOIO.</txtIndexacao>
                        </discurso>
                    </discursos>
                </faseSessao>
            </fasesSessao>
        </sessao>
    </sessoesDiscursos>
    """
    expected_list = [
        {'codigo': '321.2.54.O',
         'fasesSessao': {'faseSessao': {
             'descricao': 'Homenagem',
             'discursos': {
                 'discurso':
                 {'orador': {'nome': 'MAURO BENEVIDES (PRESIDENTE)'},
                  'txtIndexacao': 'RECURSOS APOIO.'}
             }}
         }},
        {'codigo': '321.2.54.O',
         'fasesSessao': {'faseSessao': {
             'descricao': 'Homenagem',
             'discursos': {
                 'discurso':
                 {'orador': {'nome': 'MAURO BENEVIDES (PRESIDENTE)'},
                  'txtIndexacao': 'RECURSOS APOIO.'}
             }}
         }},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'ListarDiscursosPlenario',
        body=xml_response, status=200)
    assert cd.sessions.speeches('10/10/2010', '10/10/2010') == expected_list
    datetime_result = cd.sessions.speeches(
        datetime(2010, 10, 10), datetime(2010, 10, 10))
    assert datetime_result == expected_list
    assert len(responses.calls) == 2


@responses.activate
def test_session_full_speech():
    xml_response = """
    <sessao>
        <nome>DUDIMAR PAXIUBA</nome>
        <discursoRTFBase64>
            dGVzdCBlbmNvZGVkIHN0cmluZw==
        </discursoRTFBase64>
    </sessao>
    """
    expected_dict = {'nome': 'DUDIMAR PAXIUBA',
                     'discursoRTF': b'test encoded string'}
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'obterInteiroTeorDiscursosPlenario',
        body=xml_response, status=200)
    assert cd.sessions.full_speech('200.10.3', 1, 1, 1) == expected_dict
    assert len(responses.calls) == 1


@responses.activate
def test_session_frequency():
    xml_response = """
    <dia>
        <legislatura>54</legislatura>
        <parlamentares>
            <parlamentar>
                <nomeParlamentar>Berinho Bantim</nomeParlamentar>
                <sessoesDia>
                    <sessaoDia>
                        <descricao>ORDINÁRIA 073</descricao>
                    </sessaoDia>
                    <sessaoDia>
                        <descricao>EXTRAORDINÁRIA 074</descricao>
                    </sessaoDia>
                </sessoesDia>
            </parlamentar>
        </parlamentares>
    </dia>
    """
    expected_dict = {
        'legislatura': 54,
        'parlamentares': {'parlamentar': {
            'nomeParlamentar': 'Berinho Bantim',
            'sessoesDia': {'sessaoDia': [
                {'descricao': u'ORDINÃ\x81RIA 073'},
                {'descricao': u'EXTRAORDINÃ\x81RIA 074'}
            ]}}}
    }
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'ListarPresencasDia',
        body=xml_response, status=200)
    assert cd.sessions.frequency('10/10/2010') == expected_dict
    assert cd.sessions.frequency(datetime(2010, 10, 10)) == expected_dict
    assert len(responses.calls) == 2


@responses.activate
def test_session_status():
    xml_response = """
    <situacaoReuniaoSessao>
        <situacaoReuniao id="1" descricao="Não Confirmada "/>
        <situacaoReuniao id="2" descricao="Convocada "/>
    </situacaoReuniaoSessao>
    """
    expected_list = [{'id': 1, 'descricao': u'NÃ£o Confirmada'},
                     {'id': 2, 'descricao': 'Convocada'}]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'ListarSituacoesReuniaoSessao',
        body=xml_response, status=200)
    assert cd.sessions.status() == expected_list
    assert len(responses.calls) == 1
