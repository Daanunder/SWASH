import datetime as dt
import numpy as np

class simulations(object):
    # Tidal Basin
    tidbas001 = dict(
            # general
            name = 'Tidal basin',
            sim_id = '001',
            description = 'Modelling free and force behaviour of a tidal basin',
            basinlenght = 10000,
            xm = 100,
            # boundary conditions
            tidal_amp = 1,
            tidal_freq = np.pi*2/(12*3600),
            tidal_phase = 90,
            # bottom
            # Possibly construct .bot file from bottom definition
            botfname = 'flat.bot',
            swashfname = 'tidal-basin.sws',
            # computation
            starttime = dt.datetime(2021, 4, 20),
            simulation_time = dt.timedelta(days=5),
            timestep = 5,
            timestep_unit = 'MIN',
            # output
            output_start = 0, # 0 -> starttime else specify datetime or timedelta 
            output_freq = 5,
            output_freq_unit = 'MIN' #SEC MIN HR DAY
            )

    tidbas002 = dict(
            # general
            name = 'Tidal basin',
            sim_id = '002',
            description = 'Modelling free and force behaviour of a tidal basin',
            basinlenght = 10000,
            xm = 100,
            # boundary conditions
            tidal_amp = 1,
            tidal_freq = np.pi*2/(12*3600),
            tidal_phase = 90,
            # bottom
            # Possibly construct .bot file from bottom definition
            botfname = 'flat.bot',
            swashfname = 'tidal-basin.sws',
            # computation
            starttime = dt.datetime(2021, 4, 20),
            simulation_time = dt.timedelta(days=5),
            timestep = 10,
            timestep_unit = 'MIN',
            # output
            output_start = 0, # 0 -> starttime else specify datetime or timedelta 
            output_freq = 5,
            output_freq_unit = 'MIN' #SEC MIN HR DAY
            )




