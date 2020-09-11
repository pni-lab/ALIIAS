from limesurveyrc2api import LimeSurveyRemoteControl2API
from collections import OrderedDict
from pseudoID import config


class LimeSurveyController:

    def __init__(self, username, password, url=config._ls_url_rc_):
        self.username = username  # todo: encrypt with user key
        self.password = password  # todo: encrypt with user key

        # Make a session.
        self.api = LimeSurveyRemoteControl2API(url)
        self.session_req = self.api.sessions.get_session_key(username, password)
        self.session_key = self.session_req.get('result')

    def get_surveys(self, filter=""):
        # Get a list of surveys the admin can see, and print their IDs.
        surveys_req = self.api.surveys.list_surveys(self.session_key, self.username)
        surveys = surveys_req.get('result')
        ret = []
        for survey in surveys:
            if filter in survey.get('surveyls_title'):
                ret.append({'sid': survey.get('sid'), 'surveyls_title': survey.get('surveyls_title')})
        return ret

    def get_participants(self, survey_id):
        # list_participants(string $sSessionKey,integer $iSurveyID,integer $iStart,integer $iLimit = 10,
        # boolean $bUnused = false,boolean|array $aAttributes = false,array $aConditions = array()): array

        params = OrderedDict([
            ('sSessionKey', self.session_key),
            ('iSurveyID', survey_id),
            ('iStart', 0),
            ('iLimit', 1000000000),
            ('aAttributes', 'true')
        ])

        data = self.api.utils.prepare_params('list_participants', params)
        response = self.api.utils.request(data)
        return response['result']

    def contains_participant(self, survey_id, short_id, long_id):
        ret = self.get_participants(survey_id=survey_id)

        print("**", ret)

        if isinstance(ret, dict):
            print("return false here")
            return False
        for part in ret:
            if part['participant_info']['firstname'] == short_id:
                assert (part['participant_info']['lastname'] == long_id), "Possible Duplicate Detected!"
                return True
            else:
                return False
            

    def register_to_survey(self, short_id, long_id, survey_id):
        #string $sSessionKey, integer $iSurveyID, array $aParticipantData, boolean $bCreateToken = true): array
        participant_data = [{"firstname": short_id,
                             "lastname": long_id,
                             "language": "de"
                             }]

        params = OrderedDict([
            ('sSessionKey', self.session_key),
            ('iSurveyID', survey_id),
            ('aParticipants', participant_data)
        ])

        data = self.api.utils.prepare_params('add_participants', params)
        response = self.api.utils.request(data)
        return response

    def register_in_cpdb(self, short_id, long_id, logical_delete=False):

        if logical_delete:
            blacklisted = 'Y'
        else:
            blacklisted = 'N'

        participant_data = [{"lastname": short_id,
                             "longID": long_id,
                             "blacklisted": blacklisted,
                             "language": "de"
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

    def close_session(self):
        #release_session_key(string $sSessionKey): string
        params = OrderedDict([
            ('sSessionKey', self.session_key)
        ])
        data = self.api.utils.prepare_params('release_session_key', params)
        response = self.api.utils.request(data)
        return response