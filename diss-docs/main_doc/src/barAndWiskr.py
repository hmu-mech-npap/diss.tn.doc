#!/usr/bin/env ipython
# %%
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
filt_on_fir_std = sosfilt(tf2sos(fir_filt_coeff, 1), noise_chan.data)


sos = butter(2,
             200,   # This is in Hz !!!!
             # [min(noise_frequencies[L]), max(noise_frequencies[L]-1)],
             btype="low", fs=fs_noise, output='sos')

# Apply filter
filt_on_iir_std = np.std(sosfilt(sos, noise_chan.data))
# function to add value labels

# Bar graph:
#       Adding the comparison for standard deviation to backup my filter
#       strategy.
x_axis = ['Inverter Off', 'Inverter On',
          'Filtered IIR On \n(order 2)', 'Filtered FIR On \n(order 22)']
y_axis = [clean_off_std, noise_on_std, filt_on_iir_std, np.std(filt_on_fir_std)]
labels = ["raw", "raw", "order 2", "order 22"]

plt.title("Comparison for Wind Tunnel measurements and inverter On and Off")
plt.xlabel("O m/s airflow")
plt.ylabel("standard deviation")
plt.bar(x_axis, y_axis)
plt.show()

# %%
"""
# TODO Explain the wisker plot in the document

The documentation says:


            Q2-1.5IQR   Q1   median  Q3   Q3+1.5IQR
                         |-----:-----|
         o      |--------|     :     |--------|  o  o
                         |-----:-----|
     lier                <----------->          fliers
                              IQR

- autorangebool, default: False
    When True and the data are distributed such that the 25th and 75th
    percentiles are equal, whis is set to (0, 100) such that the whisker ends
    are at the minimum and maximum of the data.

*reference* :
    - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
"""
labels = ["Inverter Off",
          "Inverter On",
          "Butterworth low-pass\nat 200Hz(IIR)",
          "Simple window low-pass\nat 200Hz(FIR)"]

plt.boxplot([clean_chan_off_0, noise_chan, sosfilt(sos, noise_chan.data), filt_on_fir_std],
            labels=labels,
            # notch=True,
            vert=True,
            patch_artist=False,
            meanline=True,
            showmeans=True,
            autorange=True,
            showfliers=False
            )
plt.title("Wind Tunnel measurements with airflow O m/s")
plt.xlabel("Filtering technics")
plt.ylabel("Mean value of recorded signal")
# plt.ylim(1.52, 1.72)
plt.show()
