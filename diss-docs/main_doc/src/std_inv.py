#!/usr/bin/env ipython
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, tf2sos, sosfilt, firwin
from data import noise_chan, clean_chan_off_0, fs_noise

# zero speed graph
noise_on_std = np.std(noise_chan.data)
clean_off_std = np.std(clean_chan_off_0)


fir_filt_coeff = firwin(numtaps=22,
                        fs=fs_noise,
                        cutoff=200,
                        )
sos_fir_mode = tf2sos(fir_filt_coeff, 1)
sos_filt_data = sosfilt(sos_fir_mode, noise_chan.data)
# print(noise_on_std, clean_off_std, np.std(sos_filt_data))

b, a = butter(2,
              200,   # This is in Hz !!!!
              # [min(noise_frequencies[L]), max(noise_frequencies[L]-1)],
              btype="low", fs=fs_noise)

# Apply filter
sos_out = tf2sos(b, a)
filtered_signal = sosfilt(sos_out, noise_chan.data)
filt_on_std = np.std(filtered_signal)
# function to add value labels

x_axis = ['Inverter Off', 'Inverter On',
          'Filtered IIR On \n(order 2)', 'Filtered FIR On \n(order 22)']
y_axis = [clean_off_std, noise_on_std, filt_on_std, np.std(sos_filt_data)]
labels = ["raw", "raw", "order 2", "order 22"]

plt.title("Comparison for Wind Tunnel measurements and inverter On and Off")
plt.xlabel("O m/s airflow")
plt.ylabel("standard deviation")
plt.bar(x_axis, y_axis)
plt.show()
