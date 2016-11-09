from pygov_br.camara_deputados import cd
import datetime
import responses


@responses.activate
def test_deputy_all():
    xml_response = """
    <deputados>
        <deputado>
            <ideCadastro>74784</ideCadastro>
            <comissoes>
                <titular/>
                <suplente/>
            </comissoes>
        </deputado>
        <deputado>
            <ideCadastro>152610</ideCadastro>
            <comissoes>
                <titular/>
                <suplente/>
            </comissoes>
        </deputado>
    </deputados>
    """
    expected_list = [
        {'ideCadastro': 74784,
         'comissoes': {'titular': None, 'suplente': None}},
        {'ideCadastro': 152610,
         'comissoes': {'titular': None, 'suplente': None}}
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterDeputados',
        body=xml_response, status=200)
    assert cd.deputies.all() == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_details():
    xml_response = """
    <Deputados>
        <Deputado>
            <numLegislatura>53</numLegislatura>
            <partidoAtual>
                <sigla>PSD</sigla>
            </partidoAtual>
            <comissoes>
                <comissao>
                    <siglaComissao>CEREFPOL</siglaComissao>
                </comissao>
            </comissoes>
            <cargosComissoes>
                <cargoComissoes>
                    <siglaComissao>MESA</siglaComissao>
                </cargoComissoes>
            </cargosComissoes>
            <periodosExercicio>
                <periodoExercicio>
                    <siglaUFRepresentacao>RN</siglaUFRepresentacao>
                </periodoExercicio>
            </periodosExercicio>
            <historicoLider>
                <itemHistoricoLider>
                    <idHistoricoLider>141428</idHistoricoLider>
                </itemHistoricoLider>
            </historicoLider>
        </Deputado>
        <Deputado>
            <numLegislatura>54</numLegislatura>
            <partidoAtual>
                <sigla>PSD</sigla>
            </partidoAtual>
            <comissoes>
                <comissao>
                    <siglaComissao>CEREFPOL</siglaComissao>
                </comissao>
            </comissoes>
            <cargosComissoes>
                <cargoComissoes>
                    <siglaComissao>MESA</siglaComissao>
                </cargoComissoes>
            </cargosComissoes>
            <periodosExercicio>
                <periodoExercicio>
                    <siglaUFRepresentacao>RN</siglaUFRepresentacao>
                </periodoExercicio>
            </periodosExercicio>
            <historicoLider>
                <itemHistoricoLider>
                    <idHistoricoLider>141428</idHistoricoLider>
                </itemHistoricoLider>
            </historicoLider>
        </Deputado>
    </Deputados>
    """
    expected_list = [
        {'numLegislatura': 53,
         'partidoAtual': {'sigla': 'PSD'},
         'comissoes': {'comissao': {'siglaComissao': 'CEREFPOL'}},
         'cargosComissoes': {'cargoComissoes': {'siglaComissao': 'MESA'}},
         'periodosExercicio': {
             'periodoExercicio': {'siglaUFRepresentacao': 'RN'}},
         'historicoLider': {'itemHistoricoLider': {
             'idHistoricoLider': 141428}}},
        {'numLegislatura': 54,
         'partidoAtual': {'sigla': 'PSD'},
         'comissoes': {'comissao': {'siglaComissao': 'CEREFPOL'}},
         'cargosComissoes': {'cargoComissoes': {'siglaComissao': 'MESA'}},
         'periodosExercicio': {
             'periodoExercicio': {'siglaUFRepresentacao': 'RN'}},
         'historicoLider': {'itemHistoricoLider': {
             'idHistoricoLider': 141428}}},
    ]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        'ObterDetalhesDeputado',
        body=xml_response, status=200)
    assert cd.deputies.details(141428) == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_parties():
    xml_response = """
    <partidos>
        <partido>
            <idPartido>ADB</idPartido>
        </partido>
        <partido>
            <idPartido>AIB</idPartido>
        </partido>
    </partidos>
    """
    expected_list = [{'idPartido': 'ADB'}, {'idPartido': 'AIB'}]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/ObterPartidosCD',
        body=xml_response, status=200)
    assert cd.deputies.parties() == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_parties_bloc():
    xml_response = """
    <blocos>
        <bloco>
            <nomeBloco>PV, PPS</nomeBloco>
            <Partidos>
                <partido>
                    <idPartido>PPS</idPartido>
                </partido>
                <partido>
                    <idPartido>PV</idPartido>
                </partido>
            </Partidos>
        </bloco>
    </blocos>
    """
    expected_list = {
        'nomeBloco': 'PV, PPS',
        'Partidos': {'partido': [{'idPartido': 'PPS'}, {'idPartido': 'PV'}]}
    }
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        'ObterPartidosBlocoCD',
        body=xml_response, status=200)
    assert cd.deputies.parties_bloc() == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_parliamentary_seats():
    xml_response = """
    <bancadas>
        <bancada sigla="Bloco PP, PTB" nome="Bloco Parlamentar PP, PTB">
            <lider>
                <ideCadastro>160527</ideCadastro>
            </lider>
            <vice_lider>
                <ideCadastro>73666</ideCadastro>
            </vice_lider>
        </bancada>
    </bancadas>
    """
    expected_list = [{'nome': 'Bloco Parlamentar PP, PTB',
                      'sigla': 'Bloco PP, PTB'}]
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        'ObterLideresBancadas',
        body=xml_response, status=200)
    assert cd.deputies.parliamentary_seats() == expected_list
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_parliamentary_seat_leaders():
    xml_response = """
    <bancadas>
        <bancada sigla="Bloco PP, PTB" nome="Bloco Parlamentar PP, PTB">
            <lider>
                <ideCadastro>160527</ideCadastro>
            </lider>
            <vice_lider>
                <ideCadastro>73666</ideCadastro>
            </vice_lider>
            <vice_lider>
                <ideCadastro>626651</ideCadastro>
            </vice_lider>
        </bancada>
    </bancadas>
    """
    expected_dict = {
        'lider': {'ideCadastro': 160527},
        'vice_lider': [{'ideCadastro': 73666}, {'ideCadastro': 626651}]
    }
    responses.add(
        responses.GET,
        'http://www.camara.gov.br/SitCamaraWS/Deputados.asmx/'
        'ObterLideresBancadas',
        body=xml_response, status=200)
    result_dict = cd.deputies.parliamentary_seat_leaders('Bloco PP, PTB')
    assert result_dict == expected_dict
    assert len(responses.calls) == 1


@responses.activate
def test_deputy_frequency():
    xml_response = """
    <parlamentar>
        <legislatura>54</legislatura>
        <diasDeSessoes2>
            <dia>
                <frequencianoDia>Presença</frequencianoDia>
                <sessoes>
                    <sessao>
                        <frequencia>Presença</frequencia>
                    </sessao>
                </sessoes>
            </dia>
        </diasDeSessoes2>
    </parlamentar>
    """
    expected_dict = {
        'frequencianoDia': 'PresenÃ§a',
        'sessoes': {'sessao': {'frequencia': 'PresenÃ§a'}},
    }
    responses.add(
        responses.GET,
        'http://www.camara.leg.br/sitcamaraws/SessoesReunioes.asmx/'
        'ListarPresencasParlamentar',
        body=xml_response, status=200)
    result_dict = cd.deputies.frequency('10/10/2010', '11/10/2010', 1)
    assert result_dict == expected_dict

    result_dict = cd.deputies.frequency(
        datetime.date(2010, 10, 10), datetime.date(2010, 10, 11), 1)
    assert result_dict == expected_dict

    result_dict = cd.deputies.frequency(
        datetime.datetime(2010, 10, 10), datetime.datetime(2010, 10, 11), 1)
    assert result_dict == expected_dict
    assert len(responses.calls) == 3
