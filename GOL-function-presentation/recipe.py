import argparse
import sys,os

import hpccm
from hpccm.primitives import copy, shell, runscript, environment, label
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.building_blocks.packages import packages
from hpccm.templates.git import git

container_version = 1.2


def main():
    parser = argparse.ArgumentParser(
        description='Simple script for generating a singularity recipe for the GOL example.')
    parser.add_argument('--build_prefix', type=str, default='/tmp/GOL_example',
                        help='Define the path in which all projects will be built (default: /tmp/GOL_example).')
    parser.add_argument('-v ', '--version', action='store_true',
                        help='print version of the container')
    args = parser.parse_args()

    if args.version:
        print(container_version)
        sys.exit(0)

    hpccm.config.set_container_format('singularity')
    hpccm.config.set_singularity_version('3.3')
    stage = hpccm.Stage()

    stage += label(metadata={'GOL_MAINTAINER': 'Simeon Ehrig'})
    stage += label(metadata={'GOL_EMAIL': 's.ehrig@hzdr.de'})
    stage += label(metadata={'GOL_Version': str(container_version)})

    # copy example inside container
    stage += copy(src='notebook', dest='/')
    stage += copy(src='jupyter_notebook_config.py', dest='/')

    # copy and build the pnwriter library
    stage += packages(ospackages=['libpng-dev'])
    png = []

    png_git = git()
    png.append(png_git.clone_step(repository='https://github.com/pngwriter/pngwriter.git',
                                  branch='dev',
                                  path='/opt/'))

    png_cmake = CMakeBuild(prefix='/notebook/pngwriter')
    png.append(png_cmake.configure_step(directory='/opt/pngwriter',
                                        opts=['-DBUILD_SHARED_LIBS=ON']))
    png.append(png_cmake.build_step(target='install'))
    png.append('rm -rf /opt/pngwriter')

    stage += shell(commands=png)

    # Copy notebook examples and pngwriter lib to the host's /tmp file system to obtain a writable file system.
    stage += runscript(commands=['if [ ! -d /tmp/GOL-xeus-cling-cuda ]; then \n'
                                 ' mkdir /tmp/GOL-xeus-cling-cuda &&'
                                 ' cp -r /notebook/ /tmp/GOL-xeus-cling-cuda\n fi',
                                 'cd /tmp/GOL-xeus-cling-cuda/notebook',
                                 'jupyter-notebook --config=/jupyter_notebook_config.py'])

    # Add the bootstrap manually because hpccm does not support .sregistry,
    recipe = stage.__str__()
    recipe = 'Bootstrap: library\nFrom: sehrig/default/xeus-cling-cuda:2.3\n\n' + recipe

    print(recipe)


if __name__ == '__main__':
    main()
