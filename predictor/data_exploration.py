import pandas as pd

def dataset_exploration(df):
    return df.head().to_html(
        classes="table table-bordered table-striped table-sm",
        index=False
    )

def data_exploration(df):
    return df.describe().to_html(
        classes="table table-bordered table-striped table-sm"
    )