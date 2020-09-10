import random

from pseudoID import config
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController
from pseudoID.utility import PseudonymLogger, norm_str
from pseudoID.barcode_gen import generate_barcodeset

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')

possible_duplicate = False
already_registered = False
already_added_to = []
first_name = None
subject = {}
ids = {}
lime_warning = {}
enc = Encryptor(site_tag=config._site_tag_['Test'])
show_pseudonym = {}
lscontrol = None

logger = PseudonymLogger()

@bp.route('/login', methods=('GET', 'POST'))
def login():
    global lscontrol
    session['username'] = None
    if request.method == 'POST':
        username = request.form['username']
        lscontrol = LimeSurveyController(username=username, password=request.form['password'])

        if isinstance(lscontrol.session_key, dict):
            # error logging in
            flash(lscontrol.session_key['status'])
            lscontrol = None
        else:
            session['username'] = username
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

    surveys = lscontrol.get_surveys(filter="A01") #Todo: include the actual project name here dynamically!
    survey_names = []
    for survey in surveys:
        survey_names.append(survey['surveyls_title'])

    if request.method == 'POST':
        subject['first_name'] = request.form['first_name']
        subject['family_name'] = request.form['family_name']
        subject['place_of_birth'] = request.form['place_of_birth']
        subject['date_of_birth'] = request.form['dob_d'].zfill(2) + '.' + \
                                   request.form['dob_m'].zfill(2) + '.' + \
                                   request.form['dob_y']
        subject['maiden_name'] = request.form['maiden_name']
        status = request.form['registered']

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
        for survey in surveys:

            # check if the participant is already added to this survey
            try:
                already_added = lscontrol.contains_participant(survey['sid'], short_id, long_id)
            except AssertionError as error:
                # duplicate
                print(error)
                already_added = False
                lime_warning['warning_color'] = 'Tomato'
                lime_warning['warning_text'] = config._warnings_['duplicate']
                lime_warning['warning_details'] += "Duplicate detected in survey: " + survey['surveyls_title'] + ". "
                #handle duplicate:
                ids['short_id'] = ids['short_id'] + random.choice(config._hexchars_)

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


        #response = lscontrol.register_in_cpdb(short_id, long_id)

        #if response['result']['ImportCount'] == 0 and status == 'registered':
        #    lime_warning['warning_color'] = 'MediumSeaGreen'
        #    lime_warning['warning_text'] = config._warnings_['known']
        #    already_registered = True
        #elif response['result']['ImportCount'] == 0 and status == 'not_registered':
        #    lime_warning['warning_color'] = 'Tomato'
        #    lime_warning['warning_text'] = config._warnings_['duplicate']
        #    possible_duplicate = True
        #elif response['result']['ImportCount'] != 0 and status == 'not_registered':
        #    lime_warning['warning_color'] = 'MediumSeaGreen'
        #    lime_warning['warning_text'] = config._warnings_['new']
        #elif response['result']['ImportCount'] != 0 and status == 'registered':
        #    lime_warning['warning_color'] = 'Tomato'
        #    lime_warning['warning_text'] = config._warnings_['unknown']

       # lime_warning['warning_short'] = "LS: " + str((response['result']['ImportCount'], status))

        logger.add_entry(
            "PREVIEW : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] +\
        lime_warning['warning_details'])

        return redirect(url_for('pseudoID.preview'))

    return render_template('pseudoID/generate.html', _exp_tag_=config._exp_tag_)


@bp.route('/preview', methods=('GET', 'POST'))
def preview():
    barcodes = []
    global possible_duplicate
    global show_pseudonym
    global subject, ids, lime_warning, logger, lscontrol, survey_not_added

    surveys = lscontrol.get_surveys(filter="A01") #Todo: include the actual project name here dynamically!
    survey_not_added = dict()
    survey_added = dict()
    for survey in surveys:
        if survey['sid'] not in already_added_to:
            survey_not_added[survey['sid']] = survey['surveyls_title']
        else:
            survey_added[survey['sid']] = survey['surveyls_title']

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
                print("add:", ids['short_id'], ids['long_id'], sid)
                lscontrol.register_to_survey(ids['short_id'], ids['long_id'], sid)
                logger.add_entry(
                    "ACCEPTED : " + ids['short_id'] + '\t' + ids['long_id'] + '\t' + lime_warning['warning_text'] + \
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

        surveys = lscontrol.get_surveys(filter="A01")  # Todo: include the actual project name here dynamically!
        survey_not_added = dict()
        survey_added = dict()
        for survey in surveys:
            if survey['sid'] not in already_added_to:
                survey_not_added[survey['sid']] = survey['surveyls_title']
            else:
                survey_added[survey['sid']] = survey['surveyls_title']

        print("not_added", survey_not_added)
        print("    added", survey_added)

    return render_template('pseudoID/preview.html',
                           items=barcodes,
                           subject=subject,
                           ids=ids,
                           survey_not_added=survey_not_added,
                           survey_added=survey_added,
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
    return render_template('pseudoID/exit.html')
