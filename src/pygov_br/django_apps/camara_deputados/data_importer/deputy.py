from pygov_br.django_apps.base import BaseDataImporter
from pygov_br.django_apps.camara_deputados import models
from pygov_br.camara_deputados import cd


class PartyImporter(BaseDataImporter):

    field_relation = {
        'creation_date': 'dataCriacao',
        'extinction_date': 'dataExtincao',
        'name': 'nomePartido',
        'initials': 'siglaPartido',
    }

    def get_model(self):
        return models.Party

    def get_data(self):
        return cd.deputies.parties()


class PartyBlocImporter(BaseDataImporter):

    field_relation = {
        'id': 'idBloco',
        'creation_date': 'dataCriacaoBloco',
        'extinction_date': 'dataExtincaoBloco',
        'name': 'nomeBloco',
        'initials': 'siglaBloco',
    }

    def get_model(self):
        return models.PartyBloc

    def get_data(self):
        return cd.deputies.parties_bloc()


class PartyBlocMemberImporter(BaseDataImporter):

    field_relation = {
        'party_bloc': 'idBloco',
        'party': 'idPartido',
        'adhesion_date': 'dataAdesaoPartido',
        'shutdown_date': 'dataDesligamentoPartido',
    }

    def get_model(self):
        return models.PartyBlocMember

    def get_data(self):
        return cd.deputies.parties_bloc()

    def save_data(self):
        data = self.get_data()
        for data_row in data:
            members_data = data_row['Partidos']['partido']
            for data in members_data:
                data['idBloco'] = data_row['idBloco']
                self._get_object(data)

    def clean_party_bloc(self, data):
        return models.PartyBloc.objects.get(id=data)

    def clean_party(self, data):
        return models.Party(initials=data)


class ParliamentarySeatImporter(BaseDataImporter):

    field_relation = {
        'name': 'nome',
        'initials': 'sigla',
    }

    def get_model(self):
        return models.ParliamentarySeat

    def get_data(self):
        return cd.deputies.parliamentary_seats()

    def after_save_object(self, obj):
        leaders = cd.deputies.parliamentary_seat_leaders(obj.initials)
        leader_data = leaders.get('lider', None)
        if leader_data:
            leader = models.Deputy.objects.get(pk=leader_data['ideCadastro'])
            leader.parliamentary_seat = obj
            leader.parliamentary_seat_leader = True
            leader.save()
        else:
            representative_id = leaders['representante']['ideCadastro']
            representative = models.Deputy.objects.get(pk=representative_id)
            representative.parliamentary_seat = obj
            representative.save()
        vice_leaders = leaders.get('vice_leader', None)
        if vice_leaders:
            for vice_leader in vice_leaders:
                deputy = models.Deputy.objects.get(
                    pk=vice_leader['ideCadastro'])
                deputy.parliamentary_seat = obj
                deputy.save()


class DeputyImporter(BaseDataImporter):

    field_relation = {
        'id': 'ideCadastro',
        'outbuilding': 'anexo',
        'budget_id': 'codOrcamento',
        'condition': 'condicao',
        'email': 'email',
        'phone': 'fone',
        'cabinet': 'gabinete',
        'parliamentary_id': 'idParlamentar',
        'enrollment_id': 'matricula',
        'name': 'nome',
        'parliamentary_name': 'nomeParlamentar',
        'party': 'partido',
        'gender': 'sexo',
        'region': 'uf',
        'photo_url': 'urlFoto',
    }

    def get_model(self):
        return models.Deputy

    def get_data(self):
        return cd.deputies.all()

    def clean_party(self, data):
        return models.Party.objects.get(initials=data)
