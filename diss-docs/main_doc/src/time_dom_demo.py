import matplotlib.pyplot as plt
from scipy.signal import butter, tf2sos, sosfilt, firwin
from data import (noise_chan,
                  fs_noise, t_noise,)


# FFT
# frequencies_clean = np.fft.fftfreq(len(clean_signal), T_clean)
# frequencies_noisy = np.fft.fftfreq(len(noise_chan.data), T_noise)
# fft_clean = fft(clean_signal)
# fft_noisy = fft(noise_chan.data)

# FIR filter
fir_filt_coeff = firwin(numtaps=22,
                        fs=fs_noise,
                        cutoff=200,
                        )
sos_fir_mode = tf2sos(fir_filt_coeff, 1)
filt_on_fir_std = sosfilt(sos_fir_mode, noise_chan.data)

# Butterworth filter design
""" low pass is more suitable for us """
sos_out = butter(4,
                 200,   # This is in Hz !!!!
                 # [min(noise_frequencies[L]), max(noise_frequencies[L]-1)],
                 btype="low", fs=fs_noise, output='sos')

# Apply filter
filtered_signal = sosfilt(sos_out, noise_chan.data)

# # Validation
# fig = plt.figure(figsize=(10, 12))
fig, axs = plt.subplots(2, 2)
plot2 = plt.subplot2grid((2, 1), (1, 0), colspan=2)
# plot3 = plt.subplot2grid((3, 2), (2, 0), colspan=2)

axs[0, 1].set_xlabel("Time in seconds")
axs[0, 0].set_xlabel("Time in seconds")
axs[0, 0].set_ylabel("Recorded value (raw)")
axs[0, 0].set_title('Inverter On 0 m/s (FIR at 200 Hz)')
axs[0, 0].plot(t_noise, filt_on_fir_std)
axs[0, 1].set_title("Inverter On 0 m/s (IIR at 200 Hz)")
axs[0, 1].plot(t_noise, filtered_signal)
axs[0, 0].set_ylim([3.0, 3.75])
axs[0, 1].set_ylim([3.0, 3.75])

plot2.plot(t_noise, noise_chan.data, label="Inverter On 0 m/s")
# plot2.plot(t_clean, clean_signal, label="Inverter Off 0 m/s")
plot2.set_xlabel("Time (s)")
plot2.set_ylabel("Recorded value (raw)")
plot2.set_xlim(0, 7)
plot2.set_ylim(2.5, 4.5)
plot2.legend()

# plot3.plot(t_noise, noise_chan.data, label="Inverter On 0 m/s")
# plot3.plot(t_noise, filt_on_fir_std, label="FIR low-pass 200Hz")
# plot3.plot(t_noise, filtered_signal, label="IIR low-pass 200Hz")
# plot3.set_xlabel("Time (s)")
# plot3.set_ylabel("Recorded value (raw)")
# plot2.set_xlim(0, 7)
# plot3.set_ylim(2.5, 4.5)
# plot3.legend()

plt.show()
# plt.savefig("./demo_time_exp.png")

# # %%
