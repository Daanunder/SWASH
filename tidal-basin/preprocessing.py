from jinja2 import Template
from simulations import simulations


def create_sws_file(sim):
    with open('tidal_basin_base.jinja') as base:
        template = Template(base.read())

    new_file = f'runfile_{sim["sim_id"]}.sws'
    template.stream(sim=sim).dump(new_file)

sim = simulations.tidbas001
create_sws_file(sim=sim)
