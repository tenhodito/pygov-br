import pytest
import pygov_br
from pygov_br.camara_deputados.deputy import DeputyClient
from pygov_br.camara_deputados.legislative_body import LegislativeBodyClient
from pygov_br.camara_deputados.proposal import ProposalClient


def test_lazy_loader():
    assert isinstance(pygov_br.data.camara_deputados.deputy, DeputyClient)
    assert isinstance(pygov_br.data.camara_deputados.legislative_body, LegislativeBodyClient)
    assert isinstance(pygov_br.data.camara_deputados.proposal, ProposalClient)