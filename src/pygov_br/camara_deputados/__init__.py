from pygov_br.base import ClientWrapper
from .deputy import DeputyClient
from .legislative_body import LegislativeBodyClient
from .proposal import ProposalClient
from .session import SessionClient

cd = ClientWrapper(
    deputies=DeputyClient,
    legislative_bodies=LegislativeBodyClient,
    proposals=ProposalClient,
    sessions=SessionClient
)
