from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(debug=True)


# Load the trained linear regression model
model = joblib.load("trained_model1.pkl")

column_list = ['customerID', 'vehicle_no', 'Dest_states', 'supplierID', 'Current_Location', 'vehicleType', 'Material Shipped','Market/Regular '
               ,'Driver_Name', 'vehicle_states', 'Origin_states']

file_names = []
for column_name in column_list:
    file_name = "data/" + column_name.lower().replace(" ", "_").replace("/", "_") + ".pkl"
    file_names.append(file_name)


class DeliveryRequest(BaseModel):
    Current_Location: str
    TRANSPORTATION_DISTANCE_IN_KM: str
    vehicleType: str
    Driver_MobileNo: float
    supplierID:str
    Material_Shipped:str
    vehicle_states: str
    Dest_states: str


@app.post("/calculate-delay")
async def calculate_delay(request: DeliveryRequest):
    # Convert input data to pandas DataFrame
    data = pd.DataFrame([request.dict()])
    data["Material Shipped"] = data["Material_Shipped"]
    del data["Material_Shipped"]

    features = ['Current_Location', 'TRANSPORTATION_DISTANCE_IN_KM', 'vehicleType', 'Driver_MobileNo', 'supplierID',
                'Material Shipped', 'vehicle_states', 'Dest_states']

    # Reorder columns to match the order used during model training
    data = data.reindex(columns=features)

    # Make prediction using the loaded model
    prediction = model.predict(data)

    # Convert prediction to scalar integer
    prediction_scalar = int(prediction[0])

    # Return "ontime" if prediction is 1, else return 0
    if prediction_scalar == 1:
        result = "ontime"
    else:
        result = "Delay"

    return {"prediction": result}