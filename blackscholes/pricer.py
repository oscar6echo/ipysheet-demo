
from math import erf, exp, log, pi, sqrt


def N(x):
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def Nprime(x):
    return exp(-x*x / 2.0) / sqrt(2.0 * pi)

def Price_Call(S, K, T, v, r, q):
    """
    BlackScholes formula and Greeks - Call option
    """
    sqrt_T = sqrt(T)
    d1 = (log(S/K) + (r - q + v**2/2) * T) / (v *sqrt_T)
    d2 = d1 - v * sqrt_T
    N_d1 = N(d1)
    N_prime_d1 = Nprime(d1)
    N_d2 = N(d2)
    N_prime_d2 = Nprime(d2)
    PV = exp(-r * T)
    PV_K = K * PV
    D = exp(-q * T)
    price = N_d1 * S * D - N_d2 * PV_K
    
    delta = D * N_d1
    gamma = D * N_prime_d1 / (S * v * sqrt_T)
    vega = S *D * N_prime_d1 * sqrt_T
    theta = -D * S * N_prime_d1 * v / (2 * sqrt_T) - r * PV_K * N_d2 + q * S * D * N_d1
    rho = PV_K * T * N_d2
    voma = S * D * N_prime_d1 * sqrt_T * d1 * d2 / v

    payoff = max(0, S - K)
    PV_payoff = PV * payoff
 
    return {'d1': d1,
            'd2': d2,
            'N_d1': N_d1,
            'N_d2': N_d2,
            'N_prime_d1': N_prime_d1,
            'N_prime_d2': N_prime_d2,
            'PV': PV,
            'PV_K': PV_K,
            'D': D,
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho,
            'voma': voma,
            'payoff': payoff,
            'PV_payoff': PV_payoff}

# S = 100.0
# K = 100.0
# T = 5.0
# vol = 0.25
# r = 0.02
# q = 0.03
# typ = +1
# Price_Call(S, K, T, vol, r, q)




def Price_Put(S, K, T, v, r, q):
    """
    BlackScholes formula and Greeks - Put option
    """
    sqrt_T = sqrt(T)
    d1 = (log(S/K) + (r - q + v**2/2) * T) / (v *sqrt_T)
    d2 = d1 - v * sqrt_T
    N_minus_d1 = N(-d1)
    N_prime_d1 = Nprime(d1)
    N_minus_d2 = N(-d2)
    N_prime_d2 = Nprime(d2)
    PV = exp(-r * T)
    PV_K = K * PV
    D = exp(-q * T)
    price = N_minus_d2 * PV_K - N_minus_d1 * S * D

    delta = - D * N_minus_d1
    gamma = D * N_prime_d1 / (S * v * sqrt_T)
    vega = S *D * N_prime_d1 * sqrt_T
    theta = -D * S * N_prime_d1 * v / (2 * sqrt_T) + r * PV_K * N_minus_d2 - q * S * D * N_minus_d1
    rho = - PV_K * T * N_minus_d2
    voma = S * D * N_prime_d1 * sqrt_T * d1 *d2 / v

    payoff = max(0, K - S)
    PV_payoff = PV * payoff
 
    return {'d1': d1,
            'd2': d2,
            'N_minus_d1': N_minus_d1,
            'N_minus_d2': N_minus_d2,
            'N_prime_d1': N_prime_d1,
            'N_prime_d2': N_prime_d2,
            'PV': PV,
            'PV_K': PV_K,
            'D': D,
            'price': price,
            'delta': delta,
            'gamma': gamma,
            'vega': vega,
            'theta': theta,
            'rho': rho,
            'voma': voma,
            'payoff': payoff,
            'PV_payoff': PV_payoff}

# S = 100.0
# K = 100.0
# T = 5.0
# vol = 0.25
# r = 0.02
# q = 0.03
# typ = +1
# Price_Put(S, K, T, vol, r, q)
