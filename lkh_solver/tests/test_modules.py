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
      valid_ext =  fullpath.endswith('.tsp')
      valid_ext |= fullpath.endswith('.atsp')
      valid_ext |= fullpath.endswith('.m-pdtsp')
      if os.path.isfile(fullpath) and valid_ext:
        files.append(fullpath)
    # Solve them
    for problem_file in files:
      params = lkh.solver.SolverParameters()
      params.problem_file = problem_file
      params.trace_level = 0
      params.max_trials = 1
      params.special = problem_file.endswith('.m-pdtsp')
      tour, info = lkh.solver.lkh_solver(params)
      self.assertIsNotNone(tour)
    # Solve burma14 with 2 salesmen MINSUM
    params.salesmen = 2
    params.mtsp_min_size = 7
    params.mtsp_max_size = 8
    params.mtsp_objective = 'MINSUM'
    problem_file = [name for name in files if 'burma' in name].pop()
    params.problem_file = problem_file
    tour, info = lkh.solver.lkh_solver(params)
    self.assertIsNotNone(tour)
    # Solve br17 with 2 salesmen MINMAX_SIZE and SPECIAL options
    params.salesmen = 2
    params.special = True
    params.mtsp_min_size = 1
    params.mtsp_max_size = 16
    params.mtsp_objective = 'MINMAX_SIZE'
    problem_file = [name for name in files if 'br17' in name].pop()
    params.problem_file = problem_file
    tour, info = lkh.solver.lkh_solver(params)
    self.assertIsNotNone(tour)

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
