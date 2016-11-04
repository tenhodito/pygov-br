from pygov_br.base import Client
from base64 import b64decode
from xmldict import xml_to_dict
from datetime import datetime


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
            [Mandatory] initial_date: String (dd/mm/yyyy) or datetime
            [Mandatory] final_date: String (dd/mm/yyyy) or datetime
            [Optional] session_id: Integer
            [Optional] parliamentary_name: String
            [Optional] party_initials: String
            [Optional] region: String
        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ListarDiscursosPlenario?dataIni={}&dataFim={}&" \
               "codigoSessao={}&parteNomeParlamentar={}&" \
               "siglaPartido={}&siglaUF={}"
        xml_response = self._get(path.format(
            initial_date, final_date, session_id, parliamentary_name,
            party_initials, region
        ))
        xml_dict = xml_to_dict(xml_response)
        return self._safe(xml_dict['sessoesDiscursos']['sessao'])

    def full_speech(self, session_id, speaker_number, quarter, insertion):
        """
        Returns the full content of a specified speech with the deputy
        informations and datetime from the speech. All parameter can be caught
        with the `speeches` method.

        Parameters:
            [Mandatory] session_id: String
            [Mandatory] speaker_number: Integer
            [Mandatory] quarter: Integer
            [Mandatory] insertion: Integer
        """
        path = "obterInteiroTeorDiscursosPlenario?codSessao={}&numOrador={}&" \
               "numQuarto={}&numInsercao={}"
        xml_response = self._get(path.format(session_id, speaker_number,
                                             quarter, insertion))
        xml_dict = xml_to_dict(xml_response)['sessao']
        xml_dict['discursoRTF'] = b64decode(xml_dict.pop('discursoRTFBase64'))
        return self._safe(xml_dict)

    def frequency(self, session_date, legislature='', deputy_enrollment_id='',
                  party_initials='', region=''):
        """
        List the parliamentary frequency on sessions in specific date.
        Returns a list of sessions that occurred on the specified date and the
        frequency of parliamentarians in each session.

        Parameters:
            [Mandatory] session_date: String (dd/mm/yyyy) or datetime
            [Optional] legislature: Integer
            [Optional] deputy_enrollment_id: Integer
            [Optional] party_initials: String
            [Optional] region: String
        """
        if isinstance(session_date, datetime):
            session_date = session_date.strftime('%d/%m/%Y')

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
