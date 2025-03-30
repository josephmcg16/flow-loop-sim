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
    coeffs = np.array([-0.26478213, 3.90862164, -6.44491341, 7.45752813, -5.00264694, 1.34623555])
    return (
        np.column_stack([v ** (i + 1) for i in range(len(coeffs))]) @ coeffs * 2518.2
    )[0]


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
    Cv = np.maximum(Cv, 1e-6)
    Qv = np.maximum(Qv, 0.0)
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
    Qt = np.maximum(Qt, 0.0)
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
