import pandas as pd

# ======================================
# FAILURE PREDICTION ENGINE
# ======================================

def predict_failure(

    predictive_model,

    air_temperature,

    process_temperature,

    rotational_speed,

    torque,

    tool_wear

):

    prediction_features = pd.DataFrame({

        "Air temperature [K]":

        [air_temperature],

        "Process temperature [K]":

        [process_temperature],

        "Rotational speed [rpm]":

        [rotational_speed],

        "Torque [Nm]":

        [torque],

        "Tool wear [min]":

        [tool_wear]

    })

    prediction_probability = predictive_model.predict_proba(

        prediction_features

    )[:, 1]

    failure_probability = round(

        prediction_probability[0] * 100,

        2

    )

    return failure_probability