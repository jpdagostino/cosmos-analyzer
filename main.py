import pandas as pd
import numpy as np
import yaml
from sqlalchemy import create_engine, Table, Column, Float, String, MetaData, inspect

from astropy.io import fits

import downloader
import extractor
import filter
import model
import profiler

with open('cosmos.yml', 'r') as file:
    options = yaml.safe_load(file)

path = options['catalog']['path']

if not downloader.check(path):
    path = downloader.download(path)
file = extractor.get_extracted_path(downloader.url_to_file(path))

print(f'Loading {file}')
catalog_data = fits.open(file)

inputs = options['catalog']['inputs']
outputs = options['catalog']['outputs']

inputs_indexes = filter.name_to_col(catalog_data, inputs)
outputs_indexes = filter.name_to_col(catalog_data, outputs)

search_indexes = inputs_indexes + outputs_indexes

engine = create_engine(options['database'])
metadata = MetaData()
connection = engine.connect()


search = options['catalog']['inputs'] + options['catalog']['outputs']

data_table = Table(options['data_table'], metadata, Column('id', String(36), primary_key=True), *[Column(column, Float) for column in search]) # Inputs + Outputs
profiled_table = Table(options['profiling_table'], metadata, Column('id', String(36), primary_key=True), *[Column(column, Float) for column in outputs]) # Outputs


if not inspect(engine).has_table(options['data_table']):
    metadata.create_all(engine, tables = [data_table]) 
    print(f'Filtering {file}')
    filter.filter(connection, data_table, catalog_data, search_indexes)
    print('Committing to Database')
    connection.commit()

df = pd.read_sql(data_table.select(), engine)


model = model.train(df, inputs, outputs, options['model'])

if not inspect(engine).has_table(options['profiling_table']):
    metadata.create_all(engine, tables = [profiled_table])

profiler.profile(connection, df, profiled_table, model, inputs, outputs)
connection.commit()

connection.close()