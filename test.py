import pandas as pd
import numpy as np

# Generate a smoother EMG signal
time = np.linspace(0, 10 * np.pi, 1999)  # 1999 points over 10 cycles
emg_amplitude = 0.5 * np.sin(time) + 0.5 * np.random.normal(scale=0.05, size=1999)  # Reduced noise

# Create a DataFrame with a single row
df = pd.DataFrame([emg_amplitude], columns=[f'EMG Amplitude {i+1} (mV)' for i in range(1999)])

# Save to CSV
df.to_csv('emg_signal_single_row_cleaned.csv', index=False)
