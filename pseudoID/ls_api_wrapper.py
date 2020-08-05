from limesurveyrc2api import LimeSurveyRemoteControl2API
from collections import OrderedDict
import config


class LimeSurveyController:

    def __init__(self, user_key=config._user_key_, url=config._ls_url_rc_, username='admin', password='admin'):
        self.username = username  # todo: encrypt with user key
        self.password = password  # todo: encrypt with user key

        # Make a session.
        self.api = LimeSurveyRemoteControl2API(url)
        self.session_req = self.api.sessions.get_session_key(username, password)
        self.session_key = self.session_req.get('result')


    def getSurveys(self):
        # Get a list of surveys the admin can see, and print their IDs.
        surveys_req = self.api.surveys.list_surveys(self.session_key, self.username)
        surveys = surveys_req.get('result')
        ret = []
        for survey in surveys:
            ret.append({'sid': survey.get('sid'), 'surveyls_title': survey.get('surveyls_title')})

        return ret

    def register_in_cpdb(self, short_id, long_id, logical_delete=False):

        participant_data = [{"lastname" : short_id,
                             "longID" : long_id,
                             "blacklisted" : logical_delete,
                             "language" : "de"
                             }]

        params = OrderedDict([
            ('sSessionKey', self.session_key),
            ('aParticipants', participant_data),
            ('update', logical_delete)
        ])

        data = self.api.utils.prepare_params('cpd_importParticipants', params)
        response = self.api.utils.request(data)
        return response

# todo when cloning survey: init participant table, link longID with a dummy participant