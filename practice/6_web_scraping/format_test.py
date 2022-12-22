import pandas as pd
from tabulate import tabulate

formats = ['plain',
            'simple',
            'github',
            'grid',
            'fancy_grid',
            'pipe',
            'orgtbl',
            'jira',
            'presto',
            'pretty',
            'psql',
            'rst',
            'mediawiki',
            'moinmoin',
            'youtrack',
            'html',
            'latex',
            'latex_raw',
            'latex_booktabs',
            'textile']

df = pd.read_csv('output.csv', sep='\t')
for format in formats:
    print('\n', format)
    print(tabulate(df, headers = 'keys', tablefmt = format))