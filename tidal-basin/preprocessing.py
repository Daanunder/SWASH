from jinja2 import Template
from simulations import simulations
from pathlib import Path
import os
import subprocess
import shutil


def create_runfiles(sim):
    rundir = Path('./run_%03d' % int(sim['sim_id']))
    rundir.mkdir(parents=True, exist_ok=True)
    fpath_bottom = rundir / sim['fname_bottom']

    with open(fpath_bottom.absolute(), 'w+') as f:
        f.writelines([str(l)+ '\n' for l in sim['bottom_list']])

    with open(sim['fname_jinja_base']) as base:
        template = Template(base.read())

    fpath_runfile = rundir / f'runfile_{sim["sim_id"]}.sws'
    template.stream(sim=sim).dump(str(fpath_runfile.absolute()))

    if not (rundir / 'swashinit').exists():
        src = rundir.absolute().parent / 'swashinit'
        dst = rundir.absolute() / 'swashinit'
        shutil.copyfile(src,dst)


def run_swash(sim):
    rundir = Path('./run_%03d' % int(sim['sim_id']))
    fpath_runfile = rundir / f'runfile_{sim["sim_id"]}.sws'
    sim['rundir'] = rundir
    orig_dir = os.getcwd()
    os.chdir(rundir)
    subprocess.run(['swashrun', '-input', str(fpath_runfile.absolute())])
    os.chdir(orig_dir)



