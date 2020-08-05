import functools
import config
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController
from pseudoID.utility import PseudonymLogger, norm_str

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')

first_name = None
subject = {}
ids = {}
lime_warning = {}
enc = Encryptor()

logger = PseudonymLogger()


@bp.route('/generate', methods=('GET', 'POST'))
def generate():
    if request.method == 'POST':
        global subject
        subject['first_name'] = request.form['first_name']
        subject['family_name'] = request.form['family_name']
        subject['place_of_birth'] = request.form['place_of_birth']
        subject['date_of_birth'] = request.form['dob_d'].zfill(2) + '.' + \
                                   request.form['dob_m'].zfill(2) + '.' + \
                                   request.form['dob_y']
        subject['maiden_name'] = request.form['maiden_name']
        status = request.form['registered']
        global enc
        long_id = enc.long_id(norm_str(subject['first_name']) + ' ' +
                              norm_str(subject['family_name']) + ' ' +
                              norm_str(subject['place_of_birth']) + ' ' +
                              norm_str(subject['date_of_birth']) + ' ' +
                              norm_str(subject['maiden_name']))

        short_id = enc.short_id(long_id)
        global ids
        ids['short_id'] = short_id + request.form['exp_tag']
        ids['long_id'] = long_id

        global lime_warning

        # limesurvey integration
        lscontrol = LimeSurveyController()
        response = lscontrol.register_in_cpdb(short_id, long_id)

        if response['result']['ImportCount'] == 0 and status == 'registered':
            lime_warning['warning_color'] = 'MediumSeaGreen'
            lime_warning['warning_text'] = 'Participant already registered in LimeSurvey. No new participant added.'
        elif response['result']['ImportCount'] == 0 and status == 'not_registered':
            lime_warning['warning_color'] = 'Tomato'
            lime_warning['warning_text'] = 'ID already registered in LimeSurvey. ' \
                                           'Are your sure the participant has not been registered yet?' \
                                           'Go back to the previous page and double-check.' \
            # todo
        elif response['result']['ImportCount'] != 0 and status == 'not_registered':
            lime_warning['warning_color'] = 'MediumSeaGreen'
            lime_warning['warning_text'] = 'Participant successfully registered in LimeSurvey!' \
                                           'This is the initial registration. Please carefully check all data.' \
                                           'Typographical errors can result database corruption in case' \
                                           'of repeated measures!' \
                                           'Make sure to assign the participants to the required surveys at ' \
                                           + config._ls_url_login_
        elif response['result']['ImportCount'] != 0 and status == 'registered':
            lime_warning['warning_color'] = 'Tomato'
            lime_warning['warning_text'] = 'No participant is registered with this id!' \
                                           'Double-check participant data!' \
                                           'Only proceed if all details are correct and contact the developers.'

        lime_warning['warning_short'] = "LS: " + str((response['result']['ImportCount'], status))

        return redirect(url_for('pseudoID.preview'))

    return render_template('pseudoID/generate.html')


@bp.route('/preview', methods=('GET', 'POST'))
def preview():
    if request.method == 'GET':
        # access the global vars when redirected to the /preview page
        global subject, ids, lime_warning, logger
        logger.add_entry(ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])
    # return unpickeled dicts to access the keys directly in the html files
    return render_template('pseudoID/preview.html', **subject, **ids, **lime_warning)


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
    shutdown_server()
    return render_template('pseudoID/exit.html')
