# Auxiliary functions

import numpy as np
import pandas as pd
from IPython.display import Markdown, display
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

seed = 42

# ----------------------------------------------------------------------------
def structure_and_print_results(model_name, dataset_variation, y_true, y_pred, betta=1, digits=2, average=None):
    precision = precision_score(y_true, y_pred, average=average)
    recall = recall_score(y_true, y_pred, average=average)
    f1 = f1_score(y_true, y_pred, average=average)

    print('Model accuracy: ', accuracy_score(y_true, y_pred))
    print(classification_report(y_true, y_pred, digits=digits))

    n_classes = len(precision)
    frame_data = {
        'Model': [model_name] * n_classes,
        'Variation': [dataset_variation] * n_classes,
        'Target': ['F', 'M', 'N', 'S'],
        'Precision': precision,
        'Recall': recall,
        'F1_score': f1
    }
    return pd.DataFrame(frame_data)

##############################################################################
