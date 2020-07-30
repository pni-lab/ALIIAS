import time


class PseudonymLogger:
    def __init__(self):
        dt_string = time.strftime("%Y%m%d_%H%M%S")
        self.filename = '/LogFiles/log_' + dt_string + '.txt'
        f = open(self.filename, 'w')
        f.close

    def add_entry(self, log_input):
        f = open(self.filename, 'a')
        f.write(log_input + '\n')
        f.close
        return None
