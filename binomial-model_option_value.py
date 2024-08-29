import numpy as np

def binomial_option_model(S, K, T, r, sigma, N, type):

    dt = T / N  # Time step
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Probability of up move
    discount_factor = np.exp(-r * dt)  # Discount factor per time step

    # Initialize asset prices at maturity
    asset_prices = np.zeros(N + 1)
    for i in range(N + 1):
        asset_prices[i] = S * (u ** (N - i)) * (d ** i)

    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    if type == 'call':
        option_values = np.maximum(asset_prices - K, 0)
    elif type == 'put':
        option_values = np.maximum(K - asset_prices, 0)

    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            # Values at each node
            hold_value = discount_factor * (p * option_values[i] + (1 - p) * option_values[i + 1])
            exercise_value = 0
            if type == 'call':
                exercise_value = np.maximum(S * (u ** (j - i)) * (d ** i) - K, 0)
            elif type == 'put':
                exercise_value = np.maximum(K - S * (u ** (j - i)) * (d ** i), 0)
            option_values[i] = np.maximum(hold_value, exercise_value)

    return option_values[0]

# Parameters
S = 41.45  # Current price (underlying)
K = 30  # Strike price
T = 1.4  # Time until expiration (years)
r = 0.0486  # Risk-free interest rate (annual) {use current bond rate}
sigma = 0.1571  # Implied Volatility (underlying)
N = 200  # Number of time steps {use higher numbers for more accurate price predictions}
type = 'call'


if type == 'call':
    # Calculate Call Valuation
    call_val = binomial_option_model(S, K, T, r, sigma, N, type='call')
    print(f"Call Option Valuation: {call_val:.2f}")

else:
   # Calculate Put Valuation
    put_val = binomial_option_model(S, K, T, r, sigma, N, type='put')
    print(f"American Put Option Valuation: {put_val:.2f}") 
