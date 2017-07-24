from pygov_br.django_apps.base import BaseDataImporter
from pygov_br.django_apps.camara_deputados import models
from pygov_br.camara_deputados import cd


class SessionImporter(BaseDataImporter):

    field_relation = {
        'code': 'codigo',
        'date': 'data',
        'session_type': 'tipo',
        'number': 'numero',
    }

    def get_data(self):
        return cd.sessions.speeches('15/01/2016', '15/12/2016')

    def get_model(self):
        return models.Session

    def clean_session_type(self, data):
        data = data.replace(' - CD', '')
        return models.SessionType.objects.get_or_create(description=data)[0]


class SpeechImporter(BaseDataImporter):

    field_relation = {
        'initial_time': 'horaInicioDiscurso',
        'insertion_number': 'numeroInsercao',
        'quarter_number': 'numeroQuarto',
        'order': 'orador',
        'summary': 'sumario',
        'indexes': 'txtIndexacao',
        'author': 'orador',
        'session': 'codigoSessao',
        'session_phase': 'faseSessao',
    }

    def get_data(self):
        sessions = cd.sessions.speeches('15/01/2016', '15/12/2016')
        speeches_list = []
        for session in sessions:
            session_code = session['codigo']
            phases = session['fasesSessao']['faseSessao']
            if isinstance(phases, list):
                for phase in phases:
                    speeches = phase['discursos']['discurso']
                    for speech in speeches:
                        speech['codigoSessao'] = session_code
                        speech['faseSessao'] = {
                            'codigo': phase['codigo'],
                            'descricao': phase['descricao']
                        }
            else:
                speeches = phases['discursos']['discurso']
                if isinstance(speeches, list):
                    for speech in speeches:
                        speech['codigoSessao'] = session_code
                        speech['faseSessao'] = {
                            'codigo': phases['codigo'],
                            'descricao': phases['descricao']
                        }
                    speeches_list += speeches
                else:
                    speech = speeches
                    speech['codigoSessao'] = session_code
                    speech['faseSessao'] = {
                        'codigo': phases['codigo'],
                        'descricao': phases['descricao']
                    }
                    speeches_list.append(speech)
        return speeches_list

    def get_model(self):
        return models.Speech

    def clean_author(self, data):
        deputy_name = data['nome'].split(' (')
        try:
            return models.Deputy.objects.get(parliamentary_name=deputy_name[0])
        except models.Deputy.DoesNotExist:
            return None

    def clean_session(self, data):
        return models.Session.objects.get(code=data)

    def clean_session_phase(self, data):
        return models.SessionPhase.objects.get_or_create(
            code=data['codigo'],
            description=data['descricao']
        )[0]

    def clean_order(self, data):
        return data['numero']

    # def after_save_object(self, obj):
    #     speech = cd.sessions.full_speech(
    #         obj.session.code, obj.order,
    #         obj.quarter_number, obj.insertion_number
    #     )
    #     if speech['discurso'] is not None:
    #         obj.full_text = speech['discurso']
    #         obj.save()
