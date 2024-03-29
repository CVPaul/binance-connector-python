import os
import io
import sys

import pandas as pd


if __name__ == "__main__":
    content = ""
    with open(sys.argv[1]) as fp:
        for line in fp:
            if "ORDER" in line:
                content += line.split("--orders=")[1]
    df = pd.read_csv(io.StringIO(content), header=None)
    print(df)
