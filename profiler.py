import numpy as np
from sqlalchemy import insert
from rich.progress import track

def profile(connection, dataframe, table, model, input_cols, output_cols):
     for index, row in track(dataframe.iterrows(), "Profiling Data"):
        array = np.array(row.values)
        uuid = str(array[0])
        array = np.delete(array, 0) # Delete the uuid
        
        input = np.reshape(array[:len(input_cols)], (1, len(input_cols)))
        output = np.reshape(array[len(input_cols):len(input_cols)+len(output_cols)], (1, len(output_cols)))
        
        prediction = model.predict([input.astype(np.float32)], verbose=0)
        pe = []
        for i in range(len(output[0])):
            measured = prediction[0][i]
            accepted = output[0][i]
            pe.append(np.abs((measured - accepted)  /accepted) * 100)
        connection.execute(insert(table).values([uuid] + pe))