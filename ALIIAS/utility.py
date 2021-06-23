import os
from ALIIAS import config
import pkcs11
import os.path as path



class PseudonymLogger:
    def __init__(self):

        i = 1
        while os.path.exists(config.LOG_DIR + '/log_' + str(i).zfill(6) + '.txt'):
            i += 1

        self.filename = config.LOG_DIR + '/log_' + str(i).zfill(6) + '.txt'

        f = open(self.filename, 'w')
        f.close

    def add_entry(self, log_input):
        f = open(self.filename, 'a')
        f.write(log_input + '\n')
        f.close
        return None


def norm_str(str_in):
    char_dict = {ord('ä'): 'ae',
                 ord('ü'): 'ue',
                 ord('ö'): 'oe',
                 ord('ß'): 'ss',
                 ord(' '): None,
                 ord('-'): None,
                 ord(','): None,
                 ord('('): None,
                 ord(')'): None,
                 ord('.'): None,
                 }
    return str_in.lower().translate(char_dict)

def find_opensc_lib():
    path_opensc = config.settings['BASE']['opensc_path']
    try:
        lib = pkcs11.lib(path_opensc)
    except RuntimeError:
        try:
            # WIN shipped
            if not path.exists(config.OPENSC_DEFAULT_WINDOWS_ROOT_DIR):
                raise RuntimeError
            lib = pkcs11.lib(config.OPENSC_DEFAULT_WINDOWS_ROOT_DIR)
        except RuntimeError:
            try:
                # MACOS/Linux shipped
                if not path.exists(config.OPENSC_DEFAULT_MACOS_ROOT_DIR):
                    raise RuntimeError
                lib = pkcs11.lib(config.OPENSC_DEFAULT_MACOS_ROOT_DIR)
            except RuntimeError:
                try:
                    # WINDOWS default
                    if not path.exists(config.OPENSC_DEFAULT_WINDOWS):
                        raise RuntimeError
                    lib = pkcs11.lib(config.OPENSC_DEFAULT_WINDOWS)
                except RuntimeError:
                    try:
                        # LINUX default
                        if not path.exists(config.OPENSC_DEFAULT_LINUX):
                            raise RuntimeError
                        lib = pkcs11.lib(config.OPENSC_DEFAULT_LINUX)
                    except RuntimeError:
                        try:
                            # MACOS default
                            if not path.exists(config.OPENSC_DEFAULT_MACOS):
                                raise RuntimeError
                            lib = pkcs11.lib(config.OPENSC_DEFAULT_MACOS)
                        except RuntimeError:
                            try:
                                # ENV var
                                if not path.exists(config.OPENSC_DEFAULT_ENV):
                                    raise RuntimeError
                                lib = pkcs11.lib(config.OPENSC_DEFAULT_ENV)
                            except RuntimeError:
                                raise EnvironmentError("Unable to locate OpenSC!")
    return lib