print ("Hallo world!")

from pathlib import Path
from matplotlib import pyplot as plt
import scipy.signal as signal
import numpy as np
import pandas as pd

from nptdms import TdmsFile
import nptdms


import pros_noisefiltering as pnf
from pros_noisefiltering.gen_functions import (spect,plot_spect_comb2,plot_FFT,
                                               Signals_for_fft_plot, Fft_Plot_info, Axis_titles)

from pros_noisefiltering.WT_NoiProc import WT_NoiseChannelProc
from pros_noisefiltering.Graph_data_container import Graph_data_container

def apply_filter(ds:np.ndarray, fs_Hz:float, fc_Hz = 100, filt_order = 2 ):
                 # filter cutoff frequency
    sos = signal.butter(filt_order , fc_Hz, 'lp', fs=fs_Hz, output='sos')
    filtered = signal.sosfilt(sos, ds-ds[0])+ds[0]
    return filtered

#CONSTANTS

FOLDER_FOR_DATA = Path('/mnt/data_folder')/'measurements_12_05_22/new_record_prop_channel/'
if not FOLDER_FOR_DATA.exists():
    FOLDER_FOR_DATA = Path('D:/_data/WEL/WEL20220512/')

TDMS_FNAME = 'Data.tdms'

# Dir names for the Compressed air measurment
comp_air_dir = 'compressed air'

# New renamed folders for rec version information
data_CA_inv_0_WS_0 = 'ca0_0.1'
data_CA_inv_0_WS_5 = 'ca0_5.1'
data_CA_inv_0_WS_11= 'ca0_10.1'
data_CA_inv_1_WS_0 = 'ca1_0.1'
data_CA_inv_1_WS_5 = 'ca1_5.1'
data_CA_inv_1_WS_10= 'ca1_10.1'

path_comp = FOLDER_FOR_DATA / comp_air_dir

# CA stands for compressed air

raw_signal_CA = [data_CA_inv_0_WS_0, data_CA_inv_0_WS_5,
                data_CA_inv_0_WS_11, data_CA_inv_1_WS_0,
                data_CA_inv_1_WS_5, data_CA_inv_1_WS_10 ]

tdms_raw_CA = []

for item in raw_signal_CA:
    y = f'{path_comp}/{item}'
    x=TdmsFile( Path( y , TDMS_FNAME))
    tdms_raw_CA.append(x)

GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

df_tdms_i0_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=0')
df_tdms_i0_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=5')
df_tdms_i0_w10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter off, WS=11')
df_tdms_i1_w0 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=0')
df_tdms_i1_w5 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=5')
df_tdms_i1_w10 = WT_NoiseChannelProc.from_tdms(tdms_raw_CA[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter on, WS=10')

fc_Hz=2000
plot_spect_comb2([df_tdms_i0_w0.calc_spectrum(),
                df_tdms_i1_w0.calc_spectrum(),
                df_tdms_i1_w0.filter(fc_Hz=fc_Hz, filter_func=apply_filter).calc_spectrum(),],
                title='Comparison between power spectra at WS=0 ',
                     xlim =[1e2,1e5], ylim= [1e-7,1e-2],
                Kolmogorov_offset=1e3, to_disk=True)



# Estimate the power spectral density of the raw signal
# Hotwire speed 5 m/s

plot_spect_comb2([
                df_tdms_i0_w5.calc_spectrum(),
                df_tdms_i1_w5.calc_spectrum(),
                df_tdms_i1_w5.filter(fc_Hz=fc_Hz, filter_func=apply_filter).calc_spectrum()],
                title='Comparison between power spectra at WS=5 m/s ',
                xlim =[1e1,1e5], ylim= [1e-7, 1e-2],
                Kolmogorov_offset=1e2, to_disk=True)

# Estimate the power spectral density of the raw signal

# Hotwire speed 10/11 m/s

plot_spect_comb2([df_tdms_i0_w10.calc_spectrum(),
                df_tdms_i1_w10.calc_spectrum(),
                df_tdms_i1_w10.filter(fc_Hz=fc_Hz, filter_func=apply_filter).calc_spectrum()],
                title='Comparison between power spectra at WS=10 m/s ',
                     xlim =[1e1,1e5],
                Kolmogorov_offset=1e2, to_disk=True)

plt.show()

#%% CONSTANTS
FIGSIZE_STD = (6,6)
#Constant directories and names for the .tdms file structure
# Dir name
TDMS_FNAME = 'Data.tdms'
GROUP_NAME = 'Wind Measurement'
CHAN_NAME = 'Wind2'

#%%
inv_meas_dir = 'inverter'
# Inverter measurements of interest
data_inv_inv_0_WS_0= 'in0_0.1'
data_inv_inv_1_WS_0 = 'in1_0.1'
data_inv_inv_1_WS_5 = 'in1_5.1'
data_inv_inv_1_WS10= 'in1_10.1'
data_inv_inv_1_WS15 = 'in1_15.1'
data_inv_inv_1_WS_20 = 'in1_20.1'


path_comp = FOLDER_FOR_DATA / inv_meas_dir

# suffixes:
# - CA : compressed air
# - Inv : Inverter
# - DEC : decimation

raw_signal_CA = [data_inv_inv_0_WS_0, data_inv_inv_1_WS_0,
                 data_inv_inv_1_WS_5,
                data_inv_inv_1_WS10, data_inv_inv_1_WS15,
                data_inv_inv_1_WS_20 ]

l_tdms_Inv = []

for item in raw_signal_CA:
    x=TdmsFile( Path( f'{path_comp}/{item}' , TDMS_FNAME))
    l_tdms_Inv.append(x)

#%%
[print(x) for x in l_tdms_Inv[0][GROUP_NAME].channels()]

dfi_i0_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[0][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter Off, WS=0, 100kHz')
dfi_i1_w0 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[1][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=0, 100kHz')
dfi_i1_w5 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[2][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=5, 100kHz')
dfi_i1_w10 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[3][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=10, 100kHz')
dfi_i1_w15 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[4][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=15, 100kHz')
dfi_i1_w20 = WT_NoiseChannelProc.from_tdms(l_tdms_Inv[5][GROUP_NAME][CHAN_NAME]
                , desc= 'Inverter On, WS=20, 100kHz')

# here the plots are comparing the raw signals.
# First plot is with the inverter state off and on and ws 0
f, yin,yout = pnf.gen_functions.fft_sig([pnf.gen_functions.fft_calc_sig(dfi_i0_w0.data,
                                            dfi_i1_w0.data, label="inv on")])

# here the inverter is on and the ws is 5, 10 (1st and 2nd graph respectively)
f1, yin1,yout1 = pnf.gen_functions.fft_sig([pnf.gen_functions.fft_calc_sig(dfi_i1_w5.data,
                                            dfi_i1_w10.data, label="inv on")])

# here the inverter is on and the ws is 15, 20 (1st and 2nd graph respectively)
f2, yin2,yout2 = pnf.gen_functions.fft_sig([pnf.gen_functions.fft_calc_sig(dfi_i1_w15.data,
                                            dfi_i1_w20.data, label="inv on")])


ws0 = [f,yin,yout]

ws5 = [f1,yin1,yout1]

ws10 = [f2,yin2,yout2]

data_list = [ws0,ws5,ws10]

# %%
ws_list = ['ws-0','ws-5/10','ws-15/20']

for item,descr_sig in zip(data_list,ws_list):
    plot_FFT([Signals_for_fft_plot(freq=item[0], sig1=item[1], sig2= item[2]),],

         [Fft_Plot_info(Title="Inverter off/on",
                       filter_type='',
                       signal_state=f'raw-{descr_sig}-on')     ],

         [Axis_titles('Frequency [Hz]', 'Amplitute [dB]')    ]
                )


plt.show()



from numpy.fft import fft, ifft
Sr = len(dfi_i1_w0.data_as_Series.index)
dt = 1 / int(Sr)
print (f"The time interval of the measurement is:\n{dt}")

time_s = np.arange(0,7,dt)
print(f"The time array is: \n {time_s}")

n= len(time_s)
fhat = fft(dfi_i1_w0.data,n)                              # compute fft
PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
freq = (1/(dt*n)) * np.arange(n)             # create x-axis (frequencies)
L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive

print(f"This is the length of the time array and should be = 2_650_000 >< no {n}")

plt.rcParams ['figure.figsize'] =[16,12]
plt.rcParams.update ({'font.size': 18})

fig, axs = plt.subplots(2,1)

plt.sca(axs[0])
#plt.plot(time_s,df_tdms_i0_w0.data)
plt.loglog(freq,np.sqrt(PSD))

plt.sca(axs[1])
plt.plot(freq[L],abs(PSD[L]))
#plt.xscale('log')
plt.yscale('log')
plt.xscale('log')
plt.show()
print (df_tdms_i1_w0.data_as_Series, df_tdms_1_0.data)



from numpy.fft import fft, ifft
#%%
# TODO Make this in a class with functions so there is no problem with migrating
# this fft algorithm to pypkg and remove duplicate code (redundancy)
#
class FFT_new:
    def __init__(self, signal):
        self.sr = signal.fs_Hz
        self.sig = signal.data
        self.ind = signal.data_as_Series.index
        self.dt = 1/ int(self.sr)
        self.time_sec = self.ind * self.dt


    def fft_calc_and_plot(self):
        n= len(self.time_sec)
        fhat = fft(self.sig,n)                 # compute fft
        PSD = fhat * np.conj(fhat) / n               # Power spectrum (power/freq)
        freq = (1/(self.dt*n)) * np.arange(n)             # create x-axis (frequencies)
        L = np.arange(1,np.floor(n/2),dtype=int)     # plot only first half (possitive)

        fig, axs = plt.subplots(2,1)

        plt.sca(axs[0])
        plt.grid('both')
        plt.title('Time domain of raw signal')
        plt.xlabel('Time [s]')
        plt.ylabel('Amplitute (Voltage)')
        plt.plot(self.time_sec ,self.sig)
        #plt.loglog(freq[L],(PSD[L]))

        plt.sca(axs[1])
        plt.loglog(freq[L],abs(PSD[L]))
        plt.title('Frequency domain')
        plt.xlabel('Frequencies [Hz]')
        plt.ylabel('Power/Freq')
        plt.grid('both')
        plt.show()

# Sample usage for plotting
FFT_new(dfi_i0_w0).fft_calc_and_plot()
