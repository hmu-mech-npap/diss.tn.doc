"""Attempt to pyqtgraph package."""
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
from pathlib import Path
from nptdms import TdmsFile
from pros_noisefiltering.WT_NoiProc import (WT_NoiseChannelProc,
                                            Graph_data_container
                                            )

# a clone to use the time array for plotting with pyqtgraph
# TODO consider adding this to qt app cause its much faster and prettier
# than matplotlib.
# also more stylish and new looking


class FFT_new:
    """This class is used to calculate the fourier transform for raw signal."""

    def __init__(self, signal, title):
        """Construct the appropriate object to manipulate the signal.

        We should be able to integrate this in WT_Noi_proc.
        """
        self.Title = title
        self.sr = signal.fs_Hz
        self.sig = signal.data
        self.ind = signal.data_as_Series.index
        self.dt = 1 / int(self.sr)
        self.time_sec = self.ind * self.dt

        self._channel_data = signal._channel_data

    def fft_calc(self):
        """Func body for calculation of the frequency domain of raw data."""
        n = len(self.time_sec)
        fhat = np.fft.fft(self.sig, n)                  # compute fft
        PSD = fhat * np.conj(fhat) / n                  # Power spectrum (pr/f)
        freq = (1/(self.dt*n)) * np.arange(n)           # create x-axis (freqs)
        L = np.arange(1, np.floor(n/2), dtype=int)      # plot only first half
        return Graph_data_container(freq[L], abs(PSD[L]),
                                    label="fft transform")


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
    desc='Inverter off, WS=0')
df_tdms_1_0 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[3][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=0')
df_tdms_1_10 = WT_NoiseChannelProc.from_tdms(
    l_tdms_CA[5][GROUP_NAME][CHAN_NAME],
    desc='Inverter on, WS=10')

def plot_signal_all_doms(signal):

    filtrd = signal.filter(fc_Hz=2000, desc="butterworth low")
    freq_dom_filtrd = FFT_new(filtrd,
                              title=
                              f"Time domain filtered with {filtrd.description}")

    # freq_dom_filtrd.fft_calc_and_plot()

    win = pg.GraphicsLayoutWidget(show=True, title="Basic plotting examples")
    win.resize(1920, 1080)
    win.setWindowTitle('pyqtgraph example: Plotting')
    # Enable antialiasing for prettier plots
    pg.setConfigOptions(antialias=True)

    p1 = win.addPlot(row=0,
                     col=0,
                     colspan=1,
                     title=f"{signal.description}(m/s)")
    p1.setLabels(bottom='time duration (s)', left='Raw sensor Voltage',
                 )
    p1.showGrid(y=True)
    p1.plot(freq_dom_filtrd.time_sec,
            signal.data,
            pen=(0, 255, 0, 35),
            name="Raw signal")

    p1_filt = win.addPlot(row=0,
                          col=1,
                          title='Filtered signal')
    p1_filt.setLabels(bottom='time duration (s)', left='')
    p1_filt.showGrid(y=True)
    p1_filt.addLegend()
    p1_filt.setYRange(filtrd.data.min() - 0.1,
                      filtrd.data.max() + 0.1)
    p1_filt.plot(freq_dom_filtrd.time_sec,
                 filtrd.data,
                 pen=(0, 0, 255),
                 name=f"{filtrd.description}-{filtrd.operations.__getitem__(1)} Hz")

    p2 = win.addPlot(row=1,
                     col=0,
                     rowspan=1,
                     colspan=2,
                     padding=10,
                     title="Filtered signal Frequency domain representation")
    data = freq_dom_filtrd.fft_calc()
    p2.setLogMode(x=True, y=True)
    p2.showGrid(x=True, y=True)
    p2.setLabels(bottom='Frequencies in Hz', left='Power/Freq',
                 top='')
    # p2.setLabel(axis='bottom', text='Frequencies in Hz')
    # p2.setLabel(axis='left', text='Power/Freq')
    p2.plot(data.x, data.y,
            pen=(50, 50, 250), fillLevel=-18, brush=(250, 50, 50, 100))

    p3 = win.addPlot(row=2,
                     col=0,
                     rowspan=1,
                     colspan=2,
                     padding=10,
                     title="Filtered signal Spectral density (welch)")
    welch = filtrd.calc_spectrum_gen(nperseg=1024 << 6)
    p3.setLogMode(x=True, y=True)
    p3.showGrid(x=True, y=True)
    p3.setLabels(bottom='Frequencies in Hz', left='dB',
                 top='')
    # p3.setYRange(-5, -18)
    # p2.setLabel(axis='bottom', text='Frequencies in Hz')
    # p2.setLabel(axis='left', text='Power/Freq')
    p3.plot(welch.x, welch.y,
            pen=(50, 50, 250), fillLevel=-18, brush=(250, 50, 50, 100))

    # save to a file somewhere
    exporter = pg.exporters.ImageExporter(win.scene())
    exporter.parameters()['width'] = 1920   # also effects the height param
    exporter.parameters()['antialias'] = True
    exporter.export('./sig_proc_plots/test.jpg')
    return win


plot_signal_all_doms(df_tdms_1_10)
