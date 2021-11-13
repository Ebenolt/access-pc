import os, sys, ast
from configparser import ConfigParser
from datetime import datetime, date

class displayer(object):
    BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, CYAN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\33[36m', '\033[0m'

    def success(self, text, newline=True):
        text = self.GREEN + "Success : "+text+self.END
        if newline:
            text += "\n"
        self.display(text)

    def info(self, text, newline=True):
        text = self.YELLOW + "Info : "+text+self.END
        if newline:
            text += "\n"
        self.display(text)

    def error(self, text, newline=True):
        text = self.RED + "Error : "+text+self.END
        if newline:
            text += "\n"
        self.display(text)

    def verbose(self, text, newline=True):
        text = self.MAGENTA + text+self.END
        if newline:
            text += "\n"
        self.display(text)

    def validate(self, text):
        text = self.GREEN + text+self.END
        self.display(" "+text+"\n")

    def newline(self):
        self.display("\n")

    def display(self, text):
        sys.stdout.write(text)

class logger(object):
    logfile=""
    def __init__(self, logfile):
        if (not(os.path.isfile(logfile))):
            f = open(logfile, "a+", encoding="utf-8")
            f.close()
        self.logfile = logfile
        self.displayer = displayer()

    def log(self, text):
        now = datetime.datetime.now()
        current_time = now.strftime("%d/%m/%Y - %H:%M:%S")
        log_data = "["+current_time+"] "+str(text)
        f = open(self.logfile, "a+", encoding="utf-8")
        f.write(log_data+"\n")
        f.close()
        self.displayer.verbose(log_data)
import sys

class configReader(object):
    def __init__(self, conf_file):
        self.parser = ConfigParser()
        self.parser.read(conf_file)
    
    def read(self):
        result = {}
        for section in self.parser.sections():
            result[str(section)] = {}
            for element in self.parser[section]:
                if self.parser[section][element][0] in ["[", "{"]:
                    result[str(section)][str(element)] = ast.literal_eval(self.parser[section][element])
                else:
                    result[str(section)][str(element)] = self.parser[section][element]
        return result


class dateConverter():
        
    def strToDate(self, str: str, arch: str="%d/%m/%Y") -> date:
        return datetime.strptime(str, arch)
    
    def dateToStr(self, date: date, arch: str="%d/%m/%y") -> str:
        return date.strftime(arch)