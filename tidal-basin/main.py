from simulations import simulation_parameters

import jinja2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import datetime

from pathlib import Path
import os
import subprocess
import shutil

class swash_sim(object):

    def __init__(self, **params):
        self.__dict__.update(params)        
        
        # Filepaths
        self.rundir = Path('./run_%03d' % int(self.sim_id))
        self.rundir.mkdir(parents=True, exist_ok=True)

        self.fpath_runfile = self.rundir / f'runfile_{self.sim_id}.sws'
        self.fpath_output_data = self.rundir / f"output_buoy_{self.sim_id}.tbl"

        self.image_folder = self.rundir.absolute().parent / 'images'
        self.image_folder.mkdir(parents=True, exist_ok=True)
        self.fpath_abs_figure_jpg = self.image_folder / f"ass1_abs_{self.sim_id}.jpg"
        self.fpath_diff_figure_jpg = self.image_folder / f"ass1_diff_{self.sim_id}.jpg"

        self.fpath_print_file = self.rundir / f'runfile_{self.sim_id}.prt'

        if not (self.rundir / 'swashinit').exists():
            src = self.rundir.absolute().parent / 'swashinit'
            dst = self.rundir.absolute() / 'swashinit'
            shutil.copyfile(src,dst)

    ### Preprocessing 

    def _create_bottom_file(self):
        self.fpath_bottom = self.rundir / self.fname_bottom

        with open(self.fpath_bottom.absolute(), 'w+') as f:
            f.writelines([str(l)+ '\n' for l in self.bottom_list])

    def _create_sws_command_file(self):
        with open(self.fname_jinja_base) as base:
            template = jinja2.Template(base.read())

        template.stream(sim=self).dump(str(self.fpath_runfile.absolute()))

    def prepare_run(self):
        self._create_bottom_file()
        self._create_sws_command_file()

    ### Run simulation

    def run_swash(self):
        orig_dir = os.getcwd()
        os.chdir(self.rundir.absolute())
        subprocess.run(['swashrun', '-input', self.fpath_runfile.name])
        os.chdir(orig_dir)

    ### Postprocessing 
    def _get_data(self):
        df = pd.read_csv(self.fpath_output_data, sep='\s+', skiprows=7, index_col=0, names=self.output_params)
        
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
        n = self.output_nodes+1
        space_index = ['x%6d' % round(x) for x in np.linspace(0, self.basinlenght, n)]*int(time_index.size/n)
        index_arrays = [time_index, space_index]
        index_tuples = list(zip(*index_arrays))
        multi_index = pd.MultiIndex.from_tuples(index_tuples, names=['Time [s]', 'Space [m]'])
        df2 = pd.DataFrame(df.values, multi_index, self.output_params)
        
        return df2


#    def plot_buoys(sim, df=None):
#        if df == None:
#            df = get_data(sim=sim)
#
#        fig,ax=plt.subplots(2,1)
#        df2.plot(ax=ax[0])
#        ax[0].set_xlabel('Time [s]')
#        ax[0].set_ylabel('Waterlevel [m]')
#        for c in colnames:
#            e = df2['x0'] - df2[c]
#            ax[1].plot(df2.index, e, label=c)
#            ax[1].set_title('Difference with boundary conditions at x=0')
#            ax[1].set_xlabel('Time [s]')
#            ax[1].set_ylabel('Waterlevel [m]')
#
#        ax[1].legend()
#        return plt.show()
#

    def plot_multi_index(self):
        df = self._get_data()
        n = self.output_nodes+1
        axes = df.unstack(level=1).plot(sort_columns=True, subplots=True, grid=True, title=f"Simulation: {self.sim_id}; Velocity and waterlevel over time for {n} locations", legend=True, figsize=(12,7.5), sharex=True)
        
        for axis in axes:
            axis.legend(loc='lower right')
        plt.savefig(self.fpath_abs_figure_jpg)
        #plt.suptitle(f'Simulation: {self.sim_id}')
        #df.plot(kind='line', subplots=True, grid=True, title="Sample Data (Unit)",
                #layout=(4, 3), sharex=True, sharey=False, legend=True,    
                #style=['r', 'r', 'r', 'g', 'g', 'g', 'b', 'b', 'b', 'r', 'r', 'r'],
                #xticks=np.arange(0, len(df), 16))

        fig,ax = plt.subplots(2,1, figsize=(12,7.5))
        fig.suptitle('Differences in velocity and waterlevel compared to the boundary conditions')

        p_wlev_diff = df.unstack(level=1)['WATLEV'].diff(axis=1).iloc[:,1:].plot(ax=ax[0], title='Waterlevel [m]', legend=True)
        p_wlev_diff.set_ylabel('Waterlevel [m]')
        p_vmag_diff = df.unstack(level=1)['VMAG'].diff(axis=1).iloc[:,1:].plot(ax=ax[1], title='Velocity [m/s]', legend=True)
        p_vmag_diff.set_ylabel('Velocity [m/s]')

        for axis in [p_wlev_diff, p_vmag_diff]:
            axis.legend(loc='upper right')
        plt.savefig(self.fpath_diff_figure_jpg)
    
    def full_run(self):
        self.prepare_run()
        self.run_swash()
        self.plot_multi_index()



def run_all_simulations():
    ## Create log file
    log_messages = []
    ## Run simulations
    for k,params in simulation_parameters.__dict__.items():
        if not k.startswith('tid'):
            continue

        sim = swash_sim(**params)
        log_messages.append(f'\n Started new simulation - {sim.sim_id}')
        sim.full_run()

        
        error_msg = '** Warning          : CFL condition is violated!'
        with open(sim.fpath_print_file) as f:
            n = f.read().count(error_msg)
            if n:
                log_messages.append(f'[{n} CFL errors] - {error_msg}')

    
    logpath = Path('.') / ('errors-%s.log' % datetime.datetime.now().strftime('%y%m%d_%H%M%S'))
    with open(logpath.absolute(), 'w+') as f:
        f.writelines([str(l)+ '\n' for l in log_messages])



        


