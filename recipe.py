import argparse, sys

# release container from xeus-cling-cuda-container project
# https://github.com/ComputationalRadiationPhysics/xeus-cling-cuda-container
import xeusClingCudaContainer.hpccm.rel_container as relc

from hpccm.primitives import copy, shell, runscript, environment
from hpccm.templates.CMakeBuild import CMakeBuild
from hpccm.building_blocks.packages import packages

container_version = 1.0

def main():
    parser = argparse.ArgumentParser(
        description='Simple script for generating a singularity recipe for the GOL example.')
    parser.add_argument('--build_dir', type=str, default='/tmp/GOL_example',
                        help='Define the path in which all projects will be built (default: /tmp/GOL_example).')
    parser.add_argument('-j', type=str, help='number of build threads for make (default: -j)')
    parser.add_argument('-v ', '--version', action='store_true', help='print version of the container')
    args = parser.parse_args()

    if args.version:
        print(container_version)
        sys.exit(0)

    if args.j:
        threads = int(args.j)
        if threads < 1:
            raise ValueError('-j have to be greater than 0')
    else:
        threads=None

    stages = relc.gen_stage('singularity', args.build_dir, 'RELEASE', True, threads)
    if type(stages) is not list:
        singleStageBuild(stages)
    else:
        multiStageBuild(stages)

def singleStageBuild(stage):
    stage += environment(variables={'GOL_VERSION' : str(container_version)})

    # copy example inside container
    stage += copy(src='notebook', dest='/')

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
                                 'jupyter-lab'])

    print(stage.__str__())

def multiStageBuild(stages):
    print('multi-stage-builds are not supported at the moment', file=sys.stderr)

    sys.exit(1)

    # TODO: for a later implementation
    recipe = []
    for stage in stages:
            recipe.append('')
            recipe.append(stage.__str__())
    print('\n'.join(recipe))

if __name__ == '__main__':
    main()
