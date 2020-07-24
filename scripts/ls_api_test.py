from limesurveyrc2api import LimeSurveyRemoteControl2API
from collections import OrderedDict

url = 'https://www.uni-due.de/~ht2203/limesurvey/index.php/admin/remotecontrol'
username = 'admin'
password = 'admin'

# Make a session.
api = LimeSurveyRemoteControl2API(url)
session_req = api.sessions.get_session_key(username, password)
session_key = session_req.get('result')

# Get a list of surveys the admin can see, and print their IDs.
surveys_req = api.surveys.list_surveys(session_key, username)
surveys = surveys_req.get('result')
for survey in surveys:
    print(survey.get('sid'))
    print(survey.get('surveyls_title'))

# cpd_importParticipants
"""
     * Import a participant into the LimeSurvey CPDB
     *
     * It stores attributes as well, if they are registered before within ui
     *
     * Call the function with $response = $myJSONRPCClient->cpd_importParticipants( $sessionKey, $aParticipants);
     *
     * @param int $sSessionKey
     * @param array $aParticipants
     * [[0] => ["email"=>"dummy-02222@limesurvey.com","firstname"=>"max","lastname"=>"mustermann"]]
     * @param bool $update
     * @return array with status
     */
"""
participant_data = [{"lastname":"api7",
                     "firstname":"7qwkjbdkqjbdxkjqbdkjqebdkjqndkeqjdnqlkdnqeldkqnlkcbqkjbvx1zvi26rtsuz35rq7ds8z1o9z892sh9172s87fg36s721^wf7sf17gv3ius3qbx87qgvx8u17v81zbxu1biubq3xiuh",
                     "longID":"7qwkjbdkqjbdxkjqbdkjqebdkjqndkeqjdnqlkdnqeldkqnlkcbqkjbvx1zvi26rtsuz35rq7ds8z1o9z892sh9172s87fg36s721^wf7sf17gv3ius3qbx87qgvx8u17v81zbxu1biubq3xiuh",
                     "language":"de"
                     }]

params = OrderedDict([
            ('sSessionKey', session_key),
            ('aParticipants', participant_data),
            #('update', True)
        ])
data = api.utils.prepare_params('cpd_importParticipants', params)
response = api.utils.request(data)
print(response)

if response['result']['ImportCount'] == 0:
    print("Participant already registered. No new participant added.")


#if response['result']['ImportCount'] == 0 and response['result']['ImportCount'] > 0:
#    print("Error: Participant short ID already taken by a participant with different longID. Short ID must be adjusted!")


# input into survey level-table:
#params = OrderedDict([
#            ('sSessionKey', session_key),
#            ('iSurveyID', 20),
#            ('aParticipants', participant_data),
#            #('update', True)
#        ])
#data = api.utils.prepare_params('add_participants', params)
#response = api.utils.request(data)
#print(response)

# todo when cloning survey: init participant table, link longID with a dummy participant