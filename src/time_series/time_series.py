import pandas as pd

def read_csv():
    df = pd.read_csv('/Users/tripham/Desktop/satellite-dynamic-report/src/data/csv/Housel_DD_Input.csv', index_col='Date')

    # print(df.index.tolist())
    #
    # print(df['TA'].tolist())

    # print(df)

    return [df.index.tolist(), df['TA'].tolist(), df['SW'].tolist()]


if __name__ == "__main__":
    read_csv()