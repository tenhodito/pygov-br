from pygov_br.base import Client
from xml.etree.ElementTree import fromstring, ElementTree
from datetime import datetime
from xmldict import xml_to_dict


class DeputyClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        super(DeputyClient, self).__init__(host)

    def all(self):
        """
        List all deputies acting on Câmara dos Deputados.
        Returns a list of dictionaries containing the information about the
        deputies.

        Parameters:
            None
        """
        xml_response = self._get('ObterDeputados')
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['deputados']['deputado'])

    def details(self, deputy_id, legislature=''):
        """
        List detailed information about a specific deputy.
        Returns a list of dictionaries containing extra information about
        the deputy. Each dictionary represents one legislative period.

        Parameters:
            [Mandatory] deputy_id: Integer
            [Optional] lesgislature: Integer
        """
        path = 'ObterDetalhesDeputado?ideCadastro={}&numLegislatura={}'
        xml_response = self._get(path.format(deputy_id, legislature))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['Deputados']['Deputado'])

    def parties(self):
        """
        List all parties with representation on Câmara dos Deputados.
        Returns a list of dictionaries containing the information about the
        parties.

        Parameters:
            None
        """
        xml_response = self._get('ObterPartidosCD')
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['partidos']['partido'])

    def parties_bloc(self, bloc_id='', legislature=''):
        """
        List all parties blocs or filtering by legislature and id.
        Returns a list of dictionaries containing bloc information and a list
        of parties that belongs to the bloc.

        Parameters:
            [Optional] bloc_id: Integer
            [Optional] legislature: Integer
        """
        path = 'ObterPartidosBlocoCD?numLegislatura={}&idBloco={}'
        xml_response = self._get(path.format(legislature, bloc_id))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['blocos']['bloco'])

    def parliamentary_seats(self):
        """
        List all paliamentary seats.
        Returns a list of dictionaries containing the information about
        parliamentaries seats.

        Parameters:
            None
        """
        xml_response = self._get('ObterLideresBancadas')
        list_response = self._xml_attributes_to_list(xml_response, 'bancada')
        return self._safe(list_response)

    def parliamentary_seat_leaders(self, seat_initials):
        """
        List all leaders and vice-leaders of a specific paliamentary seat.
        Returns a dictionary with two keys: 'lider' and 'vice_lider', where
        'lider' is a dictionary and 'vice_lider' a list of dictionaries.
        Both dictionaries contains deputies informations.

        Parameters:
            [Mandatory] seat_initials: String
        """
        xml_response = self._get('ObterLideresBancadas')
        element_tree = ElementTree(fromstring(xml_response))
        parliamentary_seat = element_tree.find(
            "bancada[@sigla='{}']".format(seat_initials)
        )
        dict_response = self._make_dict_from_tree(parliamentary_seat)
        return self._safe(dict_response['bancada'])

    def frequency(self, initial_date, final_date, parliamentary_enrollment):
        """
        List the frequency of a parliamentary in a period.
        Returns a list of sessions that occurred on the specified period and
        the frequency of parliamentarians in each session.

        Parameters:
            [Mandatory] initial_date: String (dd/mm/yyyy) or datetime
            [Mandatory] final_date: String (dd/mm/yyyy) or datetime
            [Mandatory] parliamentary_enrollment: Integer
        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ListarPresencasParlamentar?dataIni={}&dataFim={}&" \
               "numMatriculaParlamentar={}"
        xml_response = self._get(
            path.format(initial_date, final_date, parliamentary_enrollment),
            host="http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/"
        )
        dict_response = xml_to_dict(xml_response)
        return self._safe(
            dict_response['parlamentar']['diasDeSessoes2']['dia']
        )
