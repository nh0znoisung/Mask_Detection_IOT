import tensorflow as tf
import numpy as np

class F1History(tf.keras.callbacks.Callback):

    def __init__(self, test_dataset):
        super(F1History, self).__init__()
        self.test_dataset =test_dataset
        self.history = {
            'val_precision':[],
            'val_recall':[],
            'val_f1':[],
        }

    def on_epoch_end(self, epoch, logs={}):

        logs['val_precision'] = 0 
        logs['val_recall'] = 0
        logs['val_f1'] = 0

        true_pos = 0
        pred_pos = 0
        pos = 0
        for i,j in self.test_dataset:
            y = self.model.predict(i)
            y = np.round(y[:,0])
            j = j.numpy()
            true_pos += sum(y*j)
            pred_pos += sum(y)
            pos += sum(j)

        logs['val_precision'] = true_pos/pred_pos
        logs['val_recall'] = true_pos/pos
        logs['val_f1'] = 2*logs['val_precision']*logs['val_recall']/(logs['val_recall']+logs['val_precision'])
        
        self.history['val_precision'] += [logs['val_precision']]
        self.history['val_recall'] += [logs['val_recall']]
        self.history['val_f1'] += [logs['val_f1']]
        
        print(logs)
        # X_valid, y_valid = self.validation[0], self.validation[1]
        # y_val_pred = (self.model.predict(X_valid).ravel()>0.5)+0
        # val_score = f1_score(y_valid, y_val_pred)
        # logs['F1_score_train'] = np.round(score, 5)
        # logs['F1_score_val'] = np.round(val_score, 5)