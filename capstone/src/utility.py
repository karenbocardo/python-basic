import argparse
import json
import os
import time
import random
import configparser
import logging
import uuid
import multiprocessing
import sys

logging.basicConfig(level=logging.NOTSET)

from schema import SchemaProcess
class ConsoleUtility:
    def __init__(self):
        # parser
        self.parser = argparse.ArgumentParser(prog="capstone", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.default = self.read_defaults()
        self.setup_args()
        self.args = self.parse_args()
        self.analyze_args()

        # process schema
        self.process = SchemaProcess(self.args)

    def read_defaults(self):
        # config parser for defaults
        config = configparser.ConfigParser()
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, "default.ini")
        config.read(initfile)
        return config['DEFAULT'] # ?

    def setup_args(self):
        parser = self.parser
        default = self.default

        # arguments
        parser.add_argument("path", help="Where all files need to save") # path to save files
        parser.add_argument("-count", "--file_count", dest="count", default=default['-count'], type=int, action='store',
                            help="How much json files to generate")
        parser.add_argument("-name", "--file_name", dest="name", default=default['-name'], type=str, action='store',
                            help="Base file_name. If there is no prefix, the final file name will be file_name.json. With prefix full file name will be file_name_file_prefix.json")
        parser.add_argument("-pref", "--prefix", dest="prefix", default=default['-pref'], type=str, action='store', choices=['count', 'random', 'uuid'],
                            help="What prefix for file name to use if more than 1 file needs to be generated")
        parser.add_argument("-sch", "--data_schema", dest="schema", default=default['-sch'], type=str, action='store', #required=True,
                            help="It’s a string with json schema. \nIt could be loaded in two ways: \n1) With path to json file with schema \n2) with schema entered to command line. \nData Schema must support all protocols that are described in “Data Schema Parse”")
        parser.add_argument("-lines", "--data_lines", dest="lines", default=default['-lines'], type=int, action='store',
                            help="Count of lines for each file. Default, for example: 1000.")
        parser.add_argument("-clr", "--clear_path", dest="clear", action='store_true', default=self.parse_str_to_bool(default['-clr']),
                            help="If this flag is on, before the script starts creating new data files, all files in path_to_save_files that match file_name will be deleted.")
        parser.add_argument("-multi", "--multiprocessing", dest="multiprocessing", default=default['-multi'], type=int, action='store',
                            help="The number of processes used to create files. \nDivides the “files_count” value equally and starts N processes to create an equal number of files in parallel. \nOptional argument. Default value: 1.")
    
    def parse_args(self):
        logging.info("parsing arguments")
        # parsing user defined arguments
        parser = self.parser
        logging.info("parsing args")
        return parser.parse_args()
    
    def analyze_args(self):
        logging.info("analyzing arguments")
        args = self.args
        # path

        # files count
        if args.count < 0:
            logging.error("number of files must be positive")
            sys.exit(1)

        # multiprocessing
        if args.multiprocessing < 0 :
            logging.error("number of processes for multiprocessing must be positive")
            sys.exit(1)
        elif args.multiprocessing > os.cpu_count(): 
            args.multiprocessing = os.cpu_count()

        p = multiprocessing.Pool(processes=args.multiprocessing)


    def parse_str_to_bool(self, string: str):
        '''
        Reads string and parses it to boolean. In case it is not 'True' or 'False' it returns just the string.
        '''
        d = {'True': True, 'False': False}
        return d.get(string, string)