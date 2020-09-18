from pseudoID.ls_api_wrapper import LimeSurveyController

ls = LimeSurveyController(username='admin', password='admin')


surveys = ls.get_surveys()
for survey in surveys:
    print(survey.get('sid'), survey.get('surveyls_title'))



ret = ls.get_participants(survey_id=348618)
print(ret)

for part in ret:
    print(part)
