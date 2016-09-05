from pygov_br.base import Client
from pygov_br.exceptions import ClientError
from pygov_br.camara_deputados.deputy import DeputyClient
from xmldict import xml_to_dict
from xml.etree.ElementTree import fromstring, ElementTree


class ProposalClient(Client):

    def __init__(self):
        host = 'http://www.camara.gov.br/SitCamaraWS/Proposicoes.asmx/'
        super(ProposalClient, self).__init__(host)

    def all(self):
        deputy_client = DeputyClient()
        deputies = deputy_client.all()
        proposal_list = []
        for deputy in deputies:
            try:
                proposals = self.get_proposal_by_deputy(
                    deputy['nomeParlamentar'].replace("'", ' '),
                )
                proposal_list.append(proposals)
            except ClientError:
                pass
        return proposal_list[0]

    def all_proposal_by_type(self, proposal_type):
        deputy_client = DeputyClient()
        deputies = deputy_client.all()
        proposal_list = []
        for deputy in deputies:
            try:
                proposals = self.get_proposal_by_deputy(
                    deputy['nomeParlamentar'].replace("'", ' '),
                    proposal_type=proposal_type,
                )
                proposal_list.append(proposals)
            except ClientError:
                pass
        return proposal_list[0]

    def get_proposals(self, number='', deputy_name='', proposal_type='', year='',
                      initial_presentation_date='', final_presentation_date='',
                      legislative_body_id='', author_party='', author_region='',
                      author_gender=''):
        path = 'ListarProposicoes?sigla={}&numero={}&ano={}&' \
               'datApresentacaoIni={}&datApresentacaoFim={}&parteNomeAutor={}&' \
               'idTipoAutor={}&siglaPartidoAutor={}&siglaUFAutor={}&' \
               'generoAutor={}&codEstado=&codOrgaoEstado=&emTramitacao='
        path = path.format(proposal_type, number, year,
                           initial_presentation_date, final_presentation_date,
                           deputy_name, legislative_body_id, author_party,
                           author_region, author_gender)

        print(path.format(path))
        xml_response = self._get(path)
        dict_response = xml_to_dict(xml_response)
        try:
            dict_response = dict_response['proposicoes']['proposicao']
        except KeyError:
            raise ClientError(dict_response['erro']['descricao'])

        if type(dict_response) is dict:
            return [dict_response]

        return dict_response

    def get_by_id(self, proposal_id):
        path = 'ObterProposicaoPorID?IdProp={}'
        xml_response = self._get(path.format(proposal_id))
        element_tree = ElementTree(fromstring(xml_response))
        proposal = element_tree.getroot()

        dict_response = xml_to_dict(fromstring(xml_response), strict=False)
        dict_response = dict_response['proposicao']
        dict_response['tipo'] = proposal.get('tipo')
        dict_response['ano'] = proposal.get('ano')
        dict_response['numero'] = proposal.get('numero')
        return dict_response

    def types(self):
        xml_response = self._get('ListarSiglasTipoProposicao')
        return self._xml_attributes_to_list(xml_response, 'sigla')

    def states(self):
        xml_response = self._get('ListarSituacoesProposicao')
        return self._xml_attributes_to_list(xml_response, 'situacaoProposicao')
