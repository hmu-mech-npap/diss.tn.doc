# %%
import sys
from pathlib import Path
import nptdms
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, firwin, sosfiltfilt, filtfilt

# configure the font size for all the characters
font_config = {'size': 12}
plt.rc('font', **font_config)

# behave nice for both
if sys.platform == "linux":
    my_path_noise = Path("/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/inverter/in1_10.1/Data.tdms")
elif sys.platform == "windows":
    my_path_noise = Path(
        "D:/_data/WEL/WEL20220512/inverter/in1_10.1/Data.tdms")

noise_raw_sig = nptdms.TdmsFile.read(my_path_noise)
noise_chan = noise_raw_sig["Wind Measurement"]["Wind2"]
fs_noise = 1 / noise_chan.properties["wf_increment"]

T_noise = 1.0 / fs_noise  # Sample interval
t_noise = np.linspace(0.0, 7.0, len(noise_chan.data))

# zero speed graph
noise_on_std = np.std(noise_chan.data)
# clean_off_std = np.std(clean_chan_off_0)

fir_filt_coeff = firwin(numtaps=22,
                        fs=fs_noise,
                        cutoff=200,
                        )
filt_on_fir = filtfilt(fir_filt_coeff, 1, noise_chan.data)

sos_butter_out = butter(2,
                        200,   # This is in Hz !!!!
                        # [20, 250],
                        btype="lowpass", fs=fs_noise, output='sos')

# Apply filter
filt_on_iir = sosfiltfilt(sos_butter_out, noise_chan.data)

# %%
# Bar graph:
#       Adding the comparison for standard deviation to backup my filter
#       strategy.
#       'Inverter Off',
#       "raw",
x_axis = ['Inverter On',
          'Filtered IIR On \n(order 2)', 'Filtered FIR On \n(order 22)']
# clean_off_std,
y_axis = [noise_on_std, np.std(filt_on_iir), np.std(filt_on_fir)]
labels = ["raw", "order 2", "order 22"]

# plt.title("Comparison for wind tunnel measurements\nand inverter On for 10 m/s airflow",
plt.title("Comparison for wind tunnel measurements\nand inverter On for 10 m/s airflow",
          )
# plt.xlabel("10 m/s airflow")
plt.ylabel("standard deviation")
plt.bar(x_axis, y_axis)
# plt.show()
plt.savefig('./std_wt_new.png')


# %%
# TODO Explain the wisker plot in the document.

# The documentation says:


#             Q1-1.5IQR   Q1   median  Q3   Q3+1.5IQR
#                          |-----:-----|
#          o      |--------|     :     |--------|  o  o
#                          |-----:-----|
#      lier                <----------->          fliers
#                               IQR

# - autorangebool, default: False
#     When True and the data are distributed such that the 25th and 75th
#     percentiles are equal, whis is set to (0, 100) such that the whisker ends
#     are at the minimum and maximum of the data.

# *reference* :
#     - https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.boxplot.html
#     - https://www.hackmath.net/en/calculator/quartile-q1-q3

# labels = ["Inverter On",
#           "Butterworth\nlow-pass\nat 200Hz(IIR)",
#           "Simple window\nlow-pass\nat 200Hz(FIR)"]

# fig, ax = plt.subplots()
# ax.boxplot([noise_chan, sosfiltfilt(sos_butter_out, noise_chan.data, axis=-1),
#             filt_on_fir],
#            labels=labels,
#            notch=True,
#            vert=True,
#            patch_artist=True,
#            meanline=True,
#            showmeans=True,
#            autorange=True,
#            showfliers=True
#            )
# # plt.title("wind tunnel measurements with airflow 10 m/s")
# plt.title("Compressed air measurements with airflow 10 m/s")
# plt.xlabel("Filtering technics")
# plt.ylabel("Mean value of recorded signal")
# # ax.set_xlim(0.5, 2.5)
# axins = ax.inset_axes([0.7, 0.7, 0.55, 0.55], ylim=(1.76, 2.5))
# # lbl=[]
# axins.boxplot([noise_chan,
#                sosfiltfilt(sos_butter_out,
#                            noise_chan.data, axis=-1),
#                filt_on_fir],
#               # labels=labels,
#               notch=True,
#               vert=True,
#               patch_artist=True,
#               meanline=True,
#               showmeans=True,
#               autorange=True,
#               showfliers=True,
#               )

# axins.set_xticklabels([])
# ax.indicate_inset_zoom(axins, edgecolor="black")  #.set_linestyle(":")
# plt.savefig("./whiskr_ca.png", bbox_inches="tight")
# plt.show()

# %%
