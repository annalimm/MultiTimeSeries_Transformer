from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import *
from tensorflow.keras.layers import *


def transformer_encoder(inputs, key_dim, num_heads, ff_dim, dropout=0):
    
    # "EMBEDDING LAYER"
    x = layers.LayerNormalization(epsilon=1e-6)(inputs)
    
    # "ATTENTION LAYER"
    x = layers.MultiHeadAttention(key_dim=key_dim, num_heads=num_heads, dropout=dropout)(x, x)
    x = layers.Dropout(dropout)(x)
    res = x + inputs
    
    # FEED FORWARD Part - can stick anything here or just delete the whole section - it will still work. 
    x = layers.LayerNormalization(epsilon=1e-6)(res)
    x = layers.Conv1D(filters=ff_dim, kernel_size=1, activation = "relu")(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Conv1D(filters=inputs.shape[-1], kernel_size=1)(x)
    return x + res


def build_model(input_shape,
                key_dim,   # Q, K, V dimensionality 
                num_heads, # Number of attention heads
                ff_dim,    # The number of filters in the convolutional layer
                           # Hidden layer size in feed forward network inside transformer?
                num_transformer_blocks,
                mlp_units,
                dropout=0,
                mlp_dropout=0,):
    
    inputs = keras.Input(shape=input_shape)
    x = inputs
    
    for _ in range(num_transformer_blocks):   
        x = transformer_encoder(x, key_dim, num_heads, ff_dim, dropout)

    x = layers.GlobalAveragePooling1D(data_format="channels_first")(x)
    
    for dim in mlp_units:
        x = layers.Dense(dim, activation="elu")(x)
        x = layers.Dropout(mlp_dropout)(x)
        
    outputs = layers.Dense(1, activation="linear")(x) #this is a pass-through
    
    return keras.Model(inputs, outputs)


