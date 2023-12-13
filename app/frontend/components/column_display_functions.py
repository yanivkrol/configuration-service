import pandas as pd


def allable_campaign_column(series: pd.Series) -> pd.Series:
    return series.apply(lambda c: c or "All campaigns")
