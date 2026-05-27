import streamlit as st
import serial
import numpy as np
import matplotlib.pyplot as plt

# SERIAL PORT
ser = serial.Serial('COM3', 115200)

st.title("Smart Yoga Mat Heatmap")

placeholder = st.empty()

while True:

    try:
        line = ser.readline().decode().strip()

        values = list(map(int, line.split(',')))

        if len(values) == 13:

            # Arrange sensors visually
            heatmap = np.array([
                [values[0], values[1], 0, values[2], values[3]],
                [values[4], values[5], values[6], values[7], values[8]],
                [values[9], values[10], 0, values[11], values[12]]
            ])

            fig, ax = plt.subplots()

            cax = ax.imshow(heatmap)

            plt.colorbar(cax)

            placeholder.pyplot(fig)

    except:
        pass