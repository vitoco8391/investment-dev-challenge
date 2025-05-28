import numpy as np
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import squareform

def markowitz_optimizer(df, risk_level, max_weight):
    cov_matrix = np.cov(df.T)
    num_assets = df.shape[1]

    def portfolio_volatility(w):
        return np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))

    constraints = (
        {"type": "eq", "fun": lambda w: np.sum(w) - 1},
        {"type": "ineq", "fun": lambda w: risk_level - portfolio_volatility(w)}
    )
    bounds = tuple((0, max_weight) for _ in range(num_assets))
    init_guess = np.ones(num_assets) / num_assets

    result = minimize(portfolio_volatility, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError("Optimization failed.")

    return {ticker: round(weight, 6) for ticker, weight in zip(df.columns, result.x)}

def risk_parity_optimizer(df, max_weight):
    cov_matrix = np.cov(df.T)
    num_assets = len(df.columns)

    def risk_contribution(weights):
        port_var = np.dot(weights.T, np.dot(cov_matrix, weights))
        marginal_contrib = np.dot(cov_matrix, weights)
        risk_contrib = weights * marginal_contrib / port_var
        return np.sum((risk_contrib - 1/num_assets)**2)

    init_guess = np.ones(num_assets) / num_assets
    bounds = tuple((0, max_weight) for _ in range(num_assets))
    constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)

    result = minimize(risk_contribution, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError("Risk parity optimization failed.")

    return {ticker: round(weight, 6) for ticker, weight in zip(df.columns, result.x)}

def hrp_optimizer(df, max_weight):
    cov = np.cov(df.T)
    corr = np.corrcoef(df.T)
    dist = np.sqrt(0.5 * (1 - corr))
    np.fill_diagonal(dist, 0.0)
    linkage_matrix = linkage(squareform(dist), method='single')
    sort_ix = leaves_list(linkage_matrix)
    tickers = df.columns[sort_ix]

    def get_cluster_var(cov, cluster_items):
        sub_cov = cov[np.ix_(cluster_items, cluster_items)]
        inv_diag = 1. / np.diag(sub_cov)
        weights = inv_diag / np.sum(inv_diag)
        return np.dot(weights.T, np.dot(sub_cov, weights))

    def recursive_bisection(items):
        if len(items) == 1:
            return {items[0]: 1.0}
        split = len(items) // 2
        left = items[:split]
        right = items[split:]
        left_var = get_cluster_var(cov, left)
        right_var = get_cluster_var(cov, right)
        alpha = 1.0 - left_var / (left_var + right_var)
        left_weights = recursive_bisection(left)
        right_weights = recursive_bisection(right)
        weights = {}
        for i in left_weights:
            weights[i] = alpha * left_weights[i]
        for i in right_weights:
            weights[i] = (1 - alpha) * right_weights[i]
        return weights

    indices = [df.columns.get_loc(t) for t in tickers]
    raw_weights = recursive_bisection(indices)
    return {df.columns[k]: round(v, 6) for k, v in raw_weights.items()}

def uryasev_cvar_optimizer(df, risk_level, max_weight):
    returns = df.to_numpy()
    alpha = 0.95
    num_assets = df.shape[1]

    def portfolio_loss(weights):
        port_returns = returns @ weights
        threshold = np.percentile(port_returns, 100 * (1 - alpha))
        losses = port_returns[port_returns <= threshold]
        if len(losses) == 0:
            return 1e6
        cvar = np.mean(losses)
        return -cvar

    constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)
    bounds = tuple((0, max_weight) for _ in range(num_assets))
    init_guess = np.ones(num_assets) / num_assets

    result = minimize(portfolio_loss, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError("CVaR optimization failed.")

    return {ticker: round(weight, 6) for ticker, weight in zip(df.columns, result.x)}
