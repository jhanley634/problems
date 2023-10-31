#!/usr/bin/env python

# from https://codereview.stackexchange.com/questions/287718/value-at-risk-forecast-generator

# Standard library imports
from functools import wraps
import math
import time
import warnings

# Related third-party imports
from arch import arch_model
from IPython.display import display
from scipy.stats import gumbel_r, norm
import numpy as np
import pandas as pd

# Suppress warnings
warnings.filterwarnings("ignore")

ticker_list = ["AAPL", "MSFT"]
NUM_PERIODS = 11
daily_return = pd.DataFrame(
    np.zeros((NUM_PERIODS, len(ticker_list))),
    columns=ticker_list,
    index=pd.date_range(start="2019-10-01", periods=NUM_PERIODS, freq="Q"),
)
print(daily_return)

weights = np.full(shape=len(ticker_list), fill_value=1 / len(ticker_list))
cov_matrix = daily_return.cov()


def timing_decorator(fn):
    @wraps(fn)
    def wrap(*args, **kw):
        t0 = time.time()
        result = fn(*args, **kw)
        elapsed = time.time() - t0
        print(
            "func:%r args:[%r, %r] took: %2.3f sec" % (fn.__name__, args, kw, elapsed)
        )
        return result

    return wrap


class ValueAtRisk:
    """
    A class to calculate various Value at Risk (VaR) methods.
    """

    # ------------------- Constants -------------------
    # Investment amount
    AMOUNT = 100
    # Confidence levels
    CONFIDENCE_LEVEL_95 = 0.05
    CONFIDENCE_LEVEL_975 = 0.025
    CONFIDENCE_LEVEL_99 = 0.01
    # Number of simulations for Monte Carlo methods
    SIMULATIONS = 100000

    def __init__(self, daily_return, weights):
        """
        Initialize the class with daily returns and portfolio weights.
        """
        self.daily_return = daily_return  # DataFrame of daily returns
        self.weights = weights  # List of portfolio weights
        self.cov_matrix = daily_return.cov()  # Covariance matrix of the returns

    def __repr__(self):
        return f"ValueAtRisk(size={len(self.daily_return)})"

    # ------------------- Variance-Covariance VaR -------------------
    @timing_decorator
    def variance_covariance(self):
        """
        Compute Parametric VaR using the variance-covariance method.
        """
        # Calculate the date for the next day's VaR value
        date = self.daily_return.index.max() + pd.Timedelta(days=1)
        # Z-scores for specified confidence intervals
        z_scores = norm.ppf(
            [
                self.CONFIDENCE_LEVEL_95,
                self.CONFIDENCE_LEVEL_975,
                self.CONFIDENCE_LEVEL_99,
            ]
        )
        # Calculate portfolio mean using weighted average of daily returns
        daily_mean = np.average(self.daily_return, axis=1, weights=self.weights)
        # Overall mean of daily portfolio returns
        port_mean = daily_mean.mean()
        # Portfolio standard deviation based on covariance matrix and weights
        port_stdev = np.sqrt(
            np.dot(self.weights.T, np.dot(self.cov_matrix, self.weights))
        )
        # VaR values calculated using the z-score formula
        var_values = port_mean + z_scores * port_stdev
        # Expected Shortfall (ES) for 97.5% confidence level
        es_975 = np.mean(daily_mean[daily_mean <= var_values[1]])
        # Dictionary of VaR and ES values
        var_dict = {
            "VaR(95%)": var_values[0],
            "VaR(97.5%)": var_values[1],
            "VaR(99%)": var_values[2],
            "ES(97.5%)": es_975,
        }
        # Return a DataFrame with the calculated VaR and ES values
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Historical Simulation VaR -------------------
    @timing_decorator
    def historic(self):
        """
        Compute Historical VaR.
        """
        # Calculate the date for the next day's VaR value
        date = self.daily_return.index.max() + pd.Timedelta(days=1)
        # Calculate portfolio returns by applying weights to the daily returns
        portfolio_returns = np.average(self.daily_return, axis=1, weights=self.weights)
        # Determine VaR values at different percentiles
        var_percentiles = np.percentile(
            portfolio_returns,
            [
                self.CONFIDENCE_LEVEL_95 * 100,
                self.CONFIDENCE_LEVEL_975 * 100,
                self.CONFIDENCE_LEVEL_99 * 100,
            ],
        )
        # Calculate Expected Shortfall (ES) for the 97.5% percentile
        es_975 = np.mean(portfolio_returns[portfolio_returns <= var_percentiles[1]])
        # Map calculated VaR and ES values into a dictionary
        var_dict = {
            "VaR(95%)": var_percentiles[0],
            "VaR(97.5%)": var_percentiles[1],
            "VaR(99%)": var_percentiles[2],
            "ES(97.5%)": es_975,
        }
        # Return a DataFrame with the calculated VaR and ES values
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- EMWA VaR -------------------
    @timing_decorator
    def ewma(self, lambda_factor=0.94):
        """
        Compute VaR using the Exponentially Weighted Moving Average (EWMA) method.
        """
        date = self.daily_return.index.max() + pd.Timedelta(
            days=1
        )  # Next day's date for VaR calculation
        # Initialize the EWMA covariance matrix with the simple covariance matrix
        ewma_cov_matrix = self.daily_return.cov()

        # Update the EWMA covariance matrix for each day's returns
        for ti in range(1, len(self.daily_return)):
            returns_vector = self.daily_return.iloc[ti].values
            # Outer product of returns vector for the current day
            current_return_matrix = np.outer(returns_vector, returns_vector)
            # EWMA formula to update the covariance matrix
            ewma_cov_matrix = (
                lambda_factor * ewma_cov_matrix
                + (1 - lambda_factor) * current_return_matrix
            )

        # Calculate portfolio variance and volatility using the EWMA covariance matrix
        port_variance = np.dot(self.weights.T, np.dot(ewma_cov_matrix, self.weights))
        port_volatility = np.sqrt(port_variance)
        # Mean portfolio return for VaR calculation
        port_mean_return = np.dot(self.weights, self.daily_return.mean())
        # Z-scores for VaR confidence intervals
        z_scores = norm.ppf(
            [
                self.CONFIDENCE_LEVEL_95,
                self.CONFIDENCE_LEVEL_975,
                self.CONFIDENCE_LEVEL_99,
            ]
        )

        # Calculate VaR values
        var_values = port_mean_return + z_scores * port_volatility
        # Calculate portfolio returns for Expected Shortfall calculation
        daily_return_port = np.dot(self.daily_return.values, self.weights)
        # Expected Shortfall (ES) for 97.5% confidence level
        es_975 = np.mean(daily_return_port[daily_return_port <= var_values[1]])
        # Map of VaR and ES calculations
        var_dict = {
            "VaR(95%)": var_values[0],
            "VaR(97.5%)": var_values[1],
            "VaR(99%)": var_values[2],
            "ES(97.5%)": es_975,
        }
        # Return a DataFrame with the calculated VaR and ES values
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Monte Carlo VaR Normal -------------------
    @timing_decorator
    def monte_carlo(self):
        """
        Compute Monte Carlo VaR considering the correlation between assets.

        Returns:
            DataFrame: DataFrame with VaR values.
        """
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Calculate portfolio mean and covariance based on historical returns
        asset_mean_returns = self.daily_return.mean()
        cov_matrix = self.daily_return.cov()

        # Generate multivariate normal returns that account for correlations
        multivariate_normal_samples = np.random.multivariate_normal(
            asset_mean_returns, cov_matrix, self.SIMULATIONS
        )

        # Calculate the portfolio PnL by applying the weights to the simulated multivariate returns
        PnL_list = np.dot(multivariate_normal_samples, self.weights)

        # Calculate VaR at different confidence levels
        var_percentiles = np.percentile(
            PnL_list,
            [
                self.CONFIDENCE_LEVEL_95 * 100,
                self.CONFIDENCE_LEVEL_975 * 100,
                self.CONFIDENCE_LEVEL_99 * 100,
            ],
        )
        es_975 = PnL_list[PnL_list <= var_percentiles[1]].mean()

        var_dict = {
            "VaR(95%)": var_percentiles[0],
            "VaR(97.5%)": var_percentiles[1],
            "VaR(99%)": var_percentiles[2],
            "ES(97.5%)": es_975,
        }
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Monte Carlo Extreme Value Gumbel -------------------
    @timing_decorator
    def evt_monte_carlo(self):
        """
        Compute Extreme Value Theory Monte Carlo VaR using the Gumbel distribution.

        Returns:
            DataFrame: DataFrame with VaR values.
        """
        date = self.daily_return.index.max() + pd.Timedelta(days=1)
        simulated_returns = np.random.multivariate_normal(
            self.daily_return.mean(), self.cov_matrix, self.SIMULATIONS
        )
        portfolio_pnls = np.dot(simulated_returns, self.weights)
        block_maxima = -np.sort(-portfolio_pnls)[
            : int(0.1 * len(portfolio_pnls))
        ]  # top 10% as block maxima
        loc, scale = gumbel_r.fit(block_maxima)
        gumbel_pnls = -np.random.gumbel(loc, scale, self.SIMULATIONS)  # simulate losses
        var_values = np.percentile(
            gumbel_pnls,
            [
                self.CONFIDENCE_LEVEL_95 * 100,
                self.CONFIDENCE_LEVEL_975 * 100,
                self.CONFIDENCE_LEVEL_99 * 100,
            ],
        )
        es_975 = gumbel_pnls[gumbel_pnls <= var_values[1]].mean()
        var_dict = {
            "VaR(95%)": var_values[0],
            "VaR(97.5%)": var_values[1],
            "VaR(99%)": var_values[2],
            "ES(97.5%)": es_975,
        }
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- GARCH VaR Normal -------------------
    @timing_decorator
    def para_garch_normal(self):
        """
        Compute GARCH VaR using a normal distribution.

        Returns:
            DataFrame: DataFrame with VaR values.
        """
        date = self.daily_return.index.max() + pd.Timedelta(days=1)
        weighted_avg = pd.DataFrame()
        weighted_avg["weighted_avg"] = (
            np.average(self.daily_return, axis=1, weights=self.weights) * 100
        )
        am = arch_model(
            weighted_avg["weighted_avg"], vol="Garch", p=1, o=0, q=1, dist="normal"
        )
        res = am.fit(disp="off")
        forecasts = res.forecast()
        cond_mean = forecasts.mean.iloc[-1].values
        cond_var = forecasts.variance.iloc[-1].values

        # Calculate z-scores for the normal distribution
        z_scores = norm.ppf(
            [
                self.CONFIDENCE_LEVEL_95,
                self.CONFIDENCE_LEVEL_975,
                self.CONFIDENCE_LEVEL_99,
            ]
        )
        value_at_risk = cond_mean + np.sqrt(cond_var) * z_scores
        var_95, var_975, var_99 = value_at_risk

        # Expected Shortfall calculation is not directly applicable with the normal distribution
        # ES for a normal distribution is a function of both the mean and the standard deviation
        es_975 = cond_mean + (norm.pdf(norm.ppf(0.025)) / 0.025) * np.sqrt(cond_var)

        var_dict = {
            "VaR(95%)": var_95 / 100,
            "VaR(97.5%)": var_975 / 100,
            "VaR(99%)": var_99 / 100,
            "ES(97.5%)": es_975 / 100,
        }
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- GARCH VaR Skewed-t -------------------
    @timing_decorator
    def para_garch_t(self):
        """
        Compute GARCH VaR using a skewed-t distribution.

        Returns:
            DataFrame: DataFrame with VaR values.
        """
        date = self.daily_return.index.max() + pd.Timedelta(days=1)
        weighted_avg = pd.DataFrame()
        weighted_avg["weighted_avg"] = (
            np.average(self.daily_return, axis=1, weights=self.weights) * 100
        )
        am = arch_model(
            weighted_avg["weighted_avg"], vol="Garch", p=1, o=0, q=1, dist="skewt"
        )
        res = am.fit(disp="off")
        forecasts = res.forecast()
        cond_mean = forecasts.mean.iloc[-1].values
        cond_var = forecasts.variance.iloc[-1].values
        q = am.distribution.ppf(
            [
                self.CONFIDENCE_LEVEL_95,
                self.CONFIDENCE_LEVEL_975,
                self.CONFIDENCE_LEVEL_99,
            ],
            res.params[-2:],
        )
        value_at_risk = cond_mean + np.sqrt(cond_var) * q
        var_95, var_975, var_99 = value_at_risk
        es_975 = np.mean(
            weighted_avg[weighted_avg["weighted_avg"] <= var_975]["weighted_avg"]
        )
        if math.isnan(es_975):
            es_975 = var_99

        var_dict = {
            "VaR(95%)": var_95 / 100,
            "VaR(97.5%)": var_975 / 100,
            "VaR(99%)": var_99 / 100,
            "ES(97.5%)": es_975 / 100,
        }
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Summary -------------------
    def VaR_summary(self):
        """
        Generate a summary of all VaR calculations.

        Returns:
            DataFrame: DataFrame with VaR summary scaled by the specified amount.
        """
        methods = [
            "Parametric",
            "Historical Simulation",
            "EWMA",
            "Monte Carlo (Normal)",
            "EVT Monte Carlo (Gumbel)",
            "GARCH (Normal)",
            "GARCH (Skewed-t)",
        ]
        calculations = [
            self.variance_covariance(),
            self.historic(),
            self.ewma(),
            self.monte_carlo(),
            self.evt_monte_carlo(),
            self.para_garch_normal(),
            self.para_garch_t(),
        ]

        results = dict(zip(methods, calculations))
        summary = pd.concat(results, axis=0)

        # Scale the VaR values by the constant "AMOUNT"
        summary *= self.AMOUNT

        return summary


# Record the start time
start_time = time.time()

# Execution
if __name__ == "__main__":
    VaR = ValueAtRisk(daily_return, weights)
    summary_df = VaR.VaR_summary()

# Calculate total execution time
end_time = time.time()
total_time = end_time - start_time
minutes, seconds = divmod(total_time, 60)

# Print out the total execution time
print(
    f"All functions took {int(minutes)} minutes and {seconds:.4f} seconds to complete."
)

# Print the results
print("\nValue at Risk and Expected Shortfall one-day ahead Forecast (in %)")
display(summary_df)


# Define the rolling window length
rolling_window_length = 2000


# Record the start time
start_time = time.time()

# Initialize an empty DataFrame to store results
results_df = pd.DataFrame()

# Loop through the data using the rolling window
for end in range(rolling_window_length, len(daily_return) + 1):
    # Slice the data for the rolling window
    window_data = daily_return.iloc[end - rolling_window_length : end]

    # Calculate VaR for the current window using the methods in the ValueAtRisk class
    VaR = ValueAtRisk(window_data, weights)

    # Calculate and display the execution time for individual methods
    VaR.variance_covariance()
    VaR.historic()
    VaR.ewma()
    VaR.monte_carlo()
    VaR.evt_monte_carlo()
    VaR.para_garch_normal()
    VaR.para_garch_t()

    current_summary = VaR.VaR_summary()

    # Append the results to the results_df
    results_df = pd.concat([results_df, current_summary])

# Calculate the elapsed time for all iterations
elapsed_time = time.time() - start_time

# Display the results DataFrame
print("\nRolling Window Value at Risk and Expected Shortfall Forecasts (in %)")
display(results_df)

# Print the total execution time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(
    f"\nTotal execution time for all iterations: {minutes} minutes and {seconds} seconds"
)
