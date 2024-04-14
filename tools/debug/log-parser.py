import os
import io
import sys

import pandas as pd


if __name__ == "__main__":
    content = ""
    with open(sys.argv[1]) as fp:
        for line in fp:
            if "WIN" in line or "LOSS" in line:
                direct = 'LONG' if 'LONG' in line else 'SHORT'
                action = 'OPEN' if 'OPEN' in line else 'CLOSE'
                content += f'direct={direct},action={action},' + line.split("|")[1]
    df = pd.read_csv(io.StringIO(content), header=None)
    df = df.map(lambda x: x.split('=')[1])
    df[6] = 0
    df.columns = ['direct', 'action', 'datetime', 'open', 'close', 'atr']
    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df['side'] = df.direct.apply(lambda x: 1 if x == 'LONG' else -1)
    df['gross'] = df.side * (df.close - df.open)
    df['commis'] = (df.close + df.open) * 0.0002
    df.index = pd.to_datetime(df['datetime'].astype(float) * 1e6)
    print('=' * 20, 'Trade History', '=' * 20)
    print(df)
    print('=' * 20, 'Trade Summary', '=' * 20)
    print('    - gross:%.6f'%df.gross.sum())
    print('    - commis:%.6f'%df.commis.sum())
    print('    - net-value:%.6f'%(df.gross - df.commis).sum())
    print('=' * 20, 'End of Summary', '=' * 20)
