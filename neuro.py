import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt


def reconstr(file):
    with open(file) as f:
        new_list_lines = list()
        for row in f:
            new_list = list()
            parse = row.strip('[]').replace(' ', '').replace(']\n', '').replace("'", '').replace('\n', '').split(',')
            for el in parse:
                el = float(el)
                if el < 0:
                    el += 90
                new_list.append(el)
            new_list_lines.append(new_list)
    return new_list_lines


if __name__ == '__main__':
    input_edudates = np.array(reconstr('input.txt')) / np.array([1050.0, 15.0, 3.0, 3.0, 1050.0, 15.0, 3.0])
    input_test = np.array(reconstr('input_check.txt') / np.array([1050.0, 15.0, 3.0, 3.0, 1050.0, 15.0, 3.0]))
    output_edudates = np.array(reconstr('output.txt'))
    output_test = np.array(reconstr('output_check.txt'))
    inp = tf.constant(input_edudates)

    model = keras.Sequential()
    model.add(tf.keras.layers.Dense(30, input_shape=(7,), activation='relu'))
    model.add(tf.keras.layers.Dense(15, activation='relu'))
    model.add(tf.keras.layers.Dense(3, activation='softmax'))
    print(model.summary())

    optimiz = keras.optimizers.Adam(learning_rate=0.0001)
    model.compile(optimizer=optimiz, loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print(model.summary())
    hist = model.fit(input_edudates, output_edudates, batch_size=2, epochs=900, validation_split=0.15)
    plt.plot(list(range(1, len(hist.history['loss']) + 1)), hist.history['loss'])
    plt.plot(list(range(1, len(hist.history['val_loss']) + 1)), hist.history['val_loss'])
    plt.grid(True)
    plt.show()
    model.save('model')
    print(model.evaluate(input_test, output_test))
    print(model.predict(input_test[:5]))