
from keras.models import Sequential
from keras.layers import Dense, Flatten

# cree une fonction qui retourne un model sequentiel

def AgentDQN():

    model = Sequential()
    model.add(Dense(units=130, activation='relu', input_dim=27, kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(units=250, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(units=140, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(units=60, activation='relu', kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.add(Dense(units=9, kernel_initializer='random_uniform', bias_initializer='zeros'))
    model.compile(optimizer='adam', loss='mean_squared_error')

    return model
