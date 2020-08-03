import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')

first_name = None
subject = {}
ids = {}
lime_warning = {}

@bp.route('/generate', methods=('GET', 'POST'))
def generate():
    if request.method == 'POST':
        global subject
        subject['first_name'] = request.form['first_name']
        subject['family_name'] = request.form['family_name']
        subject['place_of_birth'] = request.form['place_of_birth']
        subject['date_of_birth'] = request.form['dob_d'] + '.' + \
                                   request.form['dob_m'] + '.' + \
                                   request.form['dob_y']

        subject['maiden_name'] = request.form['maiden_name']

        enc = Encryptor()
        long_id = enc.long_id(subject['first_name'] +
                              subject['family_name'] +
                              subject['place_of_birth'] +
                              subject['date_of_birth'] +
                              subject['maiden_name'])

        short_id = enc.short_id(long_id)

        global ids
        ids['short_id'] = short_id.decode('utf-8')
        ids['long_id'] = long_id.decode('utf-8')

        global lime_warning
        lime_warning['warning_color'] = 'tomato'
        lime_warning['warning_text'] = 'I should be red like a tomato'
        # limesurvey integration
        lscontrol = LimeSurveyController()
        response = lscontrol.register_in_cpdb(short_id.decode('utf-8'), long_id.decode('utf-8'))

        if response['result']['ImportCount'] == 0:
            flash("Participant already registered in LimeSurvey. No new participant added.")
        else:
            flash("Participant successfully registered in LimeSurvey!")

        return redirect(url_for('pseudoID.preview'))

    return render_template('pseudoID/generate.html')


@bp.route('/preview', methods=('GET', 'POST'))
def preview():
    if request.method == 'GET':
        # access the global vars when redirected to the /preview page
        global subject, ids, lime_warning
    # return unpickeled dicts to access the keys directly in the html files
    return render_template('pseudoID/preview.html', **subject, **ids, **lime_warning)


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@bp.route('/exit')
def exit():
    shutdown_server()
    return render_template('pseudoID/exit.html')
