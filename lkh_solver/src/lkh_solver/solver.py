#!/usr/bin/env python
import os
import math
import time
from subprocess import Popen, PIPE
# Own modules
from . import parser


class SolverParameters(object):
  _isfrozen = False
  ascent_candidates = 50
  """The number of candidate edges to be associated with each node during the
  ascent. The candidate set is complemented such that every candidate edge is
  associated with both its two end nodes."""
  backbone_trials = 0
  """The number of backbone trials in each run."""
  backtracking = False
  """Specifies whether a backtracking `K`-opt move is to be used as the
  first move in a sequence of moves (where `K = move_type`)"""
  extra_candidates = 0
  """Number of extra candidate edges to be added to the candidate set of
  each node."""
  kicks = 1
  """Specifies the number of times to "kick" a tour found by Lin-Kernighan.
  Each kick is a random K-swap kick. However, if KICKS is zero, then LKH's
  special kicking strategy, `WALK`, is used in stead"""
  kick_type = 0
  """Specifies the value of K for a random K-swap kick (an extension of the
  double-bridge move). If `KICK_TYPE` is zero, then the LKH's special
  kicking strategy, `WALK`, is used."""
  max_candidates = 30
  """The maximum number of candidate edges to be associated with each node.
  Default: 30"""
  max_trials = 1000
  """The maximum number of trials in each run."""
  move_type = 5
  """Specifies the sequential move type to be used in local search. A value
  `K >= 2` signifies that a sequential `K`-opt move is to be used."""
  population_size = 1
  """Specifies the maximum size of the population in LKH's genetic
  algorithm. Tours found by the first `POPULATION_SIZE` runs constitute an
  initial population of tours. In each of the remaining runs two tours
  (parents) from the current population is recombined into a new tour
  (child) using a variant of the Edge Recombination Crossover (ERX). The
  parents are chosen with random linear bias towards the best members of the
  population. The child is used as initial tour for the next run. If this
  run produces a tour better than the worst tour of the population, then the
  resulting tour replaces the worst tour. Premature convergence is avoided
  by requiring that all tours in the population have different costs."""
  precision = 10
  """The internal precision in the representation of transformed distances (10
  corresponds to 2 decimal places)"""
  runs = 1
  """The total number of runs."""
  seed = 1
  """Specifies the initial seed for random number generation."""
  trace_level = 1
  """Specifies the level of detail of the output given during the solution
  process. The value 0 signifies a minimum amount of output. The higher the
  value is the more information is given"""

  def __init__(self):
    self._freeze()

  def __repr__(self):
    output = ''
    for name in dir(self):
      attr = getattr(self, name)
      if not name.startswith('_') and not callable(attr):
        output += '{0}: {1}\n'.format(name.upper(), attr)
    output = output[:-1] # Remove last new line
    return output

  def __setattr__(self, key, value):
    if self._isfrozen and not hasattr(self, key):
      raise TypeError( '{} is a frozen class'.format(type(self)) )
    object.__setattr__(self, key, value)

  def __str__(self):
    return self.__repr__()

  def _freeze(self):
    self._isfrozen = True

  def initialized(self):
    """
    Return `True` if the parameters have been initialized. `False` otherwise.
    """
    initialized = True
    for name in dir(self):
      attr = getattr(self, name)
      if name.startswith('_') or callable(attr):
        continue
      if attr is None:
        initialized = False
        break
    return initialized

def lkh_solver(problem_file, params, pkg='lkh_solver', rosnode='lkh_solver'):
  """
  Run the `lkh_solver` on the given `problem_file`. The `lkh_solver` node will
  generate several files (`.par`, `.pi`, `.tour`, etc) that can be used for
  debugging.

  Parameters
  ----------
  problem_file: str
    The problem file using the TSPLIB format. The expected extension of the
    file is `.tsp`.
  params: SolverParameters
    Parameters to be pased to the LKH solver. See :class:`SolverParameters` for
    details.
  pkg: str
    ROS package where the solver is available
  rosnode: str
    ROS node of the solver

  Returns
  -------
  tour: list
    The near-optimal tour found using the LKH heuristics.
  info: dict
    Extra information about the solver call. It includes the CPU time,
    `stdout` and `stderr`
  """
  starttime = time.time()
  # Check parameters have been initialized
  if not params.initialized():
    raise ValueError('SolverParameters have not been initialized')
  # Create a TMP folder required for the GTSP solver
  def create_dir(dpath):
    if not os.path.isdir(dpath):
      try:
        os.mkdir(dpath)
      except OSError:
        raise OSError('Failed to create: {}'.format(dpath))
  working_path = os.path.expanduser('~/.ros/lkh')
  tmp_path = os.path.join(working_path, 'TMP')
  create_dir(working_path)
  create_dir(tmp_path)
  # Generate the parameters file
  basename = parser.write_parameters_file(problem_file, params, working_path)
  # Call the LKH solver
  if params.trace_level > 0:
    outpipe = None
  else:
    outpipe = PIPE
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
  os.remove(basename+'.pi')
  os.rmdir(tmp_path)
  return tour, info
