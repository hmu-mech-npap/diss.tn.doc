#!/usr/bin/env ipython
import nptdms
import sys
import numpy as np

if sys.platform == "linux":
    my_path_noise = "/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/inverter/in1_20.1/Data.tdms"
    # my_path_clean = "/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/compressed air/ca0_10.1/Data.tdms"
else:
    my_path_noise = "D:/_data/WEL/WEL20220512/inverter/in1_5.1/Data.tdms"
    my_path_clean = "D:/_data/WEL/WEL20220512/inverter/in0_5.1/Data.tdms"

# clean_raw_sig = nptdms.TdmsFile.read(my_path_clean)
noise_raw_sig = nptdms.TdmsFile.read(my_path_noise)
# clean_chan_off_0 = clean_raw_sig["Wind Measurement"]["Wind2"]
noise_chan = noise_raw_sig["Wind Measurement"]["Wind2"]
fs_noise = 1 / noise_chan.properties["wf_increment"]
#
# Sample data
# fs_clean = 1 / clean_chan_off_0.properties["wf_increment"]
# T_clean = 1.0 / fs_clean  # Sample interval
# t_clean = np.linspace(0.0, 7.0, len(clean_chan_off_0))
# clean_signal = clean_chan_off_0.data  # np.sin(50 * 2.0 * np.pi * t)

# noisy_signal = noise_chan["Wind Measurement"]["Wind2"].data
T_noise = 1.0 / fs_noise  # Sample interval
t_noise = np.linspace(0.0, 7.0, len(noise_chan.data))
