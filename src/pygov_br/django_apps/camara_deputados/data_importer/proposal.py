from django.db import transaction
from pygov_br.django_apps.base import BaseDataImporter
from pygov_br.django_apps.camara_deputados import models
from pygov_br.camara_deputados import cd


class ProposalTypeImporter(BaseDataImporter):

    field_relation = {
        "id": "id",
        "is_active": "ativa",
        "description": "descricao",
        "gender": "genero",
        "initials": "tipoSigla",
    }

    def get_model(self):
        return models.ProposalType

    def get_data(self):
        return cd.proposals.types()


class ProposalImporter(BaseDataImporter):

    field_relation = {
        "id": "id",
        "year": "ano",
        "number": "numero",
        "submission_date": "datApresentacao",
        "name": "nome",
        "summary": "txtEmenta",
        "summary_explanation": "txtExplicacaoEmenta",
        "proposal_type": "tipoProposicao",
    }

    def get_model(self):
        return models.Proposal

    def get_data(self):
        return cd.proposals.filter(proposal_type='PL', year=2016)

    def clean_author(self, data):
        if data['idecadastro']:
            return models.Deputy.objects.get(enrollment_id=data['idecadastro'])
        else:
            return None

    def clean_proposal_type(self, data):
        return models.ProposalType.objects.get(initials=data['sigla'])

    @transaction.atomic
    def after_save_object(self, obj):
        extra_info = cd.proposals.get(proposal_type=obj.proposal_type.initials,
                                      proposal_number=obj.number,
                                      year=obj.year)
        obj.indexes = extra_info['Indexacao']
        obj.link = extra_info['LinkInteiroTeor']
        if extra_info['ideCadastro']:
            try:
                author = models.Deputy.objects.get(
                    id=extra_info['ideCadastro']
                )
                obj.author = author
            except models.Deputy.DoesNotExist:
                print('nao existe', extra_info['ideCadastro'])

        obj.save()
