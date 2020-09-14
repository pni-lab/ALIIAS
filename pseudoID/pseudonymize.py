import random

from pseudoID import config
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController
from pseudoID.utility import PseudonymLogger, norm_str
from pseudoID.barcode_gen import generate_barcodeset
from pseudoID.hw_encryption import SessionHandler

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')

handler = SessionHandler()
handler.set()
enc = Encryptor(site_tag=handler.site_tag, pseudonym_key=handler.pseudo_key)

possible_duplicate = False
already_registered = False
already_added_to = []
first_name = None
subject = {}
ids = {}
lime_warning = {}
show_pseudonym = {}
lscontrol = None

logger = PseudonymLogger()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    global lscontrol
    session['username'] = None
    if request.method == 'POST':
        username = request.form['username']
        try:
         lscontrol = LimeSurveyController(username=username, password=request.form['password'])
        except AttributeError as error:
            flash("Unable to connect to the LimeSurvey server. Please check your internet connection!")
            print(error)
            logger.add_entry(
                "LOGIN: Unable to connect to LimeSurvey")
            return render_template('pseudoID/login.html')

        if isinstance(lscontrol.session_key, dict):
            # error logging in
            flash(lscontrol.session_key['status'])
            lscontrol = None
            logger.add_entry(
                "LOGIN: Unsuccessful Limesurvey login as " + username)
        else:
            session['username'] = username
            logger.add_entry(
                "LOGIN: Successful Limesurvey login as " + username)
            return redirect(url_for('pseudoID.generate'))

    return render_template('pseudoID/login.html')


@bp.route('/generate', methods=('GET', 'POST'))
def generate():
    # reset globals
    global possible_duplicate, already_registered, lscontrol, already_added_to
    already_registered = False
    possible_duplicate = False
    global show_pseudonym, subject, ids, lime_warning
    subject = {}
    ids = {}
    lime_warning = {}
    show_pseudonym = {}
    duplicate_warning = False

    if lscontrol:
        surveys = lscontrol.get_surveys(filter=handler.site)
        survey_names = []
        for survey in surveys:
            survey_names.append(survey['surveyls_title'])
    else:
        logger.add_entry(
            "NO_LIMESURVEY_CONNECTION")

    if request.method == 'POST':
        subject['first_name'] = request.form['first_name']
        subject['family_name'] = request.form['family_name']
        subject['place_of_birth'] = request.form['place_of_birth']
        subject['date_of_birth'] = request.form['dob_d'].zfill(2) + '.' + \
                                   request.form['dob_m'].zfill(2) + '.' + \
                                   request.form['dob_y']
        subject['maiden_name'] = request.form['maiden_name']
        #status = request.form['registered']

        # do the actual pseudonym generation
        global enc
        long_id = enc.long_id(norm_str(subject['first_name']) + ' ' +
                              norm_str(subject['family_name']) + ' ' +
                              norm_str(subject['place_of_birth']) + ' ' +
                              norm_str(subject['date_of_birth']) + ' ' +
                              norm_str(subject['maiden_name']))

        short_id = enc.short_id(long_id)
        ids['short_id'] = short_id
        ids['exp_tag'] = request.form['exp_tag']
        ids['long_id'] = long_id

        # limesurvey integration
        already_added_to = []
        lime_warning['warning_color'] = 'MediumSeaGreen'
        lime_warning['warning_text'] = "No problems detected."
        lime_warning['warning_details'] = ''

        if lscontrol:
            for survey in surveys:

                # check if the participant is already added to this survey
                try:
                    already_added = lscontrol.contains_participant(survey['sid'], short_id, long_id)
                except AssertionError as error:
                    # duplicate
                    print(error)
                    already_added = False
                    duplicate_warning = True
                    lime_warning['warning_text'] = config._warnings_['duplicate']
                    lime_warning['warning_details'] += "Duplicate detected in survey: " + survey['surveyls_title'] + ". "
                    #handle duplicate:
                    ids['short_id'] = ids['short_id'] + random.choice(config.settings['ENCRYPTION']['char_base'])

                if already_added:
                    already_added_to.append(survey['sid'])

            if len(already_added_to) > 0:
                lime_warning['warning_details'] += "This participant has already been added to the following surveys: " \
                                              + str(already_added_to)
            else:
                lime_warning['warning_details'] += " No participant with these data has been added to LimeSurvey yet."

            lime_warning['warning_details'] += " Please carefully check all data. Typographical errors can result in " \
                                              "database corruption!" \
                                              " Click 'Proceed to the pseudonym' to obtain the short ID."
        else:
            lime_warning['warning_text'] += "NO_LS"
            lime_warning['warning_details'] += "no ls integration"

        logger.add_entry(
            "PREVIEW : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] +\
        lime_warning['warning_details'])

        return redirect(url_for('pseudoID.preview'))

    return render_template('pseudoID/generate.html', _exp_tag_=config._exp_tag_, duplicate_warning=duplicate_warning)


@bp.route('/preview', methods=('GET', 'POST'))
def preview():
    barcodes = []
    newly_added = []
    global possible_duplicate
    global show_pseudonym
    global subject, ids, lime_warning, logger, lscontrol, already_added_to

    surveys = lscontrol.get_surveys(filter=handler.site)
    survey_not_added = dict()
    survey_added = dict()
    ls_links = dict()
    if lscontrol:
        surveys = lscontrol.get_surveys(filter=handler.site)
        for survey in surveys:
            if survey['sid'] not in already_added_to:
                survey_not_added[survey['sid']] = survey['surveyls_title']
            else:
                survey_added[survey['sid']] = survey['surveyls_title']
    else:
        pass

    if request.method == 'POST':

        surveys_to_add = request.form.getlist('checkbox_survey_not_added')
        print(surveys_to_add)

        # undo
        if request.form['proceed'] == "No! Undo Transaction.":
            logger.add_entry(
                "WITHDRAWN : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] + \
                lime_warning['warning_details'])
            subject = ids = lime_warning = None
            return redirect(url_for('pseudoID.generate'))

        if request.form['proceed'] == "Yes! Proceed to the pseudonym.":
            # register participant to the given survey(s)
            for sid in surveys_to_add:
                if lscontrol:
                    lscontrol.register_to_survey(ids['short_id'], ids['long_id'], sid)
                    logger.add_entry(
                        "ACCEPTED : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] + \
                        lime_warning['warning_details'])
                else:
                    logger.add_entry(
                        "ACCEPTED_WITHOUT_LS : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] + \
                        lime_warning['warning_details'])

            barcodes = generate_barcodeset(ids['short_id'])
            # for f in barcodes:
            #    send_from_directory('static', f)

            show_pseudonym['show_pseudonym'] = True

        if request.form['proceed'] == "New participant":
            return redirect(url_for('pseudoID.generate'))

        if request.form['proceed'] == "Exit PseudoID":
            # shutdown_server()
            return redirect(url_for('pseudoID.exit'))

        # check if participant was added and update corresponding variables
        already_added_to = []
        if lscontrol:
            for survey in surveys:

                # check if the participant is already added to this survey
                try:
                    already_added = lscontrol.contains_participant(survey['sid'], ids['short_id'], ids['long_id'])
                except AssertionError as error:
                    # duplicate
                    print(error)
                    already_added = False
                if already_added:
                    already_added_to.append(survey['sid'])

            survey_not_added = dict()
            bckp_survey_added = survey_added
            survey_added = dict()
            for survey in surveys:
                if survey['sid'] not in already_added_to:
                    survey_not_added[survey['sid']] = survey['surveyls_title']
                else:
                    survey_added[survey['sid']] = survey['surveyls_title']
                    token=lscontrol.get_token(survey['sid'], ids['short_id'], ids['long_id'])
                    ls_links[survey['sid']] = config.settings['LIMESURVEY']['url_base'] + "/index.php/" + survey['sid'] + "?token=" + token

                    if survey['sid'] not in bckp_survey_added.keys():
                        newly_added.append(survey['surveyls_title'])
        else:
            pass

    return render_template('pseudoID/preview.html',
                           items=barcodes,
                           subject=subject,
                           ids=ids,
                           survey_not_added=survey_not_added,
                           survey_added=survey_added,
                           newly_added=newly_added,
                           ls_links=ls_links,
                           **lime_warning,
                           **show_pseudonym)


@bp.route('/reidentify', methods=('GET', 'POST'))
def reidentify():
    if request.method == 'POST':
        global enc
        long_id = request.form['long_id']
        flash(enc.reidentify(long_id))
    return render_template('pseudoID/reidentify.html')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@bp.route('/exit')
def exit():
    if lscontrol:
        lscontrol.close_session()
    session['username'] = None
    shutdown_server()
    logger.add_entry(
        "EXIT: Regular shutdown")
    return render_template('pseudoID/exit.html')
