import argparse
import os 
import logging
import json 
import sys
import uuid
import random
import builtins
from datetime import datetime

logging.basicConfig(level=logging.NOTSET)

class SchemaProcess:
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.schema = self.read_schema()
        self.parse_schema()
    
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

    def parse_schema(self):
        '''
        Parse data schema and generate data based on it
        '''
        logging.info("parsing schema and generating data")

        new_data = dict()
        types = set(['timestamp', 'str', 'int'])

        print(self.schema)
        for key, value in self.schema.items():
            value = value.split(':')
            data_type, what_to_generate = value

            if data_type not in types:
                logging.error("there is an invalid type on the schema")
                sys.exit(1)

            new_data[key] = self.get_generated(data_type, what_to_generate)
        
        print(new_data)
                
    
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
                logging.error('timestamp does not support any values and it will be ignored')
            return datetime.now().timestamp()
        # empty value
        elif not what_to_generate:
            match data_type:
                case 'str':
                    return ''
                case 'int':
                    return None
                case _:
                    logging.error(ERROR)
        # rand(from, to)
        elif "(" in what_to_generate:
            try:
                return eval(what_to_generate.replace('rand','random.randint'))
            except:
                logging.error(ERROR)
        
        # some other cases that can use eval() function
        else:
            # list
            try:
                eval_what_to_generate = eval(what_to_generate)
                if type(eval_what_to_generate) == list:
                    return random.choice(eval_what_to_generate)
            except:
            # stand alone value
                match data_type:
                    case 'str':
                        return eval(f"{data_type}('{what_to_generate}')")
                    case 'int':
                        return eval(f"{data_type}({what_to_generate})")
                    case _:
                        logging.error(ERROR)