from constants import *


class Log():  # no error detection, accessing imaginary files will get you fucked
    def __init__(self, file_name=LOG_FILE, separator=-1):
        self.file_name = file_name
        self.separator = separator
        self.log = []
        self.open()
        self.text = []

    def __str__(self):
        self.create_printable()
        res = ""
        for line in self.text:
            res += line + "\n"
        return res[:-1]

    def open(self):
        try:
            backup = open(self.file_name, "r")
            if self.separator != -1:
                for line in backup:
                    self.log.append([x.strip() for x in line.split(self.separator)])
            else:
                for line in backup:
                    self.log.append(line.strip())
            backup.close()
        except:
            ()

    def create_printable(self):
        self.text = []
        if self.separator != -1:
            if self.log != []:
                log_unit_size = len(self.log[0])
                lengths = [max([len(str(self.log[i][j])) for i in range(len(self.log))]) for j in range(log_unit_size)]
                for log_bit in self.log:
                    line = ""
                    for i in range(log_unit_size):
                        line += str(log_bit[i]) + " " * (lengths[i] - len(str(log_bit[i])))
                        if i < log_unit_size - 1:
                            line += " " + self.separator + " "
                    self.text.append(line)
        else:
            self.text = [str(log_bit) for log_bit in self.log]

    def save(self):
        self.create_printable()
        backup = open(self.file_name, "w")
        backup.write(self.__str__())
        backup.close()

    def add(self, log_bit):
        self.log.append(log_bit)

    def replace_log(self, new_log):
        self.log = new_log