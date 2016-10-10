from pygov_br.base import Client
from pygov_br.camara_deputados.proposal import ProposalClient
from xml.etree.ElementTree import fromstring, ElementTree
from xmldict import xml_to_dict


class SessionClient(Client):

    def __init__(self):
        host = 'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        super(SessionClient, self).__init__(host)

    def speeches(self, initial_date, final_date, session_id='',
                 parliamentary_name='', party_initials='', region=''):
        """
        List all speeches in a period.
        Returns a list of deputies that made speeches on Plenary of Câmara dos
        Deputados in a specific period.

        Parameters:
            [Mandatory] initial_date: String (dd/mm/yyy)
            [Mandatory] final_date: String (dd/mm/yyy)
            [Optional] session_id: Integer
            [Optional] parliamentary_name: String
            [Optional] party_initials: String
            [Optional] region: String
        """
        path = "ListarDiscursosPlenario?dataIni={}&dataFim={}&" \
               "codigoSessao={}&parteNomeParlamentar={}&" \
               "siglaPartido={}&siglaUF={}"
        xml_response = self._get(path.format(
            initial_date, final_date, session_id, parliamentary_name,
            party_initials, region
        ))
        xml_dict = xml_to_dict(xml_response)
        return self._safe(xml_dict['sessoesDiscursos']['sessao'])

    def frequency(self, session_date, legislature='', deputy_enrollment_id='',
                  party_initials='', region=''):
        """
        List the parliamentary frequency on sessions in specific date.
        Returns a list of sessions that occurred on the specified date and the
        frequency of parliamentarians in each session.

        Parameters:
            [Mandatory] session_date: String (dd/mm/yyyy)
            [Optional] legislature: Integer
            [Optional] deputy_enrollment_id: Integer
            [Optional] party_initials: String
            [Optional] region: String
        """
        path = "ListarPresencasDia?data={}&numLegislatura={}&" \
               "numMatriculaParlamentar={}&siglaPartido={}&siglaUF={}"
        xml_response = self._get(path.format(
            session_date, legislature, deputy_enrollment_id,
            party_initials, region
        ))
        xml_dict = xml_to_dict(xml_response)
        return self._safe(xml_dict['dia'])

    def status(self):
        """
        Returns a list of possible situations for commissions and sessions.

        Parameters:
            None
        """
        xml_response = self._get('ListarSituacoesReuniaoSessao')
        list_response = self._xml_attributes_to_list(xml_response,
                                                     'situacaoReuniao')
        return self._safe(list_response)
