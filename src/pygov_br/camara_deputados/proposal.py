from pygov_br.base import Client
from pygov_br.exceptions import MissingParameterError
from xmldict import xml_to_dict
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
        """
        Returns a list of the filtered proposals. The 'proposal_type' and
        'year' parameters are mandatory if 'author_name' is empty.

        Raises MissingParameterError when 'author_name' is empty AND
        'proposal_type' OR 'year' OR both are empty too.

        Raises ValueError when:
        - 'author_gender' is not 'M' or 'F'
        - 'in_progress' is not '1' or '2'

        Parameters:
            [Mandatory *] proposal_type: String
            [Mandatory *] year: Integer
            [Mandatory *] author_name: String
            [Optional] proposal_number: Integer
            [Optional] initial_date: String (dd/mm/yyyy) or datetime
            [Optional] final_date: String (dd/mm/yyyy) or datetime
            [Optional] author_type_id: Integer
            [Optional] author_party_initials: String
            [Optional] author_region: String
            [Optional] author_gender: String ('M' or 'F')
            [Optional] status_id: Integer
            [Optional] legislative_body_id: Integer
            [Optional] in_progress: Integer ('1' or '2')

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

        path = "ListarProposicoes?sigla={}&numero={}&ano={}&" \
               "datApresentacaoIni={}&datApresentacaoFim={}&" \
               "parteNomeAutor={}&idTipoAutor={}&siglaPartidoAutor={}&" \
               "siglaUFAutor={}&generoAutor={}&codEstado={}&" \
               "codOrgaoEstado={}&emTramitacao={}"
        xml_response = self._get(path.format(
            proposal_type, proposal_number, year, initial_date, final_date,
            author_name, author_type_id, author_party_initials, author_region,
            author_gender, status_id, legislative_body_id, in_progress
        ))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['proposicoes']['proposicao'])

    def get(self, proposal_type, proposal_number, year):
        """
        Returns a detailed information about one proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = "ObterProposicao?tipo={}&numero={}&ano={}"
        xml_response = self._get(path.format(proposal_type, proposal_number,
                                             year))
        element_tree = ElementTree(fromstring(xml_response))
        dict_response = self._make_dict_from_tree(element_tree.getroot())
        return self._safe(dict_response['proposicao'])

    def get_by_id(self, proposal_id):
        """
        Returns a detailed information about one proposal.

        Parameters:
            [Mandatory] proposal_id: Integer
        """
        path = "ObterProposicaoPorID?IdProp={}"
        xml_response = self._get(path.format(proposal_id))
        element_tree = ElementTree(fromstring(xml_response))
        dict_response = self._make_dict_from_tree(element_tree.getroot())
        return self._safe(dict_response['proposicao'])

    def voting(self, proposal_type, proposal_number, year):
        """
        Returns a voting list of a specified proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = "ObterVotacaoProposicao?tipo={}&numero={}&ano={}"
        xml_response = self._get(path.format(proposal_type, proposal_number,
                                             year))
        element_tree = ElementTree(fromstring(xml_response))

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
        """
        Returns a list of proposal that was voted in the year.

        Parameters:
            [Mandatory] year: Integer
            [Optional] proposal_type: String
        """
        path = 'ListarProposicoesVotadasEmPlenario?ano={}&tipo={}'
        xml_response = self._get(path.format(year, proposal_type))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['proposicoes']['proposicao'])

    def processed_in_period(self, initial_date, final_date):
        """
        Returns a list of proposal that was processed in the period.

        Parameters:
            [Mandatory] initial_date: String (dd/mm/yyyy) or datetime
            [Mandatory] final_date: String (dd/mm/yyyy) or datetime
        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = 'ListarProposicoesTramitadasNoPeriodo?dtInicio={}&dtFim={}'
        xml_response = self._get(path.format(initial_date, final_date))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['proposicoes']['proposicao'])

    def progress(self, proposal_number, year, proposal_type='',
                 initial_date='', legislative_body_id=''):
        """
        Returns a list of progress steps of a proposal.

        Parameters:
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
            [Optional] proposal_type: String
            [Optional] initial_date: String (dd/mm/yyyy) or datetime
            [Optional] legislative_body_id: Integer
        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')

        path = 'ObterAndamento?sigla={}&numero={}&ano={}&' \
               'dataIni={}&codOrgao={}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year,
                        initial_date, legislative_body_id),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['proposicao'])

    def amendments(self, proposal_type, proposal_number, year):
        """
        Returns a list of amendments of a specific proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?tipo={}&numero={}&ano={}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'Emendas'))

    def final_wordings(self, proposal_type, proposal_number, year):
        """
        Returns a list of final wordings of a specific proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?tipo={}&numero={}&ano={}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'RedacoesFinais'))

    def substitutives(self, proposal_type, proposal_number, year):
        """
        Returns a list of substitutives of a specific proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = 'ObterEmendasSubstitutivoRedacaoFinal?tipo={}&numero={}&ano={}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))

        return self._safe(self._tree_attributes_to_list(element_tree,
                                                        'Substitutivos'))

    def comissions_opinion(self, proposal_type, proposal_number, year):
        """
        Returns a list of comissions that will examine or was examine
        the proposal.

        Parameters:
            [Mandatory] proposal_type: String
            [Mandatory] proposal_number: Integer
            [Mandatory] year: Integer
        """
        path = 'ObterIntegraComissoesRelator?tipo={}&numero={}&ano={}'
        xml_response = self._get(
            path.format(proposal_type, proposal_number, year),
            host='http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/')
        element_tree = ElementTree(fromstring(xml_response))
        dict_response = self._make_dict_from_tree(
            element_tree.find('comissoes')
        )

        return self._safe(dict_response['comissoes']['comissao'])

    def types(self):
        """
        Returns a list of proposal types.

        Parameters:
            None
        """
        xml_response = self._get('ListarSiglasTipoProposicao')
        dict_response = self._xml_attributes_to_list(xml_response, 'sigla')
        return self._safe(dict_response)

    def author_types(self):
        """
        Returns a list of proposal author types.

        Parameters:
            None
        """
        xml_response = self._get('ListarTiposAutores')
        dict_response = self._xml_attributes_to_list(xml_response, 'TipoAutor')
        return self._safe(dict_response)

    def statuses(self):
        """
        Returns a list of proposal statuses.

        Parameters:
            None
        """
        xml_response = self._get('ListarSituacoesProposicao')
        dict_response = self._xml_attributes_to_list(xml_response,
                                                     'situacaoProposicao')
        return self._safe(dict_response)
