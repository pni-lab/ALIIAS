from pseudoID import config
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, send_from_directory
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController
from pseudoID.utility import PseudonymLogger, norm_str
from pseudoID.barcode_gen import generate_barcodeset

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')

possible_duplicate = False
already_registered = False
first_name = None
subject = {}
ids = {}
lime_warning = {}
enc = Encryptor()
show_pseudonym = {}

logger = PseudonymLogger()


@bp.route('/generate', methods=('GET', 'POST'))
def generate():
    # reset globals
    global possible_duplicate, already_registered
    already_registered = False
    possible_duplicate = False
    global show_pseudonym, subject, ids, lime_warning
    subject = {}
    ids = {}
    lime_warning = {}
    show_pseudonym = {}
    if request.method == 'POST':
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
        ids['short_id'] = short_id
        ids['exp_tag'] = request.form['exp_tag']
        ids['long_id'] = long_id

        # limesurvey integration
        lscontrol = LimeSurveyController()
        response = lscontrol.register_in_cpdb(short_id, long_id)

        if response['result']['ImportCount'] == 0 and status == 'registered':
            lime_warning['warning_color'] = 'MediumSeaGreen'
            lime_warning['warning_text'] = 'Participant already registered in LimeSurvey. \n ' \
                                           'No new participant added this time. ' \
                                           'Click "Proceed to the pseudonym" to obtain the short ID.'
            already_registered = True
        elif response['result']['ImportCount'] == 0 and status == 'not_registered':
            lime_warning['warning_color'] = 'Tomato'
            lime_warning['warning_text'] = 'ERROR: ID already registered in LimeSurvey. \n' \
                                           'Are your sure the participant has not been registered yet? ' \
                                           'If this participant has already been registered, click "undo", and choose' \
                                           '"yes" at the first point. ' \
                                           'If you are sure that this participant has not been registered yet, ' \
                                           'click "Proceed to the pseudonym" and CONTACT THE DEVELOPERS! ' \
                                           '(possible duplicate)!'
            possible_duplicate = True
        elif response['result']['ImportCount'] != 0 and status == 'not_registered':
            lime_warning['warning_color'] = 'MediumSeaGreen'
            lime_warning['warning_text'] = 'Participant successfully registered in LimeSurvey!\n' \
                                           'This is the initial registration. Please carefully check all data. ' \
                                           'Typographical errors can result database corruption! ' \
                                           'Make sure to assign the participants to the required surveys at ' \
                                           + config._ls_url_login_
        elif response['result']['ImportCount'] != 0 and status == 'registered':
            lime_warning['warning_color'] = 'Tomato'
            lime_warning['warning_text'] = 'ERROR: No participant has previously been registered with this id! \n' \
                                           'Double-check participant data! ' \
                                           'In case of typographical error, click "Undo" to ' \
                                           'logically delete this transaction. ' \
                                           'If all details are correct, you can now proceed with the experiment, but ' \
                                           'make sure to CONTACT THE DEVELOPERS!'

        lime_warning['warning_short'] = "LS: " + str((response['result']['ImportCount'], status))

        logger.add_entry(
            "PREVIEW : " + ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])

        return redirect(url_for('pseudoID.preview'))

    return render_template('pseudoID/generate.html', _exp_tag_=config._exp_tag_)


@bp.route('/preview', methods=('GET', 'POST'))
def preview():
    barcodes = []
    global possible_duplicate
    global show_pseudonym
    if request.method == 'GET':
        # access the global vars when redirected to the /preview page
        global subject, ids, lime_warning, logger
    # return unpickeled dicts to access the keys directly in the html files

    if request.method == 'POST':
        if request.form['proceed'] == "No! Undo Transaction." \
                or request.form['proceed'] == "Undo Transaction" \
                or request.form['proceed'] == "Undo Transaction (logically delete participant)":
            logger.add_entry(
                "WITHDRAWN: " + ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])
            if not possible_duplicate and not already_registered:
                # logically delete this participant from LimeSurvey (if not yet registered before)
                logger.add_entry(
                    "DELETE: " + ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])
                lscontrol = LimeSurveyController()
                response = lscontrol.register_in_cpdb(ids['short_id'], ids['long_id'], logical_delete=True)
            subject = ids = lime_warning = None
            return redirect(url_for('pseudoID.generate'))

        if request.form['proceed'] == "Yes! Proceed to the pseudonym.":
            if possible_duplicate:
                # add a random character to the shortID to eliminate the duplicate
                import random
                ids['short_id'] = ids['short_id'] + random.choice(config._hexchars_)
                # add participant with the modified ID
                lscontrol = LimeSurveyController()
                response = lscontrol.register_in_cpdb(ids['short_id'], ids['long_id'])
                logger.add_entry(
                    "ACCEPTED_DUPLICATE: " + ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids[
                        'long_id'])
            else:
                logger.add_entry(
                    "ACCEPTED:  " + ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])

            barcodes = generate_barcodeset(ids['short_id'])
            # for f in barcodes:
            #    send_from_directory('static', f)

            show_pseudonym['show_pseudonym'] = True

        if request.form['proceed'] == "New participant":
            return redirect(url_for('pseudoID.generate'))

        if request.form['proceed'] == "Exit PseudoID":
            # shutdown_server()
            return redirect(url_for('pseudoID.exit'))

    return render_template('pseudoID/preview.html', items=barcodes, **subject, **ids, **lime_warning, **show_pseudonym)


# @bp.route('/finalize', methods=('GET', 'POST'))
# def preview():
#    if request.method == 'GET':
#        # access the global vars when redirected to the /preview page
#        global subject, ids, lime_warning, logger
#        logger.add_entry(ids['short_id'] + '\t' + lime_warning['warning_short'] + '\t' + ids['long_id'])
#    # return unpickeled dicts to access the keys directly in the html files
#    return render_template('pseudoID/preview.html', **subject, **ids, **lime_warning)


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
