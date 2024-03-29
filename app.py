import streamlit as st
import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import time

# Load the dataset
try:
    df = pd.read_csv(r'Dataset/dataset.csv')
except FileNotFoundError:
    st.error("Dataset not found")

# Load the trained model
try:
    model = joblib.load('best.pkl')
except FileNotFoundError:
    st.error("Model file not found")

def preprocess_input(transaction_amount, amount_paid, vehicle_type, lane_type, geographical_location):
    vehicle_type_encoder = LabelEncoder()
    lane_type_encoder = LabelEncoder()
    geographical_location_encoder = LabelEncoder()

    vehicle_type_encoder.fit(df['Vehicle_Type'])
    lane_type_encoder.fit(df['Lane_Type'])
    geographical_location_encoder.fit(df['Geographical_Location'])

    try:
        vehicle_type_encoded = vehicle_type_encoder.transform([vehicle_type])[0]
    except ValueError:
        vehicle_type_encoded = -1
        # st.error("Invalid vehicle type")
   
    try:
        lane_type_encoded = lane_type_encoder.transform([lane_type])[0]
    except ValueError:
        lane_type_encoded = -1 
        # st.error("Invalid lane type")
    
    try:
        geographical_location_encoded = geographical_location_encoder.transform([geographical_location])[0]
    except ValueError:
        geographical_location_encoded = -1
        st.error("Invalid geographical location")

    processed_input = np.array([[transaction_amount, amount_paid, vehicle_type_encoded, lane_type_encoded, geographical_location_encoded]])
    return processed_input

def predict_fraud(processed_input):
    prediction = model.predict(processed_input)
    return prediction[0]

# Streamlit UI
st.title('Real-time FASTAG Fraud Detection')
st.write('Enter the following information to detect fraud:')

col1, col2, col3 = st.columns(3)
try:
    vehicle_plate = col1.text_input('Vehicle Plate')
    fastag_id = col2.text_input('FASTAG ID')
    toll_booth_id = col3.text_input('Toll Booth ID')
except Exception as e:
    st.error(f"An error occurred: {e}")

col4, col5, col6 = st.columns(3)
try:
    vehicle_type = col4.selectbox('Vehicle Type', ['Motorcycle', 'Car', 'Sedan', 'SUV', 'Van', 'Bus', 'Truck'])
    vehicle_dimensions = col5.selectbox('Vehicle Dimensions', ['Small', 'Medium', 'Large'])
    lane_type = col6.selectbox('Lane Type', ['Regular', 'Express'])
except Exception as e:
    st.error(f"An error occurred: {e}")

col7, col8 = st.columns(2)
try:
    transaction_amount = col7.number_input('Transaction Amount')
    amount_paid = col8.number_input('Amount Paid')
except Exception as e:
    st.error(f"An error occurred: {e}")

try:
    geographical_location = st.text_input('Geographical Location (latitude, longitude)')
except Exception as e:
    st.error(f"An error occurred: {e}")

if st.button('Detect Fraud'):
    all_inputs_valid = True
    
    try:
        processed_input = preprocess_input(transaction_amount, amount_paid, vehicle_type, lane_type, geographical_location)
    except:
        all_inputs_valid = False
    
    if all_inputs_valid:
        with st.spinner('Please Wait...'):
            time.sleep(3) 
            prediction = predict_fraud(processed_input)
            if prediction == 1:
                st.write('Potential Fraud Detected')
            else:
                st.write('No Fraud Detected')
