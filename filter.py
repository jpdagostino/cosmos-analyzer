import numpy as np
from rich.progress import track
from sqlalchemy import insert
import uuid

def name_to_col(catalog_data, array):
    column_names = catalog_data[1].data.columns.names
    columns_dict = {name: index for index, name in enumerate(column_names)}
    return [columns_dict.get(name) for name in array]

def filter (connection, table, catalog_data, search):
    for sample in track(catalog_data[1].data, "Processing data"):
        working_data = tuple(sample[i] for i in search if i > -1)
        if not np.isnan(working_data).any():
            connection.execute(insert(table).values((str(uuid.uuid4()),) + working_data))