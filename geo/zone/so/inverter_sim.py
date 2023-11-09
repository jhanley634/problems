# from https://codereview.stackexchange.com/questions/287853/python-3ph-2l-inverter-simulation-with-spwm

from datetime import datetime

from scipy import signal
from scipy.integrate import solve_ivp
import numpy as np

# Parameters
# time axis
starting_time = 0  # [s]
step_time = 0.2e-6  # [s]
ending_time = 50e-3  # [s]
# PWM modulator
m = 0.85  # [-] modulation index
f_e = 1e3  # [Hz] electrical frequency
f_sw = 40e3  # [Hz] switching frequency
# DC-link
Vdc = 800  # [V] DC-link voltage
# load
R = 0.5  # [ohm]
L = 400e-6  # [H] self-inductance
K = 0  # inductances coupling coefficient, <1
M = K * L  # [H] mutual inductance


# Functions


def ref(time, amplitude, frequency, phase):
    ref = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    return ref


def triangle(time, frequency):
    triangle = signal.sawtooth(2 * np.pi * frequency * time, 0.5)
    return triangle


def spwm(mod, carrier):
    if mod >= carrier:
        d = 1
    if mod < carrier:
        d = 0
    return d


def system(t, y):
    mod1 = ref(t, m, f_e, 0)
    mod2 = ref(t, m, f_e, 2 / 3 * np.pi)
    mod3 = ref(t, m, f_e, 4 / 3 * np.pi)
    carrier = triangle(t, f_sw)
    d1 = spwm(mod1, carrier)
    d2 = spwm(mod2, carrier)
    d3 = spwm(mod3, carrier)
    v1_gnd = d1 * Vdc
    v2_gnd = d2 * Vdc
    v3_gnd = d3 * Vdc
    vgnd_n = -(v1_gnd + v2_gnd + v3_gnd) / 3
    v1 = v1_gnd + vgnd_n
    v2 = v2_gnd + vgnd_n
    v3 = v3_gnd + vgnd_n
    # v12 = v1 - v2
    # v23 = v2 - v3
    # v13 = v1 - v3
    i1 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * y[0] - M * y[1] - M * y[2])
    i2 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * y[1] - M * y[0] - M * y[2])
    i3 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * y[2] - M * y[0] - M * y[1])
    dl1dt = -R * i1 + v1
    dl2dt = -R * i2 + v2
    dl3dt = -R * i3 + v3

    return dl1dt, dl2dt, dl3dt


dt1 = datetime.now()

time = np.arange(starting_time, ending_time, step_time)
time = np.round(time, 9)

sol = solve_ivp(
    system,
    [0, ending_time],
    [0, 0, 0],
    t_eval=time,
    method="LSODA",
    max_step=1 / 50 / f_sw,
    rtol=1e-6,
    atol=1e-6,
)
t = sol.t
l1 = sol.y[0]
l2 = sol.y[1]
l3 = sol.y[2]
i1 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * l1 - M * l2 - M * l3)
i2 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * l2 - M * l1 - M * l3)
i3 = 1 / (L * L + L * M - 2 * M * M) * ((L + M) * l3 - M * l1 - M * l2)

dt2 = datetime.now()
print(dt2 - dt1)
