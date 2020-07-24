import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from pseudoID.encryption import Encryptor
from pseudoID.ls_api_wrapper import LimeSurveyController

bp = Blueprint('pseudoID', __name__, url_prefix='/pseudoID')


@bp.route('/generate', methods=('GET', 'POST'))
def generate():
    if request.method == 'POST':
        first_name = request.form['first_name']
        family_name = request.form['family_name']
        place_of_birth = request.form['place_of_birth']
        date_of_birth = request.form['date_of_birth']
        maiden_name = request.form['maiden_name']

        enc = Encryptor()
        long_id = enc.long_id(first_name + family_name + place_of_birth + date_of_birth + maiden_name)
        short_id = enc.short_id(long_id)
        flash("ShortID:\n" + short_id.decode('utf-8'))
        mid = int(len(long_id.decode('utf-8'))/2)
        flash("LongID:\n" + long_id.decode('utf-8')[:mid] + "\n" + long_id.decode('utf-8')[mid:])

        # limesurvey integration
        lscontrol = LimeSurveyController()
        response = lscontrol.register_in_cpdb(short_id.decode('utf-8'), long_id.decode('utf-8'))

        if response['result']['ImportCount'] == 0:
            flash("Participant already registered in LimeSurvey. No new participant added.")
        else:
            flash("Participant successfully registered in LimeSurvey!")

    return render_template('pseudoID/generate.html')


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@bp.route('/exit')
def exit():
    shutdown_server()
    return render_template('pseudoID/exit.html')