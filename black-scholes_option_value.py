import math
from scipy.stats import norm

# Black-Scholes Model (European calls/puts)
def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return option_price

# Intrinsic Value function
def intrinsic_value(S, K, option_type='call'):
    if option_type == 'call':
        return max(S - K, 0)
    elif option_type == 'put':
        return max(K - S, 0)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

# Extrinsic Value Function
def extrinsic_value(market_price, intrinsic_value):
    return market_price - intrinsic_value

# Valuation
def evaluate_option(S, K, T, r, sigma, market_price, option_type='call'):
    iv = intrinsic_value(S, K, option_type)
    
    ev = extrinsic_value(market_price, iv)
    
    theoretical_price = black_scholes(S, K, T, r, sigma, option_type)
    
    value_ratio = theoretical_price / market_price
    
    result = {
        'Intrinsic Value': iv,
        'Extrinsic Value': ev,
        'Theoretical Price': theoretical_price,
        'Market Price': market_price,
        'Value Ratio': value_ratio,
        'Evaluation': 'Undervalued' if value_ratio > 1 else 'Overvalued' if value_ratio < 1 else 'Fairly Valued'
    }
    
    return result

# Parameters
S = 41.45  # Current price of underlying asset
K = 30   # Strike price
T = 1.4  # Time to expiration (years)
r = 0.04866 # Risk-free interest rate (annual)
sigma = 0.1591 # Implied Volatility (IV) of underlying asset
market_price = 12 # Option market price
option_type = 'call' # 'call' or 'put'

# Evaluation
evaluation = evaluate_option(S, K, T, r, sigma, market_price, option_type)

for key, value in evaluation.items():
    print(f"{key}: {value}")
