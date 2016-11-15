# -*- coding: utf-8 -*-
from pygov_br.base import Client
from pygov_br.exceptions import MissingParameterError
from xml.etree.ElementTree import fromstring, ElementTree
from datetime import datetime


class ProposalClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        super(ProposalClient, self).__init__(host)

    def filter(self, proposal_type='', year='', proposal_number='',
               initial_date='', final_date='', author_name='',
               author_type_id='', author_party_initials='', author_region='',
               author_gender='', status_id='', legislative_body_id='',
               in_progress=''):
        r"""Fetch filtered proposals.

        The `proposal_type` and `year` parameters are mandatory if
        `author_name` is empty.

        Args:
            proposal_type (str): Proposal type initials.
            year (int): Proposal's year.
            author_name (str): Part of author name.
            proposal_number (int, optional): Proposal number.
            initial_date (str or datetime, optional): Initial date of period.
                If `str`, must be in the format: `dd/mm/yyyy`.
            final_date (str or datetime, optional): Final date of period. If
                `str`,must be in the format: `dd/mm/yyyy`.
            author_type_id (int, optional): Author type identifier.
            author_party_initials (str, optional): Author's party initials
                identifier.
            author_gender (str, optional): Author gender. `M` for male or `F`
                for female.
            status_id (int, optional): Proposal status identifier.
            legislative_body_id (int, optional): Legislative body identifier.
            in_progress (int, optional): Proposal progress indication. `1` to
                `in progress` and `2` to `closed processing`.

        Returns:
            list: A list of the filtered proposals. Example::

                [{'ano': 2016,
                  'apreciacao': {'id': 5,
                   'txtApreciacao': 'Proposição Sujeita à Apreciação do ' \
                                    'Plenário'},
                  'autor1': {'codPartido': None,
                   'idecadastro': None,
                   'txtNomeAutor': 'Poder Executivo',
                   'txtSiglaPartido': None,
                   'txtSiglaUF': None},
                  'datApresentacao': datetime.datetime(2016, 11, 4, 18, 2),
                  'id': 2116055,
                  'indGenero': 'o',
                  'nome': 'PL 6427/2016',
                  'numero': 6427,
                  'orgaoNumerador': {'id': 180, 'nome': 'PLENÁRIO',
                                     'sigla': 'PLEN'},
                  'qtdAutores': 1,
                  'qtdOrgaosComEstado': 0,
                  'regime': {'codRegime': 22,
                             'txtRegime': 'Urgência art. 64 CF'},
                  'situacao': {'descricao': None,
                   'id': None,
                   'orgao': {'codOrgaoEstado': None, 'siglaOrgaoEstado': None},
                   'principal': {'codProposicaoPrincipal': 0,
                                 'proposicaoPrincipal': None}},
                  'tipoProposicao': {'id': 139, 'nome': 'Projeto de Lei',
                                     'sigla': 'PL'},
                  'txtEmenta': 'Altera a Lei nº 8.213, de 24 de julho de ' \
                               '1991, que dispõe sobre os Planos de ' \
                               'Benefícios da Previdência Social, e institui' \
                               'o Bônus Especial de Desempenho Institucional' \
                               ' por Perícia Médica em Benefícios por ' \
                               Incapacidade.',
                  'txtExplicacaoEmenta': None,
                  'ultimoDespacho': {'datDespacho': datetime.date(2016, 11, 4),
                   'txtDespacho': 'Às Comissões de Trabalho, de ' \
                                  'Administração e Serviço Público; ' \
                                  'Seguridade Social e Família; Finanças e ' \
                                  'Tributação (Art. 54 RICD) e Constituição ' \
                                  'e Justiça e de Cidadania (Art. 54 RICD)' \
                                  'Proposição Sujeita à Apreciação do ' \
                                  'Plenário. Regime de Tramitação: Urgência ' \
                                  'art. 64 CF'}}, ...]

        Raises:
            MissingParameterError: If `author_name` is empty AND
                `proposal_type` OR `year` OR both are empty too.
            ValueError: `author_gender` is not `M` or `F` or if `in_progress`
                is not `1` or `2`

        """
        proposal_type_or_year = proposal_type == '' or year == ''
        if author_name == '' and proposal_type_or_year:
            raise MissingParameterError(
                "The 'proposal_type' and 'year' parameters are mandatory if "
                "'author_name' is empty."
            )

        if author_gender not in ['M', 'm', 'F', 'f', '']:
            raise ValueError("'author_gender' must be 'M' or 'F'.")

        if in_progress not in [1, 2, '']:
            raise ValueError("'in_progress' must be '1' or '2'.")

        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ListarProposicoes?sigla={0}&numero={1}&ano={2}&" \
               "datApresentacaoIni={3}&datApresentacaoFim={4}&" \
               "parteNomeAutor={5}&idTipoAutor={6}&siglaPartidoAutor={7}&" \
               "siglaUFAutor={8}&generoAutor={9}&codEstado={10}&" \
               "codOrgaoEstado={11}&emTramitacao={12}"
        xml_response = self._get(path.format(
            proposal_type, proposal_number, year, initial_date, final_date,
            author_name, author_type_id, author_party_initials, author_region,
            author_gender, status_id, legislative_body_id, in_progress
        ))
        dict_response = self._xml_to_dict(xml_response)
        list_response = dict_response['proposicoes']['proposicao']
        if isinstance(list_response, dict):
            list_response = [list_response]

        return self._safe(list_response)

    def get(self, proposal_type, proposal_number, year):
        r"""Fetch detailed proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            dict: A detailed information about one proposal. Example::

                {'Apreciacao': 'Proposição Sujeita à Apreciação do Plenário',
                 'Autor': 'João Paulo Cunha',
                 'DataApresentacao': datetime.date(2011, 11, 16),
                 'Ementa': 'Altera a Lei nº 9.503, de 23 de setembro de 1997' \
                           'que institui o Código de Trânsito Brasileiro, ' \
                           'para dispor sobre a suspensão imediata do ' \
                           'direito de dirigir do condutor envolvido em ' \
                           'acidente de trânsito com vítima fatal, sob a ' \
                           'influência de álcool.',
                 'ExplicacaoEmenta': '',
                 'Indexacao': 'Alteração, Código de Trânsito Brasileiro, ' \
                              'suspensão, habilitação, condutor, veículo ' \
                              'automotor, ingestão, bebida alcoólica, ' \
                              'acidente de trânsito, morte, vítima.',
                 'LinkInteiroTeor': 'http://www.camara.gov.br/proposicoesWeb' \
                                    '/prop_mostrarintegra?codteor=939420',
                 'RegimeTramitacao': 'Urgência art. 155 RICD',
                 'Situacao': 'ARQUIVO - Arquivada',
                 'UltimoDespacho': 'Apense-se à(ao) PL-2473/2011.\n' \
                                   'Proposição Sujeita à Apreciação do ' \
                                   'Plenário\nRegime de Tramitação: ' \
                                   Prioridade',
                 'apensadas': None,
                 'idProposicao': 527478,
                 'idProposicaoPrincipal': '',
                 'ideCadastro': 73534,
                 'nomeProposicao': 'PL 2718/2011',
                 'nomeProposicaoOrigem': '',
                 'partidoAutor': 'PT',
                 'tema': 'Desenvolvimento Urbano e Trânsito',
                 'tipoProposicao': 'Projeto de Lei',
                 'ufAutor': 'SP'}

        """
        path = "ObterProposicao?tipo={0}&numero={1}&ano={2}"
        xml_response = self._get(path.format(proposal_type, proposal_number,
                                             year))
        dict_response = self._xml_to_dict(xml_response)
        return self._safe(dict_response['proposicao'])

    def get_by_id(self, proposal_id):
        r"""Fetch detailed proposal by id.

        Args:
            proposal_id (int): Proposal identifier.]

        Returns:
            dict: A detailed information about one proposal. Example::

                {'Apreciacao': 'Proposição Sujeita à Apreciação do Plenário',
                 'Autor': 'João Paulo Cunha',
                 'DataApresentacao': datetime.date(2011, 11, 16),
                 'Ementa': 'Altera a Lei nº 9.503, de 23 de setembro de 1997' \
                           'que institui o Código de Trânsito Brasileiro, ' \
                           'para dispor sobre a suspensão imediata do ' \
                           'direito de dirigir do condutor envolvido em ' \
                           'acidente de trânsito com vítima fatal, sob a ' \
                           'influência de álcool.',
                 'ExplicacaoEmenta': '',
                 'Indexacao': 'Alteração, Código de Trânsito Brasileiro, ' \
                              'suspensão, habilitação, condutor, veículo ' \
                              'automotor, ingestão, bebida alcoólica, ' \
                              'acidente de trânsito, morte, vítima.',
                 'LinkInteiroTeor': 'http://www.camara.gov.br/proposicoesWeb' \
                                    '/prop_mostrarintegra?codteor=939420',
                 'RegimeTramitacao': 'Urgência art. 155 RICD',
                 'Situacao': 'ARQUIVO - Arquivada',
                 'UltimoDespacho': 'Apense-se à(ao) PL-2473/2011.\n' \
                                   'Proposição Sujeita à Apreciação do ' \
                                   'Plenário\nRegime de Tramitação: ' \
                                   Prioridade',
                 'apensadas': None,
                 'idProposicao': 527478,
                 'idProposicaoPrincipal': '',
                 'ideCadastro': 73534,
                 'nomeProposicao': 'PL 2718/2011',
                 'nomeProposicaoOrigem': '',
                 'partidoAutor': 'PT',
                 'tema': 'Desenvolvimento Urbano e Trânsito',
                 'tipoProposicao': 'Projeto de Lei',
                 'ufAutor': 'SP'}

        """
        path = "ObterProposicaoPorID?IdProp={0}"
        xml_response = self._get(path.format(proposal_id))
        dict_response = self._xml_to_dict(xml_response)
        return self._safe(dict_response['proposicao'])

    def voting(self, proposal_type, proposal_number, year):
        r"""Fetch all votings of a proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            list: A list of a specified proposal votings. Example:

                [{'Data': datetime.date(2012, 2, 29),
                  'Hora': datetime.time(19, 9),
                  'ObjVotacao': 'DVS - DEM - EMENDA 26',
                  'Resumo': 'Rejeitada a Emenda nº 26. Sim: 11; não: 275; ' \
                            'abstenção:02; total: 388.',
                  'codSessao': 4533,
                  'orientacaoBancada': [{'Sigla': 'PT', 'orientacao': 'Não'},
                   {'Sigla': 'PMDB', 'orientacao': 'Não'}, ...],
                  'votos': [
                   {'Nome': 'Nilson Leitão',
                    'Partido': 'PSDB',
                    'UF': 'MT',
                    'Voto': 'Sim',
                    'ideCadastro': 166401}, ...]
                 }, ...]

        """
        path = "ObterVotacaoProposicao?tipo={0}&numero={1}&ano={2}"
        xml_response = self._get(path.format(proposal_type, proposal_number,
                                             year))
        element_tree = ElementTree(fromstring(xml_response.encode('utf-8')))

        voting = element_tree.find('Votacoes')
        voting_list = []
        for child in voting.getchildren():
            voting_dict = child.attrib
            seat_orientation_list = []
            for orientation in child.find('orientacaoBancada').getchildren():
                seat_orientation_list.append(orientation.attrib)
            voting_dict['orientacaoBancada'] = seat_orientation_list

            votes_list = []
            for vote in child.find('votos').getchildren():
                votes_list.append(vote.attrib)
            voting_dict['votos'] = votes_list

            voting_list.append(voting_dict)

        return self._safe(voting_list)

    def voted(self, year, proposal_type=''):
        """Fetch all voted proposals in the year.

        Args:
            year (int): Proposal's year.
            proposal_type (str): Proposal type initials.

        Returns:
            list: a list of proposals that was voted in the year. Example::

                [{'codProposicao': 2078295,
                  'dataVotacao': datetime.date(2016, 10, 5),
                  'nomeProposicao': 'PL 4567/2016'}, ...]

        """
        path = 'ListarProposicoesVotadasEmPlenario?ano={0}&tipo={1}'
        xml_response = self._get(path.format(year, proposal_type))
        dict_response = self._xml_to_dict(xml_response)
        list_response = dict_response['proposicoes']['proposicao']

        if isinstance(list_response, dict):
            list_response = [list_response]
        return self._safe(list_response)

    def processed_in_period(self, initial_date, final_date):
        """Fetch all processed proposals in the period.

        Args:
            initial_date (str or datetime): Initial date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            final_date (str or datetime): Final date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.

        Returns:
            list: A list of proposal that was processed in the period.
            Example::

                [{'ano': 2013,
                  'codProposicao': 590279,
                  'dataAlteracao': datetime.datetime(2013, 10, 1, 11, 16, 28),
                  'dataTramitacao': datetime.date(2013, 9, 20),
                  'numero': 47,
                  'tipoProposicao': 'SIT'}, ...]

        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = 'ListarProposicoesTramitadasNoPeriodo?dtInicio={0}&dtFim={1}'
        xml_response = self._get(path.format(initial_date, final_date))
        dict_response = self._xml_to_dict(xml_response)
        list_response = dict_response['proposicoes']['proposicao']

        if isinstance(list_response, dict):
            list_response = [list_response]
        return self._safe(list_response)

    def progress(self, proposal_number, year, proposal_type='',
                 initial_date='', legislative_body_id=''):
        r"""Fetch the progress of a proposal.

        Args:
            proposal_number (int): Proposal number.
            year (int): Proposal's year.
            proposal_type (str, optional): Proposal type initials.
            initial_date (str or datetime, optional): Initial date of period.
                If `str`, must be in the format: `dd/mm/yyyy`.
            legislative_body_id (int, optional): Legislative body identifier.

        Returns:
            dict: A dictc with progress steps of a proposal.

                {'andamento': {'tramitacao': [{'codOrgao': 4,
                    'data': datetime.date(2009, 12, 23),
                    'descricao': 'Transformado na Lei Ordinária 12154/2009.' \
                                 'DOU 24 12 09 PÁG 01 COL 01. Vetado ' \
                                 'parcialmente. Razões do veto: MSC ' \
                                 '1.085/09-PE. DOU (Edição extra) 24 12 09' \
                                 'PÁG 8 COL 02.',
                    'inteiroTeor': None,
                    'ordemDeTramitacao': 87,
                    'orgao': 'MESA'}, ...]},
                 'ementa': 'Cria a Superintendência Nacional de Previdência' \
                           'Complementar - PREVIC e dispõe sobre o seu ' \
                           'pessoal, inclui a Câmara de Recursos da ' \
                           'Previdência Complementar na estrutura básica do' \
                           'Ministério da Previdência Social, altera ' \
                           'disposições referentes a auditores-fiscais da' \
                           'Receita Federal do Brasil, e dá outras' \
                           'providências.',
                 'idProposicao': 408406,
                 'situacao': 'Tranformada no(a) Lei Ordinária 12154/2009',
                 'ultimaAcao': {'tramitacao': {'codOrgao': 4,
                   'data': datetime.date(2010, 2, 10),
                   'descricao': 'Recebimento do Ofício nº 60/10 (CN) ' \
                                'comunicando veto parcial e solicitando ' \
                                'indicação de membros para integrar a ' \
                                'Comissão Mista incumbida de relatar o(s) ' \
                                'veto(s).',
                   'ordemDeTramitacao': 89,
                   'orgao': 'MESA - Mesa Diretora da Câmara dos Deputados'}}}

        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')

        path = 'ObterAndamento?sigla={0}&numero={1}&ano={2}&' \
               'dataIni={3}&codOrgao={4}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year,
                        initial_date, legislative_body_id),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        dict_response = self._xml_to_dict(xml_response)
        return self._safe(dict_response['proposicao'])

    def amendments(self, proposal_type, proposal_number, year):
        """Fetch amendments of a proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            list: A list of amendments of a specific proposal. Example::

                [{'CodProposicao': 413970,
                  'Descricao': 'EMC 2/2008 CSSF => PL 3962/2008'}, ...]

        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?' \
               'tipo={0}&numero={1}&ano={2}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response.encode('utf-8')))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'Emendas'))

    def final_wordings(self, proposal_type, proposal_number, year):
        """Fetch final wordings of a proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            list: A list of final wordings of a specific proposal. Example::

                [{'CodProposicao': 440524,
                  'Descricao': 'RDF 1 => PL 3962/2008''}, ...]

        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?' \
               'tipo={0}&numero={1}&ano={2}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'RedacoesFinais'))

    def substitutives(self, proposal_type, proposal_number, year):
        """Fetch substitutives of a proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            list: A list of substitutives of a specific proposal. Example::

                [{'CodProposicao': 439782,
                  'Descricao': 'SBT 1 CTASP => PL 3962/2008'}]

        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?' \
               'tipo={0}&numero={1}&ano={2}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'Substitutivos'))

    def comissions_opinion(self, proposal_type, proposal_number, year):
        r"""Fetch comissions opinion about a proposal.

        Args:
            proposal_type (str): Proposal type initials.
            proposal_number (int): Proposal number.
            year (int): Proposal's year.

        Returns:
            list: A list of comissions that will examine or was examine
        the proposal. Example::

                [{'dataParecer': datetime.datetime(2009, 6, 24, 10, 0),
                  'inteiroTeorParecerComissao': None,
                  'inteiroTeorParecerRelator':
                    'http://www.camara.gov.br/proposicoesWeb/' \
                    'prop_mostrarintegra?codteor=672715',
                  'parecer': 'Parecer proferido em Plenário pelo Relator, ' \
                             'Dep. Mendes Ribeiro Filho (PMDB-RS), pela ' \
                             'Comissão de Constituição e Justiça e de ' \
                             'Cidadania, que conclui pela ' \
                             'constitucionalidade, juridicidade e técnica ' \
                             legislativa das Emendas de Plenário de nºs ' \
                             1 e 2.',
                  'relator': 'Mendes Ribeiro Filho',
                  'tipoAnalise': 'Constitucionalidade'}, ...]
        """
        path = 'ObterIntegraComissoesRelator?tipo={0}&numero={1}&ano={2}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response.encode('utf-8')))
        dict_response = self._make_dict_from_tree(
            element_tree.find('comissoes')
        )
        list_response = dict_response['comissoes']['comissao']
        if isinstance(list_response, dict):
            list_response = [list_response]

        return self._safe(list_response)

    def types(self):
        """Fetch all proposal types.

        Returns:
            list: A list of proposal types. Example::

                [{'ativa': True,
                  'descricao': 'Voto em Separado',
                  'genero': 'o',
                  'tipoSigla': 'VTS'}, ...]
        """
        xml_response = self._get('ListarSiglasTipoProposicao')
        dict_response = self._xml_attributes_to_list(xml_response, 'sigla')
        return self._safe(dict_response)

    def author_types(self):
        """Fetch all author types.

        Returns:
            list: A list of author types. Example::

                [{'descricao': 'Deputado', 'id': 'TipoParlamentar_10000'}, ...]
        """
        xml_response = self._get('ListarTiposAutores')
        dict_response = self._xml_attributes_to_list(xml_response, 'TipoAutor')
        return self._safe(dict_response)

    def statuses(self):
        """Fetch all proposal statuses.

        Returns:
            list: A list of proposal statuses. Example::

                [{'ativa': True, 'descricao': 'Arquivada', 'id': 923}, ...]
        """
        xml_response = self._get('ListarSituacoesProposicao')
        dict_response = self._xml_attributes_to_list(xml_response,
                                                     'situacaoProposicao')
        return self._safe(dict_response)
