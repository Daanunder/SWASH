from jinja2 import Template
from simulations import simulations

with open('tidal_basin_base.jinja') as base:
    template = Template(base.read())

new_file = f'runfile_{simulations.tidbas002["sim_id"]}.sws'
template.stream(sim=simulations.tidbas002).dump(new_file)

