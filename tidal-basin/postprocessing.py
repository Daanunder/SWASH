import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulations import simulations
import seaborn as sns


def get_data(sim):
    fpath_output_data = rundir / f"output_buoy_{sim['sim_id']}.tbl"
    df = pd.read_csv(fpath_output_data, sep='\s+', skiprows=7, index_col=0, names=sim['output_params'])
    
    # There are multiple ways of dealing with the different data columns; 1. split into different datasets (series) 2. Single dataset with multi-index
    # Split series 
    #n = sim['output_nodes']+1
    #series = [df.iloc[i::n, :] for i in range(n)]
    #print(series[0])
    #colnames = ['x%s' % round(x) for x in np.linspace(0, sim['basinlenght'], n)]
    #df2 = pd.DataFrame(columns=colnames, index=series[0].index)
    #for i,c in enumerate(colnames):
        #df2[c] = series[i]

    # Create multi index [time, space]
    time_index = df.index
    n = sim['output_nodes']+1
    space_index = ['x%6d' % round(x) for x in np.linspace(0, sim['basinlenght'], n)]*int(time_index.size/n)
    index_arrays = [time_index, space_index]
    index_tuples = list(zip(*index_arrays))
    multi_index = pd.MultiIndex.from_tuples(index_tuples, names=['Time [s]', 'Space [m]'])
    df2 = pd.DataFrame(df.values, multi_index, sim['output_params'])
    
    return df2


def plot_buoys(sim, df=None):
    if df == None:
        df = get_data(sim=sim)

    fig,ax=plt.subplots(2,1)
    df2.plot(ax=ax[0])
    ax[0].set_xlabel('Time [s]')
    ax[0].set_ylabel('Waterlevel [m]')
    for c in colnames:
        e = df2['x0'] - df2[c]
        ax[1].plot(df2.index, e, label=c)
        ax[1].set_title('Difference with boundary conditions at x=0')
        ax[1].set_xlabel('Time [s]')
        ax[1].set_ylabel('Waterlevel [m]')

    ax[1].legend()
    return plt.show()


def plot_multi_index(sim):
    df = get_data(sim=sim)
    n = sim['output_nodes']+1
    df.unstack(level=1).plot(sort_columns=True, subplots=True, grid=True, title=f"Velocity and waterlevel over time for {n} locations", layout=(n,len(sim['output_params'])), legend=True)
    #df.plot(kind='line', subplots=True, grid=True, title="Sample Data (Unit)",
            #layout=(4, 3), sharex=True, sharey=False, legend=True,    
            #style=['r', 'r', 'r', 'g', 'g', 'g', 'b', 'b', 'b', 'r', 'r', 'r'],
            #xticks=np.arange(0, len(df), 16))




