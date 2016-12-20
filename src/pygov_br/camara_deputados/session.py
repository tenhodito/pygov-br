# -*- coding: utf-8 -*-
from pygov_br.base import Client
from pygov_br.vendor.pyth.plugins.rtf15.reader import Rtf15Reader
from pygov_br.vendor.pyth.plugins.xhtml.writer import XHTMLWriter
from base64 import b64decode
from datetime import datetime
from bs4 import BeautifulSoup
from tempfile import TemporaryFile


class SessionClient(Client):

    def __init__(self):
        host = 'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        super(SessionClient, self).__init__(host)

    def speeches(self, initial_date, final_date, session_id='',
                 parliamentary_name='', party_initials='', region=''):
        """Fetch all speeches in a period.

        Args:
            initial_date (str or datetime): Initial date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            final_date (str or datetime): Final date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            session_id (int, optional): Session identifier. Defaults to ''.
            parliamentary_name (str, optional): A parliamentary name. Defaults
                to ''.
            party_initials (str, optional): Party identifier initials. Defaults
                to ''.
            region (str, optional): Brazilian region identifier initials.
                Defaults to ''.

        Returns:
            list: A list of sessions that contains speeches made by deputies on
            Plenary of Câmara dos Deputados in a specific period. For example::

                [{'codigo': '320.2.54.O',
                  'data': datetime.date(2012, 11, 23),
                  'fasesSessao': {'faseSessao': {'codigo': 'PE',
                    'descricao': 'Pequeno Expediente',
                    'discursos': {'discurso': [{
                       'horaInicioDiscurso':
                            datetime.datetime(2012, 11, 23, 9, 18),
                       'numeroInsercao': 0,
                       'numeroQuarto': 3,
                       'orador': {'nome': 'MAURO BENEVIDES',
                        'numero': 2,
                        'partido': 'PMDB',
                        'uf': 'CE'},
                       'sumario': 'Presença da Presidenta Dilma Rousseff em ' \
                                  'Fortaleza, Estado do Ceará, para a ' \
                                  'inauguração do novo Estádio Castelão e da' \
                                  'Zona de Processamento de Exportação - ZPE' \
                                  'Liberação da área destinada à construção ' \
                                  'da Refinaria Premium II no Estado pela '\
                                  'PETROBRAS.',
                       'txtIndexacao': 'ESTÁDIO, FUTEBOL, CIDADE, FORTALEZA,' \
                                       'CE, INAUGURAÇÃO, PRESENÇA, DILMA ' \
                                       'ROUSSEFF, PRESIDENTE DA REPÚBLICA, ' \
                                       CONFIRMAÇÃO, APOIO.'},
                  'numero': 2,
                  'tipo': 'Ordinária - CD'}, ...]

        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ListarDiscursosPlenario?dataIni={0}&dataFim={1}&" \
               "codigoSessao={2}&parteNomeParlamentar={3}&" \
               "siglaPartido={4}&siglaUF={5}"
        xml_response = self._get(path.format(
            initial_date, final_date, session_id, parliamentary_name,
            party_initials, region
        ))
        xml_dict = self._xml_to_dict(xml_response)
        list_response = xml_dict['sessoesDiscursos']['sessao']

        if isinstance(list_response, dict):
            list_response = [list_response]

        return self._safe(list_response)

    def full_speech(self, session_id, speaker_number, quarter, insertion):
        """Fetch full content of a speech.

        All parameter can be caught with the `speeches` method.

        Args:
            session_id (str): Session identifier.
            speaker_number (int): Speaker identifier.
            quarter (int): Shorthand fraction number that identifies the
                beginning of the speech.
            insertion (int): Shorthand insertion number that identifies the
                beginning of the speech.

        Returns:
            dict: The full content of a specified speech with the deputy
            informations and datetime from the speech.

            'DiscursoRTF' key is a byte string that contains the full speech in
            Rich Text Format.

            Example::

                {'discursoRTF': b"{\\rtf1\\ansi\\ansicpg1252\\deff0" \
                                 "\\deflang1046\\deflangfe1046\\deftab709" \
                                 "{\\fonttbl{\\f0\\fswiss\\fprq2\\fcharset0 " \
                                 "Arial;}}\r\n\\viewkind4\\uc1\\pard\\sl480" \
                                 "\\slmult1\\qj\\f0\\fs24\\tab\\b O SR. " \
                                 "DUDIMAR PAXIUBA \\b0 (PSDB-PA. Sem " \
                                 "revis\\'e3o do orador.) - Sr. Presidente, "\
                                 "Sras. e Srs. Parlamentares, ocupo esta " \
                                 "tribuna para parabenizar a torcida " ... },
                 'horaInicioDiscurso': datetime.datetime(2013, 3, 4, 14, 33),
                 'nome': 'DUDIMAR PAXIUBA',
                 'partido': 'PSDB',
                 'uf': 'PA'}

        """
        path = "obterInteiroTeorDiscursosPlenario?codSessao={0}" \
               "&numOrador={1}&numQuarto={2}&numInsercao={3}"
        xml_response = self._get(path.format(session_id, speaker_number,
                                             quarter, insertion))
        xml_dict = self._xml_to_dict(xml_response)['sessao']
        speech = b64decode(xml_dict.pop('discursoRTFBase64'))
        xml_dict['discurso'] = self._extract_text_from_rtf(speech)
        return self._safe(xml_dict)

    def _extract_text_from_rtf(self, rtf_text):
        try:
            temp_file = TemporaryFile()
            temp_file.write(rtf_text)
            doc = Rtf15Reader.read(temp_file)
            html = XHTMLWriter.write(doc, pretty=True).read()
            cleantext = BeautifulSoup(html, "html.parser").text.strip()
            return cleantext
        except (UnicodeDecodeError, TypeError):
            return None

    def frequency(self, session_date, legislature='', deputy_enrollment_id='',
                  party_initials='', region=''):
        """Fetch sessions ferquency.

        List the parliamentary frequency on sessions in specific date.

        Args:
            session_date (str or datetime): Initial date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            lesgislature (int, optional): To specify an legislature. Defaults
                to ''.
            deputy_enrollment_id (int, optional): Deputy enrollment identifier.
                Defaults to ''.
            party_initials (str, optional): Party identifier initials. Defaults
                to ''.
            region (str, optional): Brazilian region identifier initials.
                Defaults to ''.

        Returns:
            dict: Returns a dict with all session that occurred in the
            specified date and the frequency of parliamentarians in each
            session. For example::

                {'data': datetime.date(2012, 4, 10),
                 'legislatura': 54,
                 'parlamentares': {'parlamentar': {'carteiraParlamentar': 1,
                   'descricaoFrequenciaDia': 'Presença',
                   'justificativa': None,
                   'nomeParlamentar': 'Berinho Bantim-PSDB/RR',
                   'presencaExterna': 0,
                   'sessoesDia': {'sessaoDia': [{
                      'descricao': 'ORDINÁRIA Nº 073 - 10/04/2012',
                      'frequencia': 'Presença',
                      'inicio': datetime.datetime(2012, 4, 10, 14, 0, 14)},
                     {'descricao': 'EXTRAORDINÁRIA Nº 074 - 10/04/2012',
                      'frequencia': 'Presença',
                      'inicio': datetime.datetime(2012, 4, 10, 18, 46, 53)
                      }, ...]},
                   'siglaPartido': 'PSDB',
                   'siglaUF': 'RR'}, ...},
                 'qtdeSessoesDia': 2}

        """
        if isinstance(session_date, datetime):
            session_date = session_date.strftime('%d/%m/%Y')

        path = "ListarPresencasDia?data={0}&numLegislatura={1}&" \
               "numMatriculaParlamentar={2}&siglaPartido={3}&siglaUF={4}"
        xml_response = self._get(path.format(
            session_date, legislature, deputy_enrollment_id,
            party_initials, region
        ))
        xml_dict = self._xml_to_dict(xml_response)
        return self._safe(xml_dict['dia'])

    def status(self):
        """Fetch all status for comissions and sessions.

        Returns:
            list: A list of possible situations for commissions and sessions.
            For example::

                [{'descricao': 'Encerrada(Comunicado)', 'id': 9}, ...]

        """
        xml_response = self._get('ListarSituacoesReuniaoSessao')
        list_response = self._xml_attributes_to_list(xml_response,
                                                     'situacaoReuniao')
        return self._safe(list_response)
