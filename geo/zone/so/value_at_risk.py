#!/usr/bin/env python

# from https://codereview.stackexchange.com/questions/287718/value-at-risk-forecast-generator

# Standard library imports
import functools
import time
import warnings

# Related third-party imports
from arch import arch_model
from IPython.display import display
from scipy.stats import gumbel_r, norm
from tqdm import tqdm
import numpy as np
import pandas as pd
import yfinance as yf

# Suppress warnings
warnings.filterwarnings("ignore")


# Define a list of ticker symbols
ticker_list = ["^GSPC", "^N225", "GC=F", "000001.SS", "VBMFX", "^IXIC", "VWO"]

# Define corresponding names for the assets
name_list = [
    "S&P 500 Index",
    "Nikkei 225 Index",
    "Gold",
    "Shanghai Composite Index",
    "Vanguard Bond Index Fund",
    "Nasdaq Index",
    "Vanguard FTSE EM Index ETF",
]

# Define portfolio weights (you can choose either equal weights or custom weights)
weights = np.full(
    shape=len(ticker_list), fill_value=1 / len(ticker_list)
)  # Equally weighted portfolio

# Define the start and end dates for historical data
start_date = "2001-01-01"
end_date = "2021-12-31"


def get_stock_prices(ticker_list, name_list, start, end):
    """
    Retrieves the adjusted closing prices for a list of assets from Yahoo Finance.

    Parameters:
    - ticker_list (list): List of asset codes from Yahoo Finance.
    - name_list (list): List of corresponding asset names.
    - start (str): Start date for data retrieval (YYYY-MM-DD).
    - end (str): End date for data retrieval (YYYY-MM-DD).

    Returns:
    - portfolio_prices (DataFrame): DataFrame containing adjusted close prices of the assets.
    """
    stock_prices = pd.DataFrame()

    for ticker, name in zip(ticker_list, name_list):
        stock_price = yf.download(ticker, start=start, end=end)
        stock_price.rename(columns={"Adj Close": name}, inplace=True)
        if stock_prices.empty:
            stock_prices = stock_price[name].to_frame()
        else:
            stock_prices = stock_prices.merge(
                stock_price[name], right_index=True, left_index=True
            )

    return stock_prices


# Execution
stock_prices = get_stock_prices(ticker_list, name_list, start_date, end_date)

if stock_prices is not None:
    # Calculate log-returns
    daily_return = np.log(stock_prices / stock_prices.shift(1)).dropna()

    # Display prices and returns
    print("\nAdjusted Closing Prices:")
    display(stock_prices)
    print("\nLog-Returns:")
    display(daily_return)
else:
    print("No data available.")


# Covariance matrix
cov_matrix = daily_return.cov()

# Correlation matrix
corr_matrix = daily_return.corr()

print("\nCovariance Matrix:")
display(cov_matrix)

print("\nCorrelation Matrix:")
display(corr_matrix)


# Check Returns and Weights array lengths
if daily_return.shape[1] != len(weights):
    raise ValueError(
        "The number of columns in 'daily_return' does not match the length of 'weights'."
    )
else:
    print("The number of columns in 'daily_return' does match the length of 'weights'.")

# Print other information (optional)
# print(daily_return.shape, len(weights))
# print(daily_return.columns)


# Time Tracker per VaR Model
# Boolean flag to control timing decorator
enable_timing = False  # Set to True to enable timing, False to disable


# Timing decorator with condition
def timing_decorator(func):
    """Measure execution time of each function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if enable_timing:  # Check if timing should be enabled
            start_time = time.time()  # Record the start time before function execution
        result = func(*args, **kwargs)  # Execute the function
        if enable_timing:  # Check if timing should be enabled
            end_time = time.time()  # Record the end time after function execution
            elapsed_time = end_time - start_time  # Calculate calculation time
            print(
                f"The function {func.__name__!r} took {elapsed_time:.4f} seconds to complete."
            )
        return result

    return wrapper


class ValueAtRisk:
    """
    A class to calculate various Value at Risk (VaR) methods.
    """

    # Constants
    AMOUNT = 100  # 100 for percentage VaR/ES values or invesmtent amount for absolut VaR/ES values
    CONFIDENCE_LEVELS = {
        "95%": 0.05,
        "99%": 0.01,
    }  # Dictionary of confidence levels and their corresponding significance levels
    SIMULATIONS = 100000  # Number of Monte Carlo simulations
    CONFIDENCE_LEVEL_95 = CONFIDENCE_LEVELS[
        "95%"
    ]  # Significance level for 95% confidence
    CONFIDENCE_LEVEL_99 = CONFIDENCE_LEVELS[
        "99%"
    ]  # Significance level for 99% confidence

    def __init__(self, daily_return, weights):
        """
        Initialize the class with daily returns and portfolio weights.

        Args:
            daily_return (pd.DataFrame): DataFrame of daily returns.
            weights (list): List of portfolio weights.
        """
        self.daily_return = daily_return
        self.weights = weights
        self.cov_matrix = (
            daily_return.cov()
        )  # Compute the covariance matrix of daily returns

    def calculate_portfolio_metrics(self):
        """
        Calculate common portfolio metrics.

        Returns:
            tuple: Portfolio mean, standard deviation, and portfolio returns.
        """
        daily_mean = np.average(self.daily_return, axis=1, weights=self.weights)
        port_mean = daily_mean.mean()  # Calculate portfolio mean return
        port_stdev = np.sqrt(
            np.dot(self.weights.T, np.dot(self.cov_matrix, self.weights))
        )  # Calculate portfolio standard deviation
        portfolio_returns = np.average(
            self.daily_return, axis=1, weights=self.weights
        )  # Calculate portfolio returns

        return port_mean, port_stdev, portfolio_returns

    def calculate_var_es(self, confidence_level, portfolio_returns):
        """
        Calculate VaR and ES for a given confidence level.

        Args:
            confidence_level (str): Confidence level, e.g., "95%" or "99%".
            portfolio_returns (np.array): Portfolio returns.

        Returns:
            tuple: VaR and ES values.
        """
        var_percentile = np.percentile(
            portfolio_returns, self.CONFIDENCE_LEVELS[confidence_level] * 100
        )  # Calculate VaR at the specified confidence level
        es = np.mean(
            portfolio_returns[portfolio_returns <= var_percentile]
        )  # Calculate ES

        return var_percentile, es

    def compute_var_es(self, port_mean, port_stdev, portfolio_returns):
        """
        Compute VaR and ES values given portfolio statistics.

        Args:
            port_mean (float): Portfolio mean return.
            port_stdev (float): Portfolio standard deviation.
            portfolio_returns (np.array): Portfolio returns.

        Returns:
            tuple: VaR and ES values.
        """
        z_scores = norm.ppf([self.CONFIDENCE_LEVEL_95, self.CONFIDENCE_LEVEL_99])

        var_values = port_mean + z_scores * port_stdev  # Compute VaR values

        es_95 = np.mean(
            portfolio_returns[portfolio_returns <= var_values[0]]
        )  # Compute ES at 95% confidence
        es_99 = np.mean(
            portfolio_returns[portfolio_returns <= var_values[1]]
        )  # Compute ES at 99% confidence

        return var_values, (es_95, es_99)

    def compute_portfolio_returns(self):
        """
        Compute portfolio returns.

        Returns:
            np.array: Portfolio returns.
        """
        return np.average(self.daily_return, axis=1, weights=self.weights)

    # ------------------- Variance-Covariance VaR -------------------
    def variance_covariance(self):
        """
        Compute Parametric VaR using the variance-covariance method.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Calculate portfolio mean return, standard deviation, and portfolio returns
        port_mean, port_stdev, portfolio_returns = self.calculate_portfolio_metrics()

        # Compute VaR and ES for different confidence levels
        var_values, es_values = self.compute_var_es(
            port_mean, port_stdev, portfolio_returns
        )

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {}
        for confidence_level, var_value in zip(
            self.CONFIDENCE_LEVELS.keys(), var_values
        ):
            var_dict[f"VaR({confidence_level})"] = var_value
            es_95, es_99 = es_values
            var_dict[f"ES({confidence_level})"] = {
                "95%": es_95,
                "99%": es_99,
            }[confidence_level]

        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Historical Simulation VaR -------------------
    def historic(self):
        """
        Compute Historical VaR.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Compute portfolio returns using historical data
        portfolio_returns = self.compute_portfolio_returns()

        # Initialize a dictionary to store VaR and ES values
        var_dict = {}

        # Calculate VaR and ES for each confidence level
        for confidence_level in self.CONFIDENCE_LEVELS.keys():
            var_percentile, es = self.calculate_var_es(
                confidence_level, portfolio_returns
            )
            var_dict[f"VaR({confidence_level})"] = var_percentile
            var_dict[f"ES({confidence_level})"] = es

        # Return the results as a DataFrame
        return pd.DataFrame(var_dict, index=[date])

    # ------------------- EMWA VaR -------------------
    @timing_decorator
    def ewma(self, lambda_factor=0.94):
        """
        Compute VaR using the Exponentially Weighted Moving Average (EWMA) method.

        Args:
            lambda_factor (float): Smoothing parameter for EWMA.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Convert daily returns to numpy array
        daily_returns = self.daily_return.values

        # Calculate squared returns
        returns_squared = daily_returns**2

        # Initialize an EWMA covariance matrix
        ewma_cov_matrix = self.daily_return.cov().values

        # Update the covariance matrix iteratively
        for ti in range(1, len(self.daily_return)):
            returns_vector = daily_returns[ti]
            returns_squared_vector = returns_squared[ti]

            # Update the EWMA covariance matrix
            ewma_cov_matrix = (
                lambda_factor * ewma_cov_matrix
                + (1 - lambda_factor) * np.outer(returns_vector, returns_vector)
                + (1 - lambda_factor) * ewma_cov_matrix * returns_squared_vector
            )

        # Calculate portfolio mean return, standard deviation, and portfolio returns
        port_mean, port_stdev, portfolio_returns = self.calculate_portfolio_metrics()

        # Compute VaR and ES for different confidence levels
        var_values, es_values = self.compute_var_es(
            port_mean, port_stdev, portfolio_returns
        )

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {}
        for confidence_level, var_value in zip(
            self.CONFIDENCE_LEVELS.keys(), var_values
        ):
            var_dict[f"VaR({confidence_level})"] = var_value
            es_95, es_99 = es_values
            var_dict[f"ES({confidence_level})"] = {
                "95%": es_95,
                "99%": es_99,
            }[confidence_level]

        return pd.DataFrame(var_dict, index=[date])

        # ------------------- Monte Carlo VaR Normal -------------------

    @timing_decorator
    def monte_carlo_normal(self):
        """
        Compute Monte Carlo VaR considering the correlation between assets.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Calculate mean returns and covariance matrix for assets
        asset_mean_returns = self.daily_return.mean()
        cov_matrix = self.daily_return.cov()

        # Simulate returns using a multivariate normal distribution
        simulated_returns = np.random.multivariate_normal(
            asset_mean_returns, cov_matrix, self.SIMULATIONS
        )

        # Calculate portfolio P&L by dot product of simulated returns and weights
        portfolio_pnl = np.dot(simulated_returns, self.weights)

        # Calculate VaR percentiles and Expected Shortfall (ES)
        var_percentiles = np.percentile(
            portfolio_pnl,
            [self.CONFIDENCE_LEVEL_95 * 100, self.CONFIDENCE_LEVEL_99 * 100],
        )
        es_95 = np.mean(portfolio_pnl[portfolio_pnl <= var_percentiles[0]])
        es_99 = np.mean(portfolio_pnl[portfolio_pnl <= var_percentiles[1]])

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {
            "VaR(95%)": var_percentiles[0],
            "VaR(99%)": var_percentiles[1],
            "ES(95%)": es_95,
            "ES(99%)": es_99,
        }

        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Monte Carlo Extreme Value Gumbel -------------------
    @timing_decorator
    def evt_monte_carlo_gumbel(self):
        """
        Compute Extreme Value Theory Monte Carlo VaR using the Gumbel distribution.

        Returns:
            pd.DataFrame: DataFrame with VaR values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Calculate mean returns and covariance matrix for assets
        asset_mean_returns = self.daily_return.mean()
        cov_matrix = self.daily_return.cov()

        # Simulate returns using a multivariate normal distribution
        simulated_returns = np.random.multivariate_normal(
            asset_mean_returns, cov_matrix, self.SIMULATIONS
        )

        # Calculate portfolio P&L by dot product of simulated returns and weights
        portfolio_pnl = np.dot(simulated_returns, self.weights)

        # Select top 10% block maxima for Gumbel distribution fit
        block_maxima = -np.sort(-portfolio_pnl)[: int(0.1 * self.SIMULATIONS)]

        # Fit a Gumbel distribution to block maxima
        loc, scale = gumbel_r.fit(block_maxima)

        # Generate Gumbel losses
        gumbel_losses = -np.random.gumbel(loc, scale, self.SIMULATIONS)

        # Calculate VaR percentiles
        var_percentiles = np.percentile(
            gumbel_losses,
            [self.CONFIDENCE_LEVEL_95 * 100, self.CONFIDENCE_LEVEL_99 * 100],
        )

        # Calculate Expected Shortfall (ES)
        es_95 = np.mean(gumbel_losses[gumbel_losses <= var_percentiles[0]])
        es_99 = np.mean(gumbel_losses[gumbel_losses <= var_percentiles[1]])

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {
            "VaR(95%)": var_percentiles[0],
            "VaR(99%)": var_percentiles[1],
            "ES(95%)": es_95,
            "ES(99%)": es_99,
        }

        return pd.DataFrame(var_dict, index=[date])

    # ------------------- GARCH VaR Normal -------------------
    @timing_decorator
    def garch_normal(self):
        """
        Compute GARCH VaR using a normal distribution and calculate ES empirically.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Compute the weighted average return of the portfolio
        weighted_avg = pd.DataFrame()
        weighted_avg["weighted_avg"] = (
            np.average(self.daily_return, axis=1, weights=self.weights) * 100
        )

        # Fit a GARCH model with a normal distribution
        am = arch_model(
            weighted_avg["weighted_avg"], vol="Garch", p=1, o=0, q=1, dist="normal"
        )
        res = am.fit(disp="off")
        forecasts = res.forecast()
        cond_mean = forecasts.mean.iloc[-1].values
        cond_var = forecasts.variance.iloc[-1].values

        # Calculate z-scores for the specified confidence levels
        z_scores = norm.ppf([self.CONFIDENCE_LEVEL_95, self.CONFIDENCE_LEVEL_99])

        # Calculate Value at Risk (VaR)
        value_at_risk = cond_mean + np.sqrt(cond_var) * z_scores
        var_95, var_99 = value_at_risk

        # Calculate Expected Shortfall (ES)
        es_95 = np.mean(
            weighted_avg[weighted_avg["weighted_avg"] <= var_95]["weighted_avg"]
        )
        es_99 = np.mean(
            weighted_avg[weighted_avg["weighted_avg"] <= var_99]["weighted_avg"]
        )

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {
            "VaR(95%)": var_95 / 100,
            "VaR(99%)": var_99 / 100,
            "ES(95%)": es_95 / 100,
            "ES(99%)": es_99 / 100,
        }

        return pd.DataFrame(var_dict, index=[date])

    # ------------------- GARCH VaR Skewed-t -------------------
    @timing_decorator
    def garch_t(self):
        """
        Compute GARCH VaR using a skewed-t distribution.

        Returns:
            pd.DataFrame: DataFrame with VaR and ES values.
        """
        # Determine the calculation date as the maximum date in daily returns plus one day
        date = self.daily_return.index.max() + pd.Timedelta(days=1)

        # Compute the weighted average return of the portfolio
        weighted_avg = pd.DataFrame()
        weighted_avg["weighted_avg"] = (
            np.average(self.daily_return, axis=1, weights=self.weights) * 100
        )

        # Fit a GARCH model with a skewed-t distribution
        am = arch_model(
            weighted_avg["weighted_avg"], vol="Garch", p=1, o=0, q=1, dist="skewt"
        )
        res = am.fit(disp="off")
        forecasts = res.forecast()
        cond_mean = forecasts.mean.iloc[-1].values
        cond_var = forecasts.variance.iloc[-1].values

        # Calculate quantiles for the specified confidence levels
        q = am.distribution.ppf(
            [self.CONFIDENCE_LEVEL_95, self.CONFIDENCE_LEVEL_99],
            res.params[-2:],
        )

        # Calculate Value at Risk (VaR)
        value_at_risk = cond_mean + np.sqrt(cond_var) * q
        var_95, var_99 = value_at_risk

        # Calculate Expected Shortfall (ES)
        es_95 = np.mean(
            weighted_avg[weighted_avg["weighted_avg"] <= var_95]["weighted_avg"]
        )
        es_99 = np.mean(
            weighted_avg[weighted_avg["weighted_avg"] <= var_99]["weighted_avg"]
        )

        # Organize results into a dictionary for VaR and ES and return as a DataFrame
        var_dict = {
            "VaR(95%)": var_95 / 100,
            "VaR(99%)": var_99 / 100,
            "ES(95%)": es_95 / 100,
            "ES(99%)": es_99 / 100,
        }

        return pd.DataFrame(var_dict, index=[date])

    # ------------------- Summary -------------------
    def VaR_summary(self):
        """
        Generate a summary of all VaR calculations.

        Returns:
            pd.DataFrame: DataFrame with VaR summary scaled by the specified amount.
        """
        # List of VaR calculation methods
        methods = [
            "Parametric",
            "Historical Simulation",
            "EWMA",
            "Monte Carlo (Normal)",
            "EVT Monte Carlo (Gumbel)",
            "GARCH (Normal)",
            "GARCH (Skewed-t)",
        ]

        # Calculate VaR and ES for each method and store in a list
        calculations = [
            self.variance_covariance(),
            self.historic(),
            self.ewma(),
            self.monte_carlo_normal(),
            self.evt_monte_carlo_gumbel(),
            self.garch_normal(),
            self.garch_t(),
        ]

        # Create a dictionary mapping method names to their corresponding VaR and ES calculations
        results = dict(zip(methods, calculations))

        # Concatenate the results into a summary DataFrame
        summary = pd.concat(results, axis=0)

        # Scale the results by the specified amount (100 for percentage VaR/ES or investment amount for absolute VaR/ES)
        summary *= self.AMOUNT

        return summary


# Record the start time
start_time = time.time()

# Execution
if __name__ == "__main__":
    # Create an instance of the ValueAtRisk class with daily returns and weights
    VaR = ValueAtRisk(daily_return, weights)

# Calculate the VaR summary using the VaR_summary method
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
print("\nValue at Risk and Expected Shortfall one-day ahead Forecast (in %):")
display(summary_df)

# Define the rolling window length as a constant
ROLLING_WINDOW_LENGTH = 503

# Record the start time
start_time = time.time()

# Initialize an empty DataFrame to store results
results_df = pd.DataFrame()

# Calculate the total number of iterations
total_iterations = len(daily_return) - ROLLING_WINDOW_LENGTH + 1

# Define a custom bar format
custom_bar_format = (
    "{desc}: {percentage:3.0f}%|\x1b[32m█{bar}\x1b[0m| Iteration {n_fmt}/{total_fmt} "
    "[Elapsed Time: {elapsed}, Remaining Time: {remaining}, Rate: {rate_fmt}]"
)

# Initialize dictionaries to store the calculation times for each method
calculation_times = {
    "variance_covariance": 0,
    "historic": 0,
    "ewma": 0,
    "monte_carlo_normal": 0,
    "evt_monte_carlo_gumbel": 0,
    "garch_normal": 0,
    "garch_t": 0,
}

# Initialize the tqdm progress bar
with tqdm(
    total=total_iterations,
    desc="Rolling Window",
    unit="iteration",
    bar_format=custom_bar_format,
    ascii=False,
) as pbar:
    start_time = time.time()  # Record the start time

    # Loop through the data using the rolling window
    for end in range(ROLLING_WINDOW_LENGTH, len(daily_return) + 1):
        # Slice the data for the rolling window
        window_data = daily_return.iloc[end - ROLLING_WINDOW_LENGTH : end]

        # Calculate VaR for the current window using the methods in the ValueAtRisk class
        VaR = ValueAtRisk(window_data, weights)

        # Calculate and display the execution time for individual methods
        start_method_time = time.time()
        VaR.variance_covariance()
        calculation_times["variance_covariance"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.historic()
        calculation_times["historic"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.ewma()
        calculation_times["ewma"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.monte_carlo_normal()
        calculation_times["monte_carlo_normal"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.evt_monte_carlo_gumbel()
        calculation_times["evt_monte_carlo_gumbel"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.garch_normal()
        calculation_times["garch_normal"] += time.time() - start_method_time

        start_method_time = time.time()
        VaR.garch_t()
        calculation_times["garch_t"] += time.time() - start_method_time

        current_summary = VaR.VaR_summary()

        # Append the results to the results_df
        results_df = pd.concat([results_df, current_summary])

        # Update the tqdm progress bar
        pbar.update(1)

        # Calculate elapsed time
        elapsed_time = time.time() - start_time

        # Calculate estimated remaining time
        remaining_iterations = total_iterations - pbar.n
        estimated_remaining_time = (elapsed_time / pbar.n) * remaining_iterations

        # Update the progress bar with remaining and elapsed time
        pbar.set_postfix(
            Elapsed=f"{elapsed_time:.0f}s", Remaining=f"{estimated_remaining_time:.0f}s"
        )

# Calculate the total execution time for all iterations
total_execution_time = time.time() - start_time

# Display the total calculation times for each method
print("\nTotal Calculation Times per Method:")
for method, time_elapsed in calculation_times.items():
    print(f"{method}: {time_elapsed:.2f} seconds")

# Display the results DataFrame
print("\nRolling Window Value at Risk and Expected Shortfall Forecasts (in %):")
display(results_df)

# Print the total execution time
minutes = int(total_execution_time // 60)
seconds = int(total_execution_time % 60)
print(
    f"\nTotal execution time for all iterations: {minutes} minutes and {seconds} seconds"
)
