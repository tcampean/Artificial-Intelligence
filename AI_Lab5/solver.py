from table_values import *

def solver(t,w):
    """
    Parameters
    ----------
    t : TYPE: float
        DESCRIPTION: the angle theta
    w : TYPE: float
        DESCRIPTION: the angular speed omega

    Returns
    -------
    F : TYPE: float
        DESCRIPTION: the force that must be applied to the cart
    or

    None :if we have a division by zero

    """

    theta_values = get_values(t, THETA_RANGE)
    omega_values = get_values(w, OMEGA_RANGE)
    peak_value = {key: value[1] for key, value in F_RANGE.items()}
    force_values = dict()
    for theta_key in FUZZY_VALUES:
        for omega_key, f in FUZZY_VALUES[theta_key].items():
            val = min(theta_values[theta_key],omega_values[omega_key])
            if f not in force_values:
                force_values[f] = val
                
            else:
                force_values[f] = max(val,force_values[f])
    s = sum(force_values.values())
    if s == 0:
        return None
    return sum(force_values[force_set] * peak_value[force_set] for force_set in force_values.keys()) / s




def fuzzy(x, start, peak, end):
    if start is not None and start <= x < peak:
        return (x - start) / (peak - start)
    elif end is not None and peak <= x < end:
        return (end - x) / (end - peak)
    elif start is None and x <= peak:
        return 1
    elif end is None and x >= peak:
        return 1
    else:
        return 0

def get_values(val, valrange):
    values = dict()
    for key in valrange:
        values[key] = fuzzy(val, *valrange[key])
    return values
