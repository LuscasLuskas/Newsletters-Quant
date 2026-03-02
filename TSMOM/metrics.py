import numpy as np

def calculate_metrics(returns, risk_free_rate=0.02):

    returns = returns.dropna()
    
    # Basic stats
    total_return = (1 + returns).prod() - 1
    n_years = len(returns) / 252
    annual_return = (1 + total_return) ** (1/n_years) - 1
    annual_vol = returns.std() * np.sqrt(252)
    
    # Sharpe Ratio
    sharpe = (annual_return - risk_free_rate) / annual_vol if annual_vol > 0 else 0
    
    # Win Rate
    win_rate = (returns > 0).sum() / len(returns)
    
    # Maximum Drawdown
    cumulative = (1 + returns).cumprod()
    peak = cumulative.expanding().max()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()
    
    # Calmar Ratio (return / max drawdown)
    calmar = annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    return {
        'Total Return': f"{total_return*100:.2f}%",
        'Annual Return': f"{annual_return*100:.2f}%",
        'Annual Volatility': f"{annual_vol*100:.2f}%",
        'Sharpe Ratio': f"{sharpe:.2f}",
        'Win Rate': f"{win_rate*100:.2f}%",
        'Max Drawdown': f"{max_drawdown*100:.2f}%",
        'Calmar Ratio': f"{calmar:.2f}"
    }