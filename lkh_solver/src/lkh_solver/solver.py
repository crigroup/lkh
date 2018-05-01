#!/usr/bin/env python
import os
import math
import time
import shutil
from subprocess import Popen, PIPE
# Own modules
from . import parser


class SolverParameters(object):
  sigfigs = 3
  """Number of significative figures (decimal places) to be used in the
  conversion of distances from float to integer"""

  def __repr__(self):
    # Process the SPECIAL parameter
    output = ''
    ignore_list = ['special', 'sigfigs']
    try:
      if self.special:
        output += 'SPECIAL\n'
        ignore_list += ['kicks', 'kick_type', 'move_type', 'population_size']
    except AttributeError:
      pass
    # Generate the parameters string
    for name in dir(self):
      attr = getattr(self, name)
      if name.startswith('_') or callable(attr) or name in ignore_list:
        continue
      if type(attr) is bool:
        attr = self._bool_to_string(attr)
      output += '{0} = {1}\n'.format(name.upper(), attr)
    output = output[:-1] # Remove last new line
    return output

  def __str__(self):
    return self.__repr__()

  def _bool_to_string(self, value):
    return 'YES' if value else 'NO'

  def write(self, working_path='/tmp/lkh'):
    """
    Write the parameters file used by the `lkh_solver` node to solve a TSP
    instance.

    Returns
    -------
    basename: str
      The basename is the `problem_file` without the file extension
    """
    create_dir(working_path)
    if not hasattr(self, 'problem_file'):
      raise AttributeError('PROBLEM_FILE must be specified')
    problem_name = os.path.splitext(os.path.basename(self.problem_file))[0]
    basename = os.path.join(working_path, problem_name)
    content = self.__str__()
    # Add the OUTPUT_TOUR_FILE field if missing
    if not hasattr(self, 'output_tour_file'):
      content += '\nOUTPUT_TOUR_FILE = {}'.format(basename+'.tour')
    # Add the MTSP_SOLUTION_FILE field if missing
    try:
      if self.salesmen > 1 and not hasattr(self, 'mtsp_solution_file'):
        content += '\nMTSP_SOLUTION_FILE = {}'.format(basename+'_mtsp.tour')
    except AttributeError:
      pass
    # Write the file
    with open(basename+'.par', 'w') as f:
      f.write(content)
    return basename


def create_dir(dpath):
  if not os.path.isdir(dpath):
    try:
      os.makedirs(dpath)
    except OSError:
      raise OSError('Failed to create: {}'.format(dpath))

def lkh_solver(params, pkg='lkh_solver', rosnode='lkh_solver',
                                                      working_path='/tmp/lkh'):
  """
  Run the `lkh_solver` using the given `params`. The `lkh_solver` node will
  generate several files (`.par`, `.pi`, `.tour`, etc) that can be used for
  debugging.

  Parameters
  ----------
  params: SolverParameters
    Parameters to be pased to the LKH solver. See :class:`SolverParameters` for
    details.
  pkg: str
    ROS package where the solver is available
  rosnode: str
    ROS node of the solver
  working_path: str
    Path to be used by the LKH solver to store the required intermediate files

  Returns
  -------
  tour: list
    The near-optimal tour found using the LKH heuristics.
  info: dict
    Extra information about the solver call. It includes the CPU time,
    `stdout` and `stderr`
  """
  starttime = time.time()
  # Create a TMP folder required for the GTSP solver
  tmp_path = os.path.join(working_path, 'TMP')
  create_dir(working_path)
  create_dir(tmp_path)
  # Generate the parameters file
  basename = params.write()
  # Call the LKH solver
  outpipe = PIPE
  try:
    if params.trace_level > 0:
      outpipe = None
  except AttributeError:
    pass
  process = Popen(['rosrun', pkg, rosnode, basename+'.par'],
                              cwd=working_path, stdout=outpipe, stderr=outpipe)
  stdout, stderr = process.communicate()
  # Read the tour
  tour_filename = basename+'.tour'
  tour = None
  if os.path.isfile(tour_filename):
    tour = parser.read_tsplib_tour(tour_filename)
  cpu_time = time.time() - starttime
  # Extra info
  info = dict()
  info['cpu_time'] = cpu_time
  info['stdout'] = stdout
  info['stderr'] = stderr
  # Clean up
  try:
    os.remove(basename+'.pi')
  except OSError:
    pass
  shutil.rmtree(tmp_path, ignore_errors=True)
  return tour, info
