import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

# ======================================
# LOAD DATASET
# ======================================

df = pd.read_csv(
    "../datasets/ai4i2020.csv"
)

# ======================================
# FEATURES
# ======================================

X = df[[

    'Air temperature [K]',

    'Process temperature [K]',

    'Rotational speed [rpm]',

    'Torque [Nm]',

    'Tool wear [min]'

]]

# ======================================
# TARGET
# ======================================

y = df['Machine failure']

# ======================================
# TRAIN TEST SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# ======================================
# MODEL
# ======================================

model = RandomForestClassifier(

    n_estimators=200,

    random_state=42

)

# ======================================
# TRAIN
# ======================================

model.fit(
    X_train,
    y_train
)

# ======================================
# PREDICT
# ======================================

predictions = model.predict(
    X_test
)

# ======================================
# EVALUATION
# ======================================

accuracy = accuracy_score(
    y_test,
    predictions
)

print(f"Model Accuracy: {accuracy}")

print(

    classification_report(

        y_test,

        predictions

    )

)

# ======================================
# SAVE MODEL
# ======================================

joblib.dump(

    model,

    "predictive_maintenance_model.pkl"

)

print(
    "Model saved successfully"
)