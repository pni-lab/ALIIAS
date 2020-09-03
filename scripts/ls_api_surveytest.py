from pseudoID.ls_api_wrapper import LimeSurveyController

ls = LimeSurveyController()


surveys = ls.getSurveys()
for survey in surveys:
    print(survey.get('sid'), survey.get('surveyls_title'))



survey_id = 862374
#ret=ls.register_to_survey("fromapi3",
#                      "0883eeb065eed685f9ccfa34d812c9e778bad602ed3c348a862fc74dac035a674170fa1200d2f801c4ba9caf2930af58"
#                      "d72e1324dd81978e2b238927805fa3a95f41bf680784da2bbd85ca8e0c8723c4",
#                      survey_id=survey_id
#                      )

ret = ls.get_participants(survey_id=survey_id)

for part in ret:
    print(part)
