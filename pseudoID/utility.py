import time
import os


class PseudonymLogger:
    def __init__(self):

        i = 1
        while os.path.exists('/LogFiles/log_' + str(i).zfill(4) + '.txt'):
            i += 1

        self.filename = '/LogFiles/log_' + str(i).zfill(4) + '.txt'

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
