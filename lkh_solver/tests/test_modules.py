#! /usr/bin/env python
from __future__ import print_function
import os
import unittest
import resource_retriever
# Tested module
import lkh_solver as lkh


class Test_lkh_solver_Modules(unittest.TestCase):
  def test_lkh_solver(self):
    folder = 'package://lkh_solver/tsplib'
    path = resource_retriever.get_filename(folder, use_protocol=False)
    files = []
    for name in os.listdir(path):
      fullpath = os.path.join(path, name)
      if os.path.isfile(fullpath) and fullpath.endswith('.tsp'):
        files.append(fullpath)
    # Solve them
    params = lkh.solver.SolverParameters()
    params.trace_level = 0
    for problem_file in files:
      tour, info = lkh.solver.lkh_solver(problem_file, params)

  def test_SolverParameters(self):
    params = lkh.solver.SolverParameters()
    params.ascent_candidates = 1
    params.backbone_trials = 0
    params.backtracking = False
    params.extra_candidates = 0
    params.kicks = 1
    params.kick_type = 0
    params.max_candidates = 30
    params.max_trials = 1000
    params.move_type = 5
    params.population_size = 1
    params.precision = 10
    params.runs = 1
    params.seed = 1
    params.trace_level = 1
    self.assertRaises(TypeError, setattr, args=(params, 123, 'non_existent'))
