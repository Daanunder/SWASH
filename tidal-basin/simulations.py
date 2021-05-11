import datetime as dt
import numpy as np

class simulation_parameters(object):
    # Tidal Basin
    tidbas000 = dict(
            # general
            name = 'Tidal basin',
            sim_id = '000',
            description = 'Modelling free and force behaviour of a tidal basin',
            fname_jinja_base = 'tidal_basin_base.jinja',

            # Grid spec
            basinlenght = 10000,
            xm = 100,

            # Initial conditions
            initial_cond = False,  # -> Means INIT ZERO
            # initial_cond = True -> Means velocities are derived from waterlevel, must specify initial water level elsewhere via READINP.
            # initial_cond = dict(wlev=1, vx=1, vy=1, tke=1, epsilon=1) -> all keys are optional

            # boundary conditions
            tidal_amp = 1,
            tidal_freq = np.pi*2/(12*3600),
            tidal_phase = 90,

            # bottom
            # constructs .bot file from bottom_list
            bottom_list = [10, 10],
            fname_bottom = 'flat.bot',
            swashfname = 'tidal-basin.sws',

            # Friction
            friction_type = 'MANNING', #[CONSTANT, MANNING, CHEZY, COLEBROOK]
            frictin_val = 0.019, 

            # computation
            starttime = dt.datetime(2021, 4, 20),
            simulation_time = dt.timedelta(days=5),
            timestep = 1,
            timestep_unit = 'MIN',

            # output
            output_params = ['WATLEV', 'VMAG'],
            output_start = 0, # 0 -> starttime else specify datetime or timedelta 
            output_freq = 5,
            output_freq_unit = 'MIN', #SEC MIN HR DAY
            output_nodes = 2
            )

    tidbas001 = tidbas000.copy()
    tidbas001['sim_id'] = '001'
    tidbas001['bottom_list'] = [5, 5]

    tidbas002 = tidbas000.copy()
    tidbas002['sim_id'] = '002'
    tidbas002['bottom_list'] = [20, 20]

    tidbas003 = tidbas000.copy()
    tidbas003['sim_id'] = '003'
    tidbas003['friction_type'] = None
    tidbas003['friction_val'] = None

    tidbas004 = tidbas000.copy()
    tidbas004['sim_id'] = '004'
    tidbas004['friction_type'] = 'MANNING'
    tidbas004['friction_val'] = 0.04 # m^-1/3 s

    tidbas005 = tidbas000.copy()
    tidbas005['sim_id'] = '005'
    tidbas005['friction_type'] = 'COLEBROOK'
    tidbas005['friction_val'] = 0.01  # m
 
    tidbas006 = tidbas000.copy()
    tidbas006['sim_id'] = '006'
    tidbas006['basinlenght'] = 5000

    tidbas007 = tidbas000.copy()
    tidbas007['sim_id'] = '007'
    tidbas007['basinlenght'] = 50000

    tidbas008 = tidbas000.copy()
    tidbas008['sim_id'] = '008'
    tidbas008['simulation_time'] = dt.timedelta(days=15)

    tidbas009 = tidbas000.copy()
    tidbas009['sim_id'] = '009'
    tidbas009['simulation_time'] = dt.timedelta(days=30)
