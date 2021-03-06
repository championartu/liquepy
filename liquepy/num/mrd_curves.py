import numpy as np


def calc_mr_elastic(gamma):
    return np.ones(len(gamma))


def calc_mr_mohr_coloumb(gamma, elastic_mod, cu):
    tau = np.clip(elastic_mod * gamma, None, cu)
    secant_mod_reduction = (tau / gamma) / elastic_mod
    return secant_mod_reduction


def calc_mr_flac_default_curve(gamma, l_1, l_2):
    gamma_percent = gamma * 100
    lg = np.log10(gamma_percent)
    s = np.clip((l_2 - lg) / (l_2 - l_1), None, 1)
    return s ** 2 * (3. - 2. * s)


def calc_mr_seed_and_sun_mod(gamma):
    l_1 = -3.156
    l_2 = 1.904
    return calc_mr_flac_default_curve(gamma, l_1, l_2)


def calc_mr_daren_mod(gamma, a=0.92, gamma_ref=0.001):
    return 1.0 / (1.0 + (gamma / gamma_ref) ** a)


def calc_mr_vardanega_2013_mod(gamma, i_p):
    a = 0.943  # Eq 22b
    j = 3.7  # Eq 23
    gamma_ref = j * (i_p / 1000)
    return 1.0 / (1.0 + (gamma / gamma_ref) ** a)  # Eq. 22b


def calc_ss_ratio_from_ip_vardanega_2013(i_p, gamma_target=0.005):
    """
    Calculates an appropriate strength-stiffness ratio for a soil based on the plasticity index.
    Parameters
    ----------
    i_p
    gamma_target

    Returns
    -------

    """
    vardanega_mr = calc_mr_vardanega_2013_mod(gamma_target, i_p=i_p)
    return vardanega_mr * gamma_target


def calc_ip_from_ss_ratio_vardanega_2013(ss_ratio, gamma_target=0.005):
    """
    Calculates the appropriate plasticity index for a soil based on the strength-stiffness ratio (ss_ratio).

    The strength stiffness ratio uses the undrained strength and the initial stiffness.

    Parameters
    ----------
    ss_ratio: float
        Strength-stiffness ratio
    gamma_target: float
        Strain where backbone response should reach undrained strength
    Returns
    -------

    """
    ips = np.arange(0.05, 1.05, 0.05)
    vardanega_mr = calc_mr_vardanega_2013_mod(gamma_target, i_p=ips)
    ss_ratios = vardanega_mr * gamma_target
    return np.interp(ss_ratio, ss_ratios, ips)

