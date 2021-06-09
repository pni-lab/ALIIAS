from ALIIAS.ls_api_wrapper import LimeSurveyController

ls = LimeSurveyController(username='admin', password='admin', url="https://www.uni-due.de/~ht2203/limesurvey_sfb289_test/index.php/admin/remotecontrol")


surveys = ls.get_surveys()
for survey in surveys:
    print(survey.get('sid'), survey.get('surveyls_title'))



ret = ls.get_participants(survey_id=348618)
print(ret)

for part in ret:
    print(part)
