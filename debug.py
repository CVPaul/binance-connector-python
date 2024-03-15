import os

from strategy.main import Checkpoint
c = Checkpoint('strategy.trend.ckpt')
os.system(f'cat {c.filename}')
print(c.load())