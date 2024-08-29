from scipy.stats import norm
from scipy.optimize import brentq
import math

# Black-Scholes formula for a call option
def black_scholes_call_price(S, K, T, r, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)

# Function to calculate the implied volatility
def implied_volatility(S, K, T, r, market_price, option_type='call'):
    if option_type == 'call':
        objective_function = lambda sigma: black_scholes_call_price(S, K, T, r, sigma) - market_price
    else:
        raise ValueError("Only call option implied volatility is implemented in this example.")
    
    # Use a root-finding method (e.g., Brent's method) to solve for sigma
    implied_vol = brentq(objective_function, 0.0001, 10.0)  # sigma should be between 1% and 300%
    
    return implied_vol

# Example parameters
S = 41.45  # Current price of the underlying asset
K = 32  # Strike price of the option
T = 1.4  # Time to expiration in years
r = 0.04866 # Risk-free interest rate (annual)
market_price = 10 # Current market price of the option

# Calculate implied volatility
sigma = implied_volatility(S, K, T, r, market_price)
print(f"Implied Volatility: {sigma:.2%}")