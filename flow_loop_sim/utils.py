"""HELPER FUNCTIONS FOR PRESSURE CHANGE CALCULATIONS"""

import numpy as np


def valve_cv(v):
    """Control Valve Flow Coefficient, Cv [m^3/s]

    Parameters
    ----------
    v : float
        Fraction of maximum valve Travel [-]


    Returns
    -------
    Cv : float
        Control Valve Flow Coefficient [m^3/s]"""
    return np.polyval(
        np.array(
            [
                12102.56410256,
                -27935.31468531,
                23596.62004662,
                -7652.18531469,
                1314.06363636,
                -77.06666667,
            ]
        ),
        v,
    )


def valve_pressure_drop(Qv, v, rho=1000, g=9.81):
    """Control Valve Pressure Drop Loss, dp [m]

    Parameters
    ----------
    Qv1 : float
        Control Valve 1 Flowrate [m^3/s]
    v1 : float
        Fraction of maximum valve Travel [-]

    Returns
    -------
    dP : float
        Control Valve Pressure Drop [Pa]"""
    Cv = valve_cv(v)  # hardcoded flow coefficient (Cv) curve from manufacturer
    if Cv <= 0:
        Cv = 1e-99
    if Qv < 0:
        Qv = 0.0
    return (Qv**2) * 1.76573853211e8 / (Cv**2) * rho * g


def pump_pressure_rise(Qt, N=1.0, rho=1000, g=9.81):
    """Pump Pressure Rise, dp [Pa]

    Parameters
    ----------
    Qt : float
        Total Flowrate [m^3/s]
    N : float
        Fraction of maximum Pump Speed [-]
    Np : int, optional
        Number of Pumps in Parallel

    Returns
    -------
    dp : float
        Pump Pressure Rise [Pa]"""
    if Qt <= 0:
        Qt = 0.0
    return (
        (81 * N**1.5 - 2200 * N * Qt**2) * rho * g
    )  # hardcoded pump flow-dp curve from manufacturer


def darcy_weisbach_pressure_drop(Qt, f, l, D, rho=1000):
    """Line Head Loss (turbulent flow), Pa [Pa]

    Parameters
    ----------
    Qt : float
        Total Flowrate [m^3/s]
    f : float
        Friction Factor [-]
    l : float
        Length of Pipe [m]
    D : float
        Diameter of Pipe [m]

    Returns
    -------
    dp : float
        Pressure Drop [Pa]"""
    return (
        4.0 * f * l * Qt**2 / (np.pi**2 * D**5) * rho
    )  # pressure drop along a pipe for fully turbulent flow
