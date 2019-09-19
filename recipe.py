import argparse
import sys

# release container from xeus-cling-cuda-container project
# https://github.com/ComputationalRadiationPhysics/xeus-cling-cuda-container
import xeusClingCudaContainer.generator as gn

from hpccm.primitives import copy, shell, runscript, environment, label
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.building_blocks.packages import packages

container_version = 1.1


def main():
    parser = argparse.ArgumentParser(
        description='Simple script for generating a singularity recipe for the GOL example.')
    parser.add_argument('--build_prefix', type=str, default='/tmp/GOL_example',
                        help='Define the path in which all projects will be built (default: /tmp/GOL_example).')
    parser.add_argument(
        '-j', type=str, help='number of build threads for make (default: -j)')
    parser.add_argument(
        '-l', type=str, help='number of linker threads for the cling build (default: -j)')
    parser.add_argument('-v ', '--version', action='store_true',
                        help='print version of the container')
    args = parser.parse_args()

    if args.version:
        print(container_version)
        sys.exit(0)

    if args.j:
        threads = int(args.j)
        if threads < 1:
            raise ValueError('-j have to be greater than 0')
    else:
        threads = None

    if args.l:
        linker_threads = int(args.l)
        if linker_threads < 1:
            raise ValueError('-l have to be greater than 0')
    else:
        linker_threads = None

    xcc_gen = gn.XCC_gen(build_prefix=args.build_prefix,
                         threads=threads,
                         linker_threads=linker_threads)
    stage = xcc_gen.gen_release_single_stage()

    stage += label(metadata={'GOL_MAINTAINER': 'Simeon Ehrig'})
    stage += label(metadata={'GOL_EMAIL': 's.ehrig@hzdr.de'})
    stage += label(metadata={'GOL_Version': str(container_version)})

    # copy example inside container
    stage += copy(src='notebook', dest='/')
    stage += copy(src='jupyter_notebook_config.py', dest='/')

    # copy and build the pnwriter library
    stage += copy(src='pngwriter', dest='/opt')
    stage += packages(ospackages=['libpng-dev'])
    cmake = CMakeBuild(prefix='/notebook/pngwriter')
    stage += shell(commands=[cmake.configure_step(directory='/opt/pngwriter',
                                                  opts=['-DBUILD_SHARED_LIBS=ON']),
                             cmake.build_step(target='install'),
                             'rm -rf /opt/pngwriter'])

    # Copy notebook examples and pngwriter lib to the host's /tmp file system to obtain a writable file system.
    stage += runscript(commands=['if [ ! -d /tmp/GOL-xeus-cling-cuda ]; then \n'
                                 ' mkdir /tmp/GOL-xeus-cling-cuda &&'
                                 ' cp -r /notebook/ /tmp/GOL-xeus-cling-cuda\n fi',
                                 'cd /tmp/GOL-xeus-cling-cuda/notebook',
                                 'jupyter-notebook --config=/jupyter_notebook_config.py'])

    print(stage.__str__())


if __name__ == '__main__':
    main()
