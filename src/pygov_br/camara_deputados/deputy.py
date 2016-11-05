from pygov_br.base import Client
from xml.etree.ElementTree import fromstring, ElementTree
from datetime import datetime
from xmldict import xml_to_dict


class DeputyClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        super(DeputyClient, self).__init__(host)

    def all(self):
        """Fetch all deputies.

        List all deputies acting on Câmara dos Deputados.

        Returns:
            list: A list of deputies. Each deputy is represented as a
            disctionary. For example::

                [{'anexo': 4,
                  'codOrcamento': 2729,
                  'comissoes': {'suplente': None, 'titular': None},
                  'condicao': 'Suplente',
                  'email': 'dep.rosinhadaadefal@camara.gov.br',
                  'fone': '3215-5412',
                  'gabinete': 412,
                  'idParlamentar': 5830905,
                  'ideCadastro': 146949,
                  'matricula': 586,
                  'nome': 'ROSEANE CAVALCANTE DE FREITAS',
                  'nomeParlamentar': 'ROSINHA DA ADEFAL',
                  'partido': 'PTdoB',
                  'sexo': 'feminino',
                  'uf': 'AL',
                  'urlFoto': 'http://www.camara.gov.br/internet/deputado/' \
                             'bandep/146949.jpg'}, ...]
        """
        xml_response = self._get('ObterDeputados')
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['deputados']['deputado'])

    def details(self, deputy_id, legislature=''):
        """Fetch detailed information about a specific deputy.

        List detailed information about a specific deputy.

        Args:
            deputy_id (int): Deputy identifier.
            lesgislature (int, optional): To specify an legislature.
                Defaults to ''.

        Returns:
            list: A list of dictionaries containing extra information about
            the deputy. Each dictionary represents one legislative period. For
            example::

                [{'cargosComissoes': None,
                  'comissoes': {'comissao': {'condicaoMembro': 'Titular',
                    'dataEntrada': datetime.date(2016, 10, 25),
                    'dataSaida': None,
                    'idOrgaoLegislativoCD': 537480,
                    'nomeComissao': 'Comissão de Defesa dos Direitos das ' \
                                    'Pessoas com Deficiência',
                    'siglaComissao': 'CPD'}},
                  'dataFalecimento': None,
                  'dataNascimento': datetime.date(1973, 4, 22),
                  'email': 'dep.rosinhadaadefal@camara.gov.br',
                  'filiacoesPartidarias': None,
                  'gabinete': {'anexo': 4, 'numero': 412,
                               'telefone': '3215-5412'},
                  'historicoLider': None,
                  'historicoNomeParlamentar': None,
                  'idParlamentarDeprecated': 10007,
                  'ideCadastro': 146949,
                  'nomeCivil': 'ROSEANE CAVALCANTE DE FREITAS',
                  'nomeParlamentarAtual': 'ROSINHA DA ADEFAL',
                  'nomeProfissao': 'Funcionário Público Federal',
                  'numLegislatura': 55,
                  'partidoAtual': {'idPartido': 'PTdoB',
                   'nome': 'Partido Trabalhista do Brasil',
                   'sigla': 'PTdoB'},
                  'periodosExercicio': {'periodoExercicio': {'dataFim': None,
                    'dataInicio': datetime.date(2016, 10, 17),
                    'descricaoCausaFimExercicio': None,
                    'idCadastroParlamentarAnterior': 178843,
                    'idCausaFimExercicio': None,
                    'siglaUFRepresentacao': 'AL',
                    'situacaoExercicio': 'Suplente'}},
                  'sexo': False,
                  'situacaoNaLegislaturaAtual': 'Em Exercício',
                  'ufRepresentacaoAtual': 'AL'}, ...]

        """
        path = 'ObterDetalhesDeputado?ideCadastro={}&numLegislatura={}'
        xml_response = self._get(path.format(deputy_id, legislature))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['Deputados']['Deputado'])

    def parties(self):
        """Fetch all parties.

        List all parties with representation on Câmara dos Deputados.

        Returns:
            list: A list of dictionaries containing the information about the
            parties. For example::

                [{'dataCriacao': None,
                  'dataExtincao': datetime.date(1950, 1, 1),
                  'idPartido': 'USDH',
                  'nomePartido': 'União Social pelos Direitos do Homem',
                  'siglaPartido': 'USDH'}, ...]

        """
        xml_response = self._get('ObterPartidosCD')
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['partidos']['partido'])

    def parties_bloc(self, bloc_id='', legislature=''):
        """Fetch all parties bloc.

        List all parties blocs or filtering by legislature and id.

        Args:
            bloc_id (int): Parties bloc identifier. Optional.
            lesgislature (int, optional): To specify an legislature.
                Defaults to ''.

        Returns:
            list: A list of dictionaries containing bloc information and a list
            of parties that belongs to the bloc. For example::

                [{'Partidos': {'partido': [
                     {'dataAdesaoPartido': datetime.date(2011, 2, 1),
                      'dataDesligamentoPartido': datetime.date(2013, 10, 16),
                      'idPartido': 'PHS',
                      'nomePartido': 'Partido Humanista da Solidariedade',
                      'siglaPartido': 'PHS'}, ...]
                  'dataCriacaoBloco': datetime.date(2011, 2, 1),
                  'dataExtincaoBloco': datetime.date(2015, 1, 31),
                  'idBloco': 9,
                  'nomeBloco': 'PR, PTdoB, PRP',
                  'siglaBloco': 'PR, PTdoB, PRP'}, ...]

        """
        path = 'ObterPartidosBlocoCD?numLegislatura={}&idBloco={}'
        xml_response = self._get(path.format(legislature, bloc_id))
        dict_response = xml_to_dict(xml_response)
        return self._safe(dict_response['blocos']['bloco'])

    def parliamentary_seats(self):
        """Fetch all parliamentary seats.

        Returns:
            list: A list of dictionaries containing the information about
            parliamentaries seats. For example::

                [{'nome': 'Partido Social Liberal', 'sigla': 'PSL'}, ...]

        """
        xml_response = self._get('ObterLideresBancadas')
        list_response = self._xml_attributes_to_list(xml_response, 'bancada')
        return self._safe(list_response)

    def parliamentary_seat_leaders(self, seat_initials):
        """Fetch parliamentary seat leaders.
        List all leaders and vice-leaders of a specific paliamentary seat.

        Args:
            seat_initials (str): Parliamentary seat initials identifier.

        Returns:
            dict: A dictionary with two keys: 'lider' and 'vice_lider', where
            'lider' is a dictionary and 'vice_lider' a list of dictionaries.
            Both dictionaries contains deputies informations. For example::

                {'lider': {'ideCadastro': 74558,
                           'nome': 'GIVALDO CARIMBÃO',
                           'partido': 'PHS',
                           'uf': 'AL'},
                 'vice_lider': [{'ideCadastro': 178929,
                                 'nome': 'DIEGO GARCIA',
                                 'partido': 'PHS',
                                 'uf': 'PR'}, ...]}

        """
        xml_response = self._get('ObterLideresBancadas')
        element_tree = ElementTree(fromstring(xml_response))
        parliamentary_seat = element_tree.find(
            "bancada[@sigla='{}']".format(seat_initials)
        )
        dict_response = self._make_dict_from_tree(parliamentary_seat)
        return self._safe(dict_response['bancada'])

    def frequency(self, initial_date, final_date, parliamentary_enrollment):
        """Fetch parliamentary frequency.

        List the frequency of a parliamentary in a period.

        Args:
            initial_date (str or datetime): Initial date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            final_date (str or datetime): Final date of period. If `str`,
                must be in the format: `dd/mm/yyyy`.
            parliamentary_enrollment (int): Parliamentary enrollment number.

        Returns:
            list: A list of sessions that occurred on the specified period and
            the frequency of parliamentarians in each session. For example::

                [{'data': datetime.date(2012, 11, 20),
                  'qtdeSessoes': 3,
                  'sessoes': {'sessao': [{
                      'descricao': 'ORDINÁRIA Nº 313 - 20/11/2012',
                     'frequencia': 'Presença'}, ...]},
                  'frequencianoDia': 'Presença',
                  'justificativa': None} ...]

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
