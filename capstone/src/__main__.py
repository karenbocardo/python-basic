from utility import ConsoleUtility

cu = ConsoleUtility()

# run:
# python3 src . --file_count=3 --file_name=super_data --prefix=count --data_schema=src/schema.json
# python3 src . --file_count=3 --file_name=super_data --prefix=count --multiprocessing=4 --data_schema="{\"date\": \"timestamp:\",\"name\": \"str:rand\",\"type\": \"['client', 'partner', 'government']\",\"age\": \"int:rand(1, 90)\"}"
# python3 src . --file_count=3 --file_name=super_data --prefix=count --multiprocessing=4 --data_schema="{"date":"timestamp:", "name": "str:rand", "type":"['client', 'partner', 'government']", "age": "int:rand(1, 90)"}"

# run to save output inside out/ and only one data line:
# python3 src out --file_count=3 --file_name=super_data --prefix=count --data_schema=src/schema.json

# multiple data lines:
# python3 src out --file_count=3 --file_name=super_data --prefix=count --data_lines=3 --data_schema=src/schema.json