import numpy as np
from wave_file import wave_write_16bit_mono
from oscillator import sine_wave
from envelope import ADSR

fs = 44100
f0 = 440

gate = 3
duration = 4

number_of_partial = 2

VCO_A = np.array([0, 0])
VCO_D = np.array([0, 0])
VCO_S = np.array([1, 1])
VCO_R = np.array([0, 0])
VCO_gate = np.array([duration, duration])
VCO_duration = np.array([duration, duration])
VCO_offset = np.array([f0, f0 * 2])
VCO_depth = np.array([0, 0])

VCA_A = np.array([0.01, 0.01])
VCA_D = np.array([0, 0])
VCA_S = np.array([1, 1])
VCA_R = np.array([0.01, 0.01])
VCA_gate = np.array([gate, gate])
VCA_duration = np.array([duration, duration])
VCA_offset = np.array([0, 0])
VCA_depth = np.array([1, 1])

length_of_s = int(fs * duration)
s1 = np.zeros(length_of_s)

for i in range(number_of_partial):
    vco = ADSR(fs, VCO_A[i], VCO_D[i], VCO_S[i], VCO_R[i], VCO_gate[i], VCO_duration[i])
    for n in range(length_of_s):
        vco[n] = VCO_offset[i] + vco[n] * VCO_depth[i]

    if np.max(vco) < fs / 2:
        s0 = sine_wave(fs, vco, duration)

        vca = ADSR(fs, VCA_A[i], VCA_D[i], VCA_S[i], VCA_R[i], VCA_gate[i], VCA_duration[i])
        for n in range(length_of_s):
            vca[n] = VCA_offset[i] + vca[n] * VCA_depth[i]

        for n in range(length_of_s):
            s0[n] *= vca[n]

        for n in range(length_of_s):
            s1[n] += s0[n]

length_of_s_master = int(fs * (duration + 2))
s_master = np.zeros(length_of_s_master)

offset = int(fs * 1)
for n in range(length_of_s):
    s_master[offset + n] += s1[n]

master_volume = 0.5
s_master /= np.max(np.abs(s_master))
s_master *= master_volume

wave_write_16bit_mono(fs, s_master.copy(), 'p6_6(output).wav')
