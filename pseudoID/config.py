import pickle
from Crypto.Cipher import AES
from flask import Flask, redirect, url_for
import configparser
import os, sys

app = Flask(__name__)

if 'linux' in sys.platform:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root
else:
    if getattr(sys, 'frozen', False):
        ROOT_DIR = os.path.dirname(sys.executable)
        running_mode = 'Frozen/executable'
    else:
        try:
            app_full_path = os.path.realpath(__file__)
            ROOT_DIR = os.path.dirname(app_full_path)
            running_mode = "Non-interactive (e.g. 'python myapp.py')"
        except NameError:
            ROOT_DIR = os.getcwd()
            running_mode = 'Interactive'



OUTPUT_DIR = os.path.expanduser('~/pseudoID')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

LOG_DIR = os.path.join(OUTPUT_DIR, 'Logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

BC_DIR = os.path.join(OUTPUT_DIR, 'Barcodes')
if not os.path.exists(BC_DIR):
    os.makedirs(BC_DIR)

settings = configparser.ConfigParser()
settings.read(os.path.join(ROOT_DIR, 'settings.conf'))

HANDLER_DIR = os.path.join(ROOT_DIR, 'handler.txt')

# ToDo: remove the hard coded user key
_user_key_ = b'\xbf\xabb]\xb3\x94\xd8}>Z\x84QO\xdb\tD\xb1wl\xef@7\xa9$\x91\xb0>#\xe4\x10\x07u'

_pseudonym_key_encrypted_ = (
    b'\xf2\xe6\xaf\xc6\x81\x06\xb3~\xd19\x1f\x0b\x01zE\x8ccn\xea\xcb\xd1N\x11H\xf3\xc5\x99\x10#\x0f\xe2\xdc',
    b'\xbd2n\xb9\x91\xff\x82\xec\xb8\xa3\xd7\xefw@\xb73')

_exp_tag_ = {
    "": "",
    "Pre": "-pre",
    "Post": "-post",
    "Baseline": "-bsl",
    "Week 1": "-wk1",
    "Week 2": "-wk2",
    "Week 3": "-wk3",
    "Week 4": "-wk4",
}

_site_tag_ = {
    "Test": "t",
    "A01": "1",
    "A02": "2",
    "A03": "3",
    "A04": "4",
    "A06": "6",
    "A07": "7",
    "A08": "8",
    "A09": "9",
    "A11": "a",
    "A12": "b",
    "A13": "c",
    "A15": "e",
    "A16": "f",
}

_warnings_ = {'known': 'Participant already registered in LimeSurvey. \n ' \
                       'No new participant added this time. ' \
                       'Click "Proceed to the pseudonym" to obtain the short ID.',

              'duplicate': 'DUPLICATE ERROR: short ID (but not longID) already registered in LimeSurvey. \n' \
                           'Are your sure the participant has not been registered yet? ' \
                           'If this participant has already been registered, click "undo", and choose' \
                           '"yes" at the first point. ' \
                           'If you are sure that this participant has not been registered yet, ' \
                           'click "Proceed to the pseudonym" and CONTACT THE DEVELOPERS! ' \
                           '(possible duplicate)!',

              'new': 'Participant successfully registered in LimeSurvey!\n' \
                     'This is the initial registration. Please carefully check all data. ' \
                     'Typographical errors can result database corruption! ' \
                     'Make sure to assign the participants to the required surveys at ' \
                     + settings['LIMESURVEY']['url_login'],

              'unknown': 'ERROR: No participant has previously been registered with this id! \n' \
                         'Double-check participant data! ' \
                         'In case of typographical error, click "Undo" to ' \
                         'logically delete this transaction. ' \
                         'If all details are correct, you can now proceed with the experiment, but ' \
                         'make sure to CONTACT THE DEVELOPERS!'}

