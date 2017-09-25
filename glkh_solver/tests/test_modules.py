#! /usr/bin/env python
from __future__ import print_function
import os
import unittest
import resource_retriever
# Tested module
import lkh_solver as lkh


class Test_glkh_solver(unittest.TestCase):
  def test_glkh_solver(self):
    folder = 'package://glkh_solver/gtsplib'
    path = resource_retriever.get_filename(folder, use_protocol=False)
    files = []
    for name in os.listdir(path):
      fullpath = os.path.join(path, name)
      if os.path.isfile(fullpath) and fullpath.endswith('.gtsp'):
        files.append(fullpath)
    # Solve them
    pkg = 'glkh_solver'
    rosnode = 'glkh_solver'
    params = lkh.solver.SolverParameters()
    params.trace_level = 0
    for problem_file in files:
      tour, info = lkh.solver.lkh_solver(problem_file, params, pkg, rosnode)
