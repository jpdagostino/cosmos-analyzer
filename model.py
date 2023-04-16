import tensorflow as tf
import os
from rich.progress import track


def train(dataframe, input, output, config):
    if not os.path.exists(config['save']):
        df = dataframe
        train_size = int(0.8 * len(df))
        train_df = df[:train_size]
        val_df = df[train_size:]
        
        # Define the TensorFlow model
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(64, activation=config['activation'], input_shape=(len(input),)),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(len(output))
        ])
        
        model.compile(optimizer=config['optimizer'], loss=config['loss'])
        
        for i in track(range(config['epochs']), "Training Model"):
            model.fit(train_df[input], train_df[output],
                      validation_data=(val_df[input], val_df[output]),
                      epochs=1, batch_size=config['batch'], verbose=0)
        model.save(config['save'])
    
    return tf.keras.models.load_model(config['save'])