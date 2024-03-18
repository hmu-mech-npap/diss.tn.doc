"""Attempt to pyqtgraph package."""
from pathlib import Path
from nptdms import TdmsFile
from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.filters.fir import fir_factory_constructor
from pros_noisefiltering.filters.iir import filt_butter_factory
# a clone to use the time array for plotting with pyqtgraph
# added this to qt app cause its much faster and prettier
# than matplotlib.
# also more stylish and new looking
from pros_noisefiltering.plotting_funcs import Plotter_Class

# %%
FOLDER_FOR_DATA = Path(
    '/mnt/data_folder/measurements_12_05_22/new_record_prop_channel/')
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

# %% CONSTANTS
FIGSIZE_STD = (6, 6)
# Constant directories and names for the .tdms file structure
# Dir name
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

# %%
# Dir names for the Compressed air measurment
#
# =================================================
#
# Here the Compressed air measurements are imported
#
# =================================================
#
comp_air_dir = 'compressed air'

# %% preparing tdms files
# New renamed folders for rec version information
data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11 = 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1'
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10 = 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / comp_air_dir

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5,
                 data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                 data_CA_inv_1_WS_5, data_CA_inv_1_WS_10]

l_tdms_CA = []

for item in raw_signal_CA:
    x = TdmsFile(Path(f'{path_comp}/{item}', TDMS_FNAME))
    l_tdms_CA.append(x)

# %%
# [print(x) for x in l_tdms_CA[0][GROUP_NAME].channels()]
# %%
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'


df_tdms_0_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[0][GROUP_NAME][CHAN_NAME],
    desc='Inverter off, WS=0 (m/s)')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[3][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=0 (m/s)')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[5][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=10 (m/s)')

signal_analyzer = Plotter_Class()
a_fir = fir_factory_constructor(fir_order=32, fc_Hz=2000)
a_butter = filt_butter_factory(filt_order=2, fc_Hz=2000)

data_to_process = [df_tdms_0_0,
                   df_tdms_1_0,
                   df_tdms_1_10]
signal_analyzer.plot_signal_all_doms(signals=data_to_process,
                                     filt_func=a_butter,
                                     export_only=False,
                                     )
