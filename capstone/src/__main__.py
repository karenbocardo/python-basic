from utility import ConsoleUtility

cu = ConsoleUtility()

# run:
# python3 src . --file_count=3 --file_name=super_data --prefix=count --data_schema=src/schema.json
# python3 src . --file_count=3 --file_name=super_data --prefix=count --multiprocessing=4 --data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"
# python3 src . --file_count=3 --file_name=super_data --prefix=count --multiprocessing=4 --data_schema="{"date":"timestamp:", "name": "str:rand", "type":"['client', 'partner', 'government']", "age": "int:rand(1, 90)"}"