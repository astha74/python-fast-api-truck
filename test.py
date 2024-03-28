import joblib
import json


def convert_pkl_to_json(pkl_file_path, json_file_path):
    try:
        # Open the pickle file for reading binary data
        with open(pkl_file_path, 'rb') as pkl_file:
            # Load data from the pickle file
            data = joblib.load(pkl_file)

        # Convert int64 values to native Python integers
        data_serializable = {key: int(value) for key, value in data.items()}
        # Convert the data to JSON format
        json_data = json.dumps(data_serializable, indent=4)

        # Write the JSON data to a file
        with open(json_file_path, 'w') as json_file:
            json_file.write(json_data)

        print(f"Conversion successful. JSON data written to {json_file_path}")
    except Exception as e:
        print(f"Error: {e}")


file_names = []
column_list = ['customerID', 'vehicle_no', 'Dest_states', 'supplierID', 'Current_Location', 'vehicleType', 'Material Shipped','Market/Regular '
               ,'Driver_Name', 'vehicle_states', 'Origin_states']
for column_name in column_list:
    file_name = "data/" + column_name.lower().replace(" ", "_").replace("/", "_") + ".pkl"
    file_names.append(file_name)

  # Path where you want to store the JSON data

# Call the function to convert .pkl to .jso
for file in file_names:
    json_file_path = file.split(".")[0] + ".json"
    convert_pkl_to_json(file, json_file_path)
