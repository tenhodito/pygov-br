# -*- coding: utf-8 -*-
from pygov_br.base import Client
from datetime import datetime
from xml.etree.ElementTree import fromstring, ElementTree


class LegislativeBodyClient(Client):

    def __init__(self):
        host = 'http://www.camara.leg.br/SitCamaraWS/Orgaos.asmx/'
        super(LegislativeBodyClient, self).__init__(host)

    def all(self):
        """Fetch all legislative bodies.

        List all legislative bodies on Câmara dos Deputados.

        Returns:
            list: A list of all legislative bodies of Câmara dos Deputados
            (commissions, councils, etc). For example::

                [{'descricao': 'Comissão de Constituição e Justiça ' \
                               'e de Cidadania',
                  'id': 2003,
                  'idTipodeOrgao': 2,
                  'sigla': 'CCJC'}, ...]

        """
        xml_response = self._get('ObterOrgaos')
        list_response = self._xml_attributes_to_list(xml_response, 'orgao')
        return self._safe(list_response)

    def roles(self):
        """Fetch all legislative bodies roles.

        Returns:
            list: A list of all legislative bodies roles. For example::

            [{'descricao': 'Relator', 'id': 50}, ...]

        """
        xml_response = self._get('ListarCargosOrgaosLegislativosCD')
        list_response = self._xml_attributes_to_list(xml_response, 'cargo')
        return self._safe(list_response)

    def members(self, legislative_body_id):
        """Fetch members of a legislative body.

        Args:
            legislative_body_id (int): Legisltive body identifier.

        Returns:
            dict: A dictionary that contains 'membro', 'Presidente',
            'PrimeiroVice-Presidente', 'SegundoVice-Presidente' and
            'TerceiroVice-Presidente' as keys. The last three have a deputy
            dictionary as value and the first have a list of deputy dictionary.
            For example::

                    {'Presidente': {'ideCadastro': 73463,
                      'nome': 'Osmar Serraglio',
                      'partido': 'PMDB',
                      'situacao': 'Titular',
                      'uf': 'PR'},
                     'PrimeiroVice-Presidente': {'ideCadastro': 178897,
                      'nome': 'Rodrigo Pacheco',
                      'partido': 'PMDB',
                      'situacao': 'Titular',
                      'uf': 'MG'},
                     'SegundoVice-Presidente': {'ideCadastro': 93472,
                      'nome': 'Cristiane Brasil',
                      'partido': 'PTB',
                      'situacao': 'Titular',
                      'uf': 'RJ'},
                     'TerceiroVice-Presidente': {'ideCadastro': 178963,
                      'nome': 'Covatti Filho',
                      'partido': 'PP',
                      'situacao': 'Titular',
                      'uf': 'RS'},
                     'membro': [{'ideCadastro': 160559,
                       'nome': 'Alceu Moreira',
                       'partido': 'PMDB',
                       'situacao': 'Titular',
                       'uf': 'RS'}, ...]}

        """
        path = 'ObterMembrosOrgao?IDOrgao={0}'
        xml_response = self._get(path.format(legislative_body_id))
        element_tree = ElementTree(fromstring(xml_response))
        members = element_tree.find('membros')
        dict_response = self._make_dict_from_tree(members)
        return self._safe(dict_response['membros'])

    def schedule(self, legislative_body_id, initial_date='', final_date=''):
        """Fetch all scheduled activities of a legislative body.

        Args:
            legislative_body_id (int): Legisltive body identifier.
            initial_date (str or datetime, optional): Initial date of period.
                If `str`, must be in the format: `dd/mm/yyyy`.
            final_date (str or datetime, optional): Final date of period.
                If `str`, must be in the format: `dd/mm/yyyy`.

        Returns:
            list: A list with all scheduled activities of a legislative body.
            For example::

                [{'codReuniao': 45639,
                  'comissao': 'CCJC - CONSTITUIÇÃO E JUSTIÇA E DE CIDADANIA',
                  'data': datetime.date(2016, 11, 10),
                  'estado': 'Convocada',
                  'horario': datetime.time(10, 0),
                  'local': 'Anexo II, Plenário 01',
                  'objeto': None,
                  'proposicoes': {'proposicao': [{
                    'ementa': 'Altera a Lei nº 9.472, de 16 de julho de 1997' \
                              ' permitindo à Anatel alterar a modalidade de ' \
                              'licenciamento de serviço de telecomunicações ' \
                              'de concessão para autorização.',
                    'idProposicao': 2025543,
                    'numOrdemApreciacao': 113,
                    'partidoRelator': 'PMDB',
                    'relator': 'Deputado Sergio Souza',
                    'resultado': None,
                    'sigla': 'PL 3453/2015',
                    'textoParecerRelator':
                        'Parecer do Relator, Dep. Sergio Souza (PMDB-PR), ' \
                        'pela constitucionalidade, juridicidade e técnica ' \
                        'legislativa deste, das Emendas da Comissão de ' \
                        'Ciência e Tecnologia, Comunicação e Informática e ' \
                        do Substitutivo da Comissão de Desenvolvimento ' \
                        Econômico, Indústria, Comércio e Serviços.',
                    'ufRelator': 'PR'}, ...]},
                  'tipo': 'Reunião Deliberativa',
                  'tituloReuniao': 'Reunião Deliberativa Ordinária'},

        """
        if isinstance(initial_date, datetime):
            initial_date = initial_date.strftime('%d/%m/%Y')
        if isinstance(final_date, datetime):
            final_date = final_date.strftime('%d/%m/%Y')

        path = "ObterPauta?IDOrgao={0}&datIni={1}&datFim={2}"
        xml_response = self._get(path.format(legislative_body_id,
                                             initial_date, final_date))
        dict_response = self._xml_to_dict(xml_response)
        return self._safe(dict_response['pauta']['reuniao'])

    def types(self):
        """Fetch all legislative bodies types.

        Returns:
            list: A list of all legislative bodies types. For example::

            [{'descricao': 'Sociedade Civil', 'id': 70000}, ...]

        """
        xml_response = self._get('ListarTiposOrgaos')
        list_response = self._xml_attributes_to_list(xml_response, 'tipoOrgao')
        return self._safe(list_response)

