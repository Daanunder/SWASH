import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulations import simulations

sim = simulations.tidbas002

fname = f"output_buoy_{sim['sim_id']}.tbl"
df = pd.read_csv(fname, sep='\s+', skiprows=7, index_col=0, names=['Time', 'Waterlevel'])
series = [df.iloc[i::6, :] for i in range(6)]
colnames = ['x0', 'x2000', 'x4000', 'x6000', 'x8000', 'x10000']

df2 = pd.DataFrame(columns=colnames, index=series[0].index)

for i,c in enumerate(colnames):
    df2[c] = series[i]


fig,ax=plt.subplots(2,1)
df2.plot(ax=ax[0])
e1 = df2['x0'] - df2['x2000']
e2 = df2['x0'] - df2['x4000']
e3 = df2['x0'] - df2['x6000']
e4 = df2['x0'] - df2['x8000']
e5 = df2['x0'] - df2['x10000']
ax[1].plot(df2.index, e1, label='x2000')
ax[1].plot(df2.index, e2, label='x4000')
ax[1].plot(df2.index, e3, label='x6000')
ax[1].plot(df2.index, e4, label='x8000')
ax[1].plot(df2.index, e5, label='x10000')
ax[1].legend()
plt.show()
