import argparse
import os 
import logging
import json 
import sys
import uuid
import random
import builtins
from datetime import datetime
import time

logging.basicConfig(level=logging.NOTSET)

class SchemaProcess:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.schema = self.read_schema()
        self.generate_data()
    
    def read_schema(self):
        logging.info("reading schema")
        schema = self.args.schema

        # path case
        if os.path.isfile(schema):
            schema = open(schema)
        
        try: 
            return json.load(schema) # @TODO loads for string case
        except:
            logging.error("could not serialize JSON schema")
            sys.exit(1)
    
    def complete_filename(self, filename, prefix, i):
        match prefix:
            case 'count':
                new_prefix = i + 1
            case 'random':
                new_prefix = random.random() # @?
            case 'uuid':
                new_prefix = str(uuid.uuid4())
            case _:
                new_prefix = None
        if new_prefix:
            return f"{filename}_{new_prefix}.json"
        else:
            return f"{filename}.json"

    def generate_data(self):
        args = self.args
        
        logging.info("checking path")
        # create folder if it doesnt exist
        # @TODO check absolute path or from current directory
        if not os.path.exists(args.path):
            os.makedirs(args.path)
        
        # printing or saving to files
        printing = False
        if args.count == 0: printing = True

        # clear path
        for f in os.listdir(args.path):
            os.remove(os.path.join(args.path, f))

        # files count: iterate
        for i in range(args.count):
                pass
        
                new_data = self.parse_schema()

                if printing:
                    json_object = json.dumps(new_data, indent = 4) 
                    print(json_object)
                else:
                    # path: save files in path
                    # filename: first part of filename includes this
                    # file prefix: last part of filename includes this
                    # join path and filename_prefix
                    filename = self.complete_filename(args.name, args.prefix, i)
                    with open(os.path.join(args.path, filename), "w") as outfile:
                        json.dump(new_data, outfile)

        # data lines ?


    def parse_schema(self):
        '''
        Parse data schema and generate data based on it
        '''
        logging.info("parsing schema and generating data")

        new_data = dict()
        types = set(['timestamp', 'str', 'int'])

        for key, value in self.schema.items():
            value = value.split(':')
            data_type, what_to_generate = value

            if data_type not in types:
                logging.error("there is an invalid type on the schema")
                sys.exit(1)

            new_data[key] = self.get_generated(data_type, what_to_generate)
        
        return new_data
                
    def get_generated(self, data_type, what_to_generate):
        ERROR = "there has been an error with data types generation"
        # rand
        if what_to_generate == 'rand': 
            match data_type:
                case 'str':
                    return str(uuid.uuid4())
                case 'int':
                    return random.randint(0, 10000)
                case _:
                    logging.error(ERROR)
                    sys.exit(1)
        
        # timestamp
        elif data_type == 'timestamp':
            if what_to_generate:
                logging.warning('timestamp does not support any values and it will be ignored')
            # return datetime.now().timestamp()
            return time.time()
        # empty value
        elif not what_to_generate:
            match data_type:
                case 'str':
                    return ''
                case 'int':
                    return None
                case _:
                    logging.error(ERROR)
                    sys.exit(1)
        # rand(from, to)
        elif "(" in what_to_generate:
            if data_type == 'int':
                try:
                    return eval(what_to_generate.replace('rand','random.randint'))
                except:
                    logging.error(ERROR)
                    sys.exit(1)
            else:
                logging.error('rand(from, to) can only be used with int data type')
                sys.exit()
        # some other cases that can use eval() function
        else:
            # list
            try:
                eval_what_to_generate = eval(what_to_generate)
                if type(eval_what_to_generate) == list:
                    return random.choice(eval_what_to_generate)
            except:
            # stand alone value
            # @TODO if in schema there is “age”:”int:head”, it is an error and you must write about it in the console, because “head” could not be converted to int type
            # (check if what to generate type matches data type)
                match data_type:
                    case 'str':
                        return eval(f"{data_type}('{what_to_generate}')")
                    case 'int':
                        return eval(f"{data_type}({what_to_generate})")
                    case _:
                        logging.error(ERROR)
                        sys.exit(1)