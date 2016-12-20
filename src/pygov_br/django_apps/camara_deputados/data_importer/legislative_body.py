from pygov_br.django_apps.base import BaseDataImporter
from pygov_br.django_apps.camara_deputados import models
from pygov_br.camara_deputados import cd


class LegislativeBodyTypeImporter(BaseDataImporter):

    field_relation = {
        'id': 'id',
        'description': 'descricao'
    }

    def get_model(self):
        return models.LegislativeBodyType

    def get_data(self):
        return cd.legislative_bodies.types()


class LegislativeBodyRoleImporter(BaseDataImporter):

    field_relation = {
        'id': 'id',
        'description': 'descricao'
    }

    def get_model(self):
        return models.LegislativeBodyRole

    def get_data(self):
        return cd.legislative_bodies.roles()


class LegislativeBodyImporter(BaseDataImporter):

    field_relation = {
        'id': 'id',
        'legislative_body_type': 'idTipodeOrgao',
        'initials': 'sigla',
        'description': 'descricao',
    }

    roles = {
        'Presidente': 'Presidente',
        'PrimeiroVice-Presidente': '1º Vice-Presidente',
        'SegundoVice-Presidente': '2º Vice-Presidente',
        'TerceiroVice-Presidente': '3º Vice-Presidente',
        'Relator': 'Relator',
        'Relator-Parcial': 'Relator-Parcial',
        'PrimeiroSecretário': '1º Secretário',
        'SegundoSecretário': '2º Secretário',
        'TerceiroSecretário': '3º Secretário',
        'QuartoSecretário': '4º Secretário',
        'PrimeiroSuplente-de-Secretário': '1º Suplente de Secretário',
        'SegundoSuplente-de-Secretário': '2º Suplente de Secretário',
        'TerceiroSuplente-de-Secretário': '3º Suplente de Secretário',
        'QuartoSuplente-de-Secretário': '4º Suplente de Secretário',
    }

    def get_model(self):
        return models.LegislativeBody

    def get_data(self):
        return cd.legislative_bodies.all()

    def clean_legislative_body_type(self, data):
        return models.LegislativeBodyType.objects.get(id=data)

    def after_save_object(self, obj):
        if obj.initials == 'PLEN':
            return

        members = cd.legislative_bodies.members(obj.id)
        if members is not None:
            for role in members.keys():
                if role == 'membro':
                    self._save_common_members(members, obj)
                else:
                    self._save_special_members(members[role], role, obj)

    def _save_special_members(self, members, role, legislative_body):
        if isinstance(members, list):
            for member in members:
                self._save_member(member['ideCadastro'], role=role,
                                  legislative_body=legislative_body)
        else:
            self._save_member(members['ideCadastro'], role=role,
                              legislative_body=legislative_body)

    def _save_common_members(self, members, legislative_body):
        for member in members['membro']:
            self._save_member(member['ideCadastro'], legislative_body)

    def _save_member(self, deputy_id, legislative_body, role=False):
        deputy = self._get_deputy(deputy_id)
        obj_dict = {}
        if deputy is not None:
            obj_dict['deputy'] = deputy
            obj_dict['legislative_body'] = legislative_body

            if role:
                obj_dict['role'] = models.LegislativeBodyRole.objects.get(
                    description=self.roles[role]
                )

        if obj_dict:
            models.LegislativeBodyMember.objects.get_or_create(**obj_dict)

    def _get_deputy(self, deputy_id):
        try:
            return models.Deputy.objects.get(pk=deputy_id)
        except models.Deputy.DoesNotExist:
            return None
