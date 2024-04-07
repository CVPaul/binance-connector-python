import os
import io
import sys

import pandas as pd


if __name__ == "__main__":
    content = ""
    with open(sys.argv[1]) as fp:
        for line in fp:
            if "TRADE" in line:
                direct = 'LONG' if 'LONG' in line else 'SHORT'
                action = 'OPEN' if 'OPEN' in line else 'CLOSE'
                content += f'direct={direct},action={action},' + line.split("|")[1]
    df = pd.read_csv(io.StringIO(content), header=None)
    df = df.map(lambda x: x.split('=')[1])
    df.index = pd.to_datetime(df[2].astype(float) * 1e6)
    print(df)
