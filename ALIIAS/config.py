import configparser
import os
import sys

from flask import Flask

app = Flask(__name__)

DONGLE_PIN = None

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

OUTPUT_DIR = os.path.expanduser('~/ALIIAS')
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

LOG_DIR = os.path.join(OUTPUT_DIR, 'Logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

BC_DIR = os.path.join(OUTPUT_DIR, 'Barcodes')
if not os.path.exists(BC_DIR):
    os.makedirs(BC_DIR)

OPENSC_DEFAULT_LINUX = '/usr/lib/x86_64-linux-gnu/opensc-pkcs11.so'
OPENSC_DEFAULT_MACOS = '/usr//local/lib/opensc-pkcs11.so'
OPENSC_DEFAULT_WINDOWS = 'C:/Program Files/OpenSC Project/OpenSC/pkcs11/opensc-pkcs11.dll'
OPENSC_DEFAULT_WINDOWS_ROOT_DIR = os.path.join(ROOT_DIR, 'opensc-pkcs11.dll')
OPENSC_DEFAULT_MACOS_ROOT_DIR = os.path.join(ROOT_DIR, 'opensc-pkcs11.so')
OPENSC_DEFAULT_ENV = os.getenv('PKCS11_MODULE', "")

settings = configparser.ConfigParser()
settings.read(os.path.join(ROOT_DIR, 'settings.conf'))

HANDLER_DIR = os.path.join(ROOT_DIR, settings['BASE']['handler_name'] + '.txt')

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

