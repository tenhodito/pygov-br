# -*- coding: utf-8 -*-
from pygov_br.camara_deputados import cd
from pygov_br.exceptions import MissingParameterError
from datetime import datetime, date, time
import responses
import pytest


@responses.activate
def test_proposal_filter():
    xml_response = """
    <proposicoes>
        <proposicao>
            <nome>PL 2718/2011</nome>
            <tipoProposicao>
                <sigla>PL</sigla>
            </tipoProposicao>
            <orgaoNumerador>
                <sigla>PLEN</sigla>
            </orgaoNumerador>
            <regime>
                <txtRegime>Urgência</txtRegime>
            </regime>
            <apreciacao>
                <txtApreciacao>Apreciação do Plenário</txtApreciacao>
            </apreciacao>
            <autor1>
                <txtNomeAutor>João Paulo Cunha</txtNomeAutor>
            </autor1>
            <ultimoDespacho>
                <txtDespacho>
                Sujeita à Apreciação
                </txtDespacho>
            </ultimoDespacho>
            <situacao>
                <descricao>Arquivada</descricao>
                <orgao>
                    <siglaOrgaoEstado>ARQUIVO</siglaOrgaoEstado>
                </orgao>
                <principal>
                    <proposicaoPrincipal>PL 2473/2011</proposicaoPrincipal>
                </principal>
            </situacao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [
        {'nome': 'PL 2718/2011',
         'tipoProposicao': {'sigla': 'PL'},
         'orgaoNumerador': {'sigla': 'PLEN'},
         'regime': {'txtRegime': u'UrgÃªncia'},
         'apreciacao': {'txtApreciacao': u'ApreciaÃ§Ã£o do PlenÃ¡rio'},
         'autor1': {'txtNomeAutor': u'JoÃ£o Paulo Cunha'},
         'ultimoDespacho': {'txtDespacho': u'Sujeita Ã\xa0 ApreciaÃ§Ã£o'},
         'situacao': {'descricao': 'Arquivada',
                      'orgao': {'siglaOrgaoEstado': 'ARQUIVO'},
                      'principal': {'proposicaoPrincipal': 'PL 2473/2011'}}}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoes',
        body=xml_response, status=200)
    assert cd.proposals.filter(proposal_type='PL', year=2010) == expected_list
    result_list = cd.proposals.filter(
        proposal_type='PL',
        year=2010,
        initial_date=datetime(2010, 10, 10),
        final_date=datetime(2010, 10, 10))
    assert result_list == expected_list

    with pytest.raises(ValueError):
        cd.proposals.filter(proposal_type='PL', year=2010, in_progress='3')

    with pytest.raises(ValueError):
        cd.proposals.filter(proposal_type='PL', year=2010, author_gender='x')

    with pytest.raises(MissingParameterError):
        cd.proposals.filter()

    with pytest.raises(MissingParameterError):
        cd.proposals.filter(proposal_type='PL')

    with pytest.raises(MissingParameterError):
        cd.proposals.filter(year=2010)

    assert len(responses.calls) == 2


@responses.activate
def test_proposal_filter_dict():
    xml_response = """
    <proposicoes>
        <proposicao>
            <nome>PL 2718/2011</nome>
            <tipoProposicao>
                <sigla>PL</sigla>
            </tipoProposicao>
            <orgaoNumerador>
                <sigla>PLEN</sigla>
            </orgaoNumerador>
            <regime>
                <txtRegime>Urgência</txtRegime>
            </regime>
            <apreciacao>
                <txtApreciacao>Apreciação do Plenário</txtApreciacao>
            </apreciacao>
            <autor1>
                <txtNomeAutor>João Paulo Cunha</txtNomeAutor>
            </autor1>
            <ultimoDespacho>
                <txtDespacho>
                Sujeita à Apreciação
                </txtDespacho>
            </ultimoDespacho>
            <situacao>
                <descricao>Arquivada</descricao>
                <orgao>
                    <siglaOrgaoEstado>ARQUIVO</siglaOrgaoEstado>
                </orgao>
                <principal>
                    <proposicaoPrincipal>PL 2473/2011</proposicaoPrincipal>
                </principal>
            </situacao>
        </proposicao>
        <proposicao>
            <nome>PL 2718/2011</nome>
            <tipoProposicao>
                <sigla>PL</sigla>
            </tipoProposicao>
            <orgaoNumerador>
                <sigla>PLEN</sigla>
            </orgaoNumerador>
            <regime>
                <txtRegime>Urgência</txtRegime>
            </regime>
            <apreciacao>
                <txtApreciacao>Apreciação do Plenário</txtApreciacao>
            </apreciacao>
            <autor1>
                <txtNomeAutor>João Paulo Cunha</txtNomeAutor>
            </autor1>
            <ultimoDespacho>
                <txtDespacho>
                Sujeita à Apreciação
                </txtDespacho>
            </ultimoDespacho>
            <situacao>
                <descricao>Arquivada</descricao>
                <orgao>
                    <siglaOrgaoEstado>ARQUIVO</siglaOrgaoEstado>
                </orgao>
                <principal>
                    <proposicaoPrincipal>PL 2473/2011</proposicaoPrincipal>
                </principal>
            </situacao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [
        {'nome': 'PL 2718/2011',
         'tipoProposicao': {'sigla': 'PL'},
         'orgaoNumerador': {'sigla': 'PLEN'},
         'regime': {'txtRegime': u'UrgÃªncia'},
         'apreciacao': {'txtApreciacao': u'ApreciaÃ§Ã£o do PlenÃ¡rio'},
         'autor1': {'txtNomeAutor': u'JoÃ£o Paulo Cunha'},
         'ultimoDespacho': {'txtDespacho': u'Sujeita Ã\xa0 ApreciaÃ§Ã£o'},
         'situacao': {'descricao': 'Arquivada',
                      'orgao': {'siglaOrgaoEstado': 'ARQUIVO'},
                      'principal': {'proposicaoPrincipal': 'PL 2473/2011'}}},
        {'nome': 'PL 2718/2011',
         'tipoProposicao': {'sigla': 'PL'},
         'orgaoNumerador': {'sigla': 'PLEN'},
         'regime': {'txtRegime': u'UrgÃªncia'},
         'apreciacao': {'txtApreciacao': u'ApreciaÃ§Ã£o do PlenÃ¡rio'},
         'autor1': {'txtNomeAutor': u'JoÃ£o Paulo Cunha'},
         'ultimoDespacho': {'txtDespacho': u'Sujeita Ã\xa0 ApreciaÃ§Ã£o'},
         'situacao': {'descricao': 'Arquivada',
                      'orgao': {'siglaOrgaoEstado': 'ARQUIVO'},
                      'principal': {'proposicaoPrincipal': 'PL 2473/2011'}}},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoes',
        body=xml_response, status=200)
    assert cd.proposals.filter(proposal_type='PL', year=2010) == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_get():
    xml_response = """
    <proposicao tipo="PL " numero="3962" ano="2008">
        <nomeProposicao>PL 3962/2008</nomeProposicao>
        <idProposicao>408406</idProposicao>
        <Autor>Poder Executivo</Autor>
    </proposicao>
    """
    expected_dict = {'nomeProposicao': 'PL 3962/2008',
                     'idProposicao': 408406,
                     'Autor': 'Poder Executivo'}
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ObterProposicao',
        body=xml_response, status=200)
    assert cd.proposals.get(proposal_number=408406,
                            proposal_type='PL',
                            year=2008) == expected_dict
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_get_by_id():
    xml_response = """
    <proposicao tipo="PL " numero="3962" ano="2008">
        <nomeProposicao>PL 3962/2008</nomeProposicao>
        <idProposicao>408406</idProposicao>
        <Autor>Poder Executivo</Autor>
    </proposicao>
    """
    expected_dict = {'nomeProposicao': 'PL 3962/2008',
                     'idProposicao': 408406,
                     'Autor': 'Poder Executivo'}
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ObterProposicaoPorID',
        body=xml_response, status=200)
    assert cd.proposals.get_by_id(408406) == expected_dict
    assert len(responses.calls) == 1


@responses.activate
def test_proposals_voting():
    xml_response = """
    <proposicao>
        <Sigla>PL</Sigla>
        <Numero>1992</Numero>
        <Ano>2007</Ano>
        <Votacoes>
            <Votacao Resumo="Aprovada" Data="28/2/2012" Hora="20:26"
                     ObjVotacao="SUBEMENDA SUBSTITUTIVA GLOBAL DE PLENÁRIO"
                     codSessao="4531">
            <orientacaoBancada>
                <bancada Sigla="PT" orientacao="Sim "/>
                <bancada Sigla="PMDB" orientacao="Sim "/>
            </orientacaoBancada>
            <votos>
                <Deputado Nome="Henrique Afonso" ideCadastro="73940"
                          Partido="PV " UF="AC" Voto="Sim "/>
                <Deputado Nome="Carlos Souza" ideCadastro="73934"
                          Partido="PSD " UF="AM" Voto="Sim "/>
            </votos>
            </Votacao>
        </Votacoes>
    </proposicao>
    """
    expected_list = [{
        'Resumo': 'Aprovada',
        'Data': date(2012, 2, 28),
        'Hora': time(20, 26),
        'ObjVotacao': u'SUBEMENDA SUBSTITUTIVA GLOBAL DE PLENÃ\x81RIO',
        'codSessao': 4531,
        'orientacaoBancada': [{'Sigla': 'PT', 'orientacao': 'Sim'},
                              {'Sigla': 'PMDB', 'orientacao': 'Sim'}],
        'votos': [{'Nome': 'Henrique Afonso', 'ideCadastro': 73940,
                   'Partido': 'PV', 'UF': 'AC', 'Voto': 'Sim'},
                  {'Nome': 'Carlos Souza', 'ideCadastro': 73934,
                   'Partido': 'PSD', 'UF': 'AM', 'Voto': 'Sim'},]
    }]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ObterVotacaoProposicao',
        body=xml_response, status=200)
    assert cd.proposals.voting(proposal_number=408406,
                               proposal_type='PL',
                               year=2008) == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_voted():
    xml_response = """
    <proposicoes>
        <proposicao>
            <nomeProposicao>PEC 3/1999</nomeProposicao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [
        {'nomeProposicao': 'PEC 3/1999'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoesVotadasEmPlenario',
        body=xml_response, status=200)
    assert cd.proposals.voted(proposal_type='PL',
                              year=2008) == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_voted_dict():
    xml_response = """
    <proposicoes>
        <proposicao>
            <nomeProposicao>PEC 3/1999</nomeProposicao>
        </proposicao>
        <proposicao>
            <nomeProposicao>PEC 3/1999</nomeProposicao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [
        {'nomeProposicao': 'PEC 3/1999'},
        {'nomeProposicao': 'PEC 3/1999'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoesVotadasEmPlenario',
        body=xml_response, status=200)
    assert cd.proposals.voted(proposal_type='PL',
                              year=2008) == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_processed_in_period():
    xml_response = """
    <proposicoes>
        <proposicao>
            <tipoProposicao>MPV</tipoProposicao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [{'tipoProposicao': 'MPV'}]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoesTramitadasNoPeriodo',
        body=xml_response, status=200)
    assert cd.proposals.processed_in_period(
        initial_date='10/10/2010',
        final_date='11/10/2010') == expected_list
    assert cd.proposals.processed_in_period(
        initial_date=datetime(2010, 10, 10),
        final_date=datetime(2010, 10, 11)) == expected_list
    assert len(responses.calls) == 2


@responses.activate
def test_proposal_processed_in_period_dict():
    xml_response = """
    <proposicoes>
        <proposicao>
            <tipoProposicao>MPV</tipoProposicao>
        </proposicao>
        <proposicao>
            <tipoProposicao>MPV</tipoProposicao>
        </proposicao>
    </proposicoes>
    """
    expected_list = [{'tipoProposicao': 'MPV'}, {'tipoProposicao': 'MPV'}]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarProposicoesTramitadasNoPeriodo',
        body=xml_response, status=200)
    assert cd.proposals.processed_in_period(
        initial_date='10/10/2010',
        final_date='11/10/2010') == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_proposal_progress():
    xml_response = """
    <proposicao tipo="PL" numero="3962" ano="2008">
        <idProposicao>408406</idProposicao>
        <ultimaAcao>
            <tramitacao>
                <orgao>MESA</orgao>
            </tramitacao>
        </ultimaAcao>
        <andamento>
            <tramitacao>
                <orgao>MESA</orgao>
            </tramitacao>
            <tramitacao>
                <orgao>MESA</orgao>
            </tramitacao>
        </andamento>
    </proposicao>
    """
    expected_dict = {
        'idProposicao': 408406,
        'ultimaAcao': {'tramitacao': {'orgao': 'MESA'}},
        'andamento': {'tramitacao': [{'orgao': 'MESA'},
                                     {'orgao': 'MESA'}]}
    }
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterAndamento',
        body=xml_response, status=200)
    assert cd.proposals.progress(proposal_number=1293,
                                 year=2008) == expected_dict
    assert cd.proposals.progress(proposal_number=1293,
                                 initial_date='10/10/2010',
                                 year=2008) == expected_dict
    assert cd.proposals.progress(proposal_number=1293,
                                 initial_date=datetime(2012, 10, 10),
                                 year=2008) == expected_dict
    assert len(responses.calls) == 3


@responses.activate
def test_proposal_amendments():
    xml_response = """
    <Proposicao tipo="PL" Numero="3962" Ano="2008">
        <Substitutivos>
            <Substitutivo CodProposicao="439782"
                          Descricao="SBT 1 CTASP => PL 3962/2008"/>
        </Substitutivos>
        <RedacoesFinais>
            <RedacaoFinal CodProposicao="440524"
                          Descricao="RDF 1 => PL 3962/2008"/>
        </RedacoesFinais>
        <Emendas>
            <Emenda CodProposicao="413968"
                    Descricao="EMC 1/2008 CSSF => PL 3962/2008"/>
            <Emenda CodProposicao="413970"
                    Descricao="EMC 2/2008 CSSF => PL 3962/2008"/>
        </Emendas>
    </Proposicao>
    """
    expected_list = [
        {'CodProposicao': 413968,
         'Descricao': 'EMC 1/2008 CSSF => PL 3962/2008'},
        {'CodProposicao': 413970,
         'Descricao': 'EMC 2/2008 CSSF => PL 3962/2008'},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterEmendasSubstitutivoRedacaoFinal',
        body=xml_response, status=200)
    assert cd.proposals.amendments(proposal_number=1293,
                                   proposal_type='PL',
                                   year=2008) == expected_list


@responses.activate
def test_proposal_final_wordings():
    xml_response = """
    <Proposicao tipo="PL" Numero="3962" Ano="2008">
        <Substitutivos>
            <Substitutivo CodProposicao="439782"
                          Descricao="SBT 1 CTASP => PL 3962/2008"/>
        </Substitutivos>
        <RedacoesFinais>
            <RedacaoFinal CodProposicao="440524"
                          Descricao="RDF 1 => PL 3962/2008"/>
        </RedacoesFinais>
        <Emendas>
            <Emenda CodProposicao="413968"
                    Descricao="EMC 1/2008 CSSF => PL 3962/2008"/>
            <Emenda CodProposicao="413970"
                    Descricao="EMC 2/2008 CSSF => PL 3962/2008"/>
        </Emendas>
    </Proposicao>
    """
    expected_list = [
        {'CodProposicao': 440524,
         'Descricao': 'RDF 1 => PL 3962/2008'},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterEmendasSubstitutivoRedacaoFinal',
        body=xml_response, status=200)
    assert cd.proposals.final_wordings(proposal_number=1293,
                                       proposal_type='PL',
                                       year=2008) == expected_list


@responses.activate
def test_proposal_substitutives():
    xml_response = """
    <Proposicao tipo="PL" Numero="3962" Ano="2008">
        <Substitutivos>
            <Substitutivo CodProposicao="439782"
                          Descricao="SBT 1 CTASP => PL 3962/2008"/>
        </Substitutivos>
        <RedacoesFinais>
            <RedacaoFinal CodProposicao="440524"
                          Descricao="RDF 1 => PL 3962/2008"/>
        </RedacoesFinais>
        <Emendas>
            <Emenda CodProposicao="413968"
                    Descricao="EMC 1/2008 CSSF => PL 3962/2008"/>
            <Emenda CodProposicao="413970"
                    Descricao="EMC 2/2008 CSSF => PL 3962/2008"/>
        </Emendas>
    </Proposicao>
    """
    expected_list = [
        {'CodProposicao': 439782,
         'Descricao': 'SBT 1 CTASP => PL 3962/2008'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterEmendasSubstitutivoRedacaoFinal',
        body=xml_response, status=200)
    assert cd.proposals.substitutives(proposal_number=1293,
                                      proposal_type='PL',
                                      year=2008) == expected_list


@responses.activate
def test_proposal_comissions_opinion():
    xml_response = """
    <proposicao tipo="PL" numero="3962" ano="2008" codProposicao="408406">
        <integra LinkArquivo="http://www.camara.gov.br/?codteor=595202"/>
        <comissoes>
            <comissao nome="Comissão de Trabalho" sigla="CT" codOrgao="2015">
                <tipoAnalise>Constitucionalidade</tipoAnalise>
                <relator>Arnaldo Faria</relator>
            </comissao>
        </comissoes>
    </proposicao>
    """
    expected_list = [
        {'tipoAnalise': 'Constitucionalidade',
         'relator': 'Arnaldo Faria'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterIntegraComissoesRelator',
        body=xml_response, status=200)
    assert cd.proposals.comissions_opinion(proposal_number=1293,
                                           proposal_type='PL',
                                           year=2008) == expected_list


@responses.activate
def test_proposal_comissions_opinion_dict():
    xml_response = """
    <proposicao tipo="PL" numero="3962" ano="2008" codProposicao="408406">
        <integra LinkArquivo="http://www.camara.gov.br/?codteor=595202"/>
        <comissoes>
            <comissao nome="Comissão de Trabalho" sigla="CT" codOrgao="2015">
                <tipoAnalise>Constitucionalidade</tipoAnalise>
                <relator>Arnaldo Faria</relator>
            </comissao>
            <comissao nome="Comissão de Trabalho" sigla="CT" codOrgao="2015">
                <tipoAnalise>Constitucionalidade</tipoAnalise>
                <relator>Arnaldo Faria</relator>
            </comissao>
        </comissoes>
    </proposicao>
    """
    expected_list = [
        {'tipoAnalise': 'Constitucionalidade',
         'relator': 'Arnaldo Faria'},
        {'tipoAnalise': 'Constitucionalidade',
         'relator': 'Arnaldo Faria'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        'ObterIntegraComissoesRelator',
        body=xml_response, status=200)
    assert cd.proposals.comissions_opinion(proposal_number=1293,
                                           proposal_type='PL',
                                           year=2008) == expected_list


@responses.activate
def test_proposal_types():
    xml_response = """
    <siglas>
        <sigla tipoSigla="ADD " descricao="Adendo" ativa="True"/>
    </siglas>
    """
    expected_list = [
        {'tipoSigla': 'ADD', 'descricao': 'Adendo', 'ativa': True}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarSiglasTipoProposicao',
        body=xml_response, status=200)
    assert cd.proposals.types() == expected_list


@responses.activate
def test_proposal_author_types():
    xml_response = """
    <siglas>
        <TipoAutor id="TipoOrgao_11" descricao="Conselho"/>
    </siglas>
    """
    expected_list = [
        {'id': 'TipoOrgao_11', 'descricao': 'Conselho'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarTiposAutores',
        body=xml_response, status=200)
    assert cd.proposals.author_types() == expected_list


@responses.activate
def test_proposal_statuses():
    xml_response = """
    <situacaoProposicao>
        <situacaoProposicao id="1180" descricao="Aguardando Apoiamento"/>
    </situacaoProposicao>
    """
    expected_list = [
        {'id': 1180, 'descricao': 'Aguardando Apoiamento'}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        'ListarSituacoesProposicao',
        body=xml_response, status=200)
    assert cd.proposals.statuses() == expected_list
