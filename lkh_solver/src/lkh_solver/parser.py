#! /usr/bin/env python
import os

def get_keyword_index(lines, keyword):
  """
  Helper function used for parsing TSPLIB files.
  It searchs for the given `keyword` across the list of `lines`.

  Parameters
  ----------
  lines: list
    List of lines. Each element of this list is a string.
  keyword: str
    The input keyword

  Returns
  -------
  index: int
    If the keyword is found, returns the line index. `None` will be returned
    otherwise.
  """
  for i,line in enumerate(lines):
    if keyword in line:
      return i
  return None

def read_tsplib_tour(filename):
  """
  Read a tour from a TSPLIB file

  Parameters
  ----------
  filename: list
    Path to the tour file. The expected extension is `.tour`

  Returns
  -------
  tour: list
    The tour as a list of integers
  info: dict
    Extra information contained in the `.tour` file
  """
  lines = []
  # Read the raw file and dump it into a list
  with open(filename, 'rb') as f:
    while True:
      line = f.readline()
      if line.find('EOF') != -1 or not line:
        break
      lines.append(line)
  # Parse the named fields
  remaining_lines = []
  info = dict()
  for line in lines:
    if ':' in line:
      key, val_str = (item.strip() for item in line.split(':', 1))
      try:
        value = int(val_str)
      except:
        value = val_str
      if key in info:
        if type(info[key]) == str:
          value = info[key] + ' ' + value
      info[key] = value
    else:
      remaining_lines.append(line)
  lines = list(remaining_lines)
  # Read the TOUR_SECTION
  keyword = 'TOUR_SECTION'
  first = get_keyword_index(lines, keyword) + 1
  last = first + info['DIMENSION']
  tour = []
  for line in lines[first:last]:
    tour.append(int(line))
  return tour, info

def write_parameters_file(problem_file, params):
  """
  Write the parameters file used by the `lkh_solver` node to solve a TSP
  instance.

  Parameters
  ----------
  problem_file: str
    Path to the problem file (`.tsp` file)
  params: SolverParameters
    Parameters to be pased to the LKH solver. See :class:`SolverParameters` for
    details.

  Returns
  -------
  basename: str
    The basename is the `problem_file` without the file extension
  """
  def bool_to_string(value):
    return 'YES' if value else 'NO'
  basename, file_extension = os.path.splitext(problem_file)
  content =  'PROBLEM_FILE = {}\n'.format(problem_file)
  content += 'ASCENT_CANDIDATES = {:d}\n'.format(params.ascent_candidates)
  content += 'BACKBONE_TRIALS = {:d}\n'.format(params.backbone_trials)
  content += 'BACKTRACKING = {}\n'.format(bool_to_string(params.backtracking))
  content += 'EXTRA_CANDIDATES = {:d}\n'.format(params.extra_candidates)
  content += 'KICKS = {:d}\n'.format(params.kicks)
  content += 'KICK_TYPE = {:d}\n'.format(params.kick_type)
  content += 'MAX_CANDIDATES = {:d}\n'.format(params.max_candidates)
  content += 'MAX_TRIALS = {:d}\n'.format(params.max_trials)
  content += 'MOVE_TYPE = {:d}\n'.format(params.move_type)
  content += 'OUTPUT_TOUR_FILE = {}\n'.format(basename+'.tour')
  content += 'PI_FILE = {}\n'.format(basename+'.pi')
  content += 'POPULATION_SIZE = {:d}\n'.format(params.population_size)
  content += 'PRECISION = {:d}\n'.format(params.precision)
  content += 'RUNS = {:d}\n'.format(params.runs)
  content += 'SEED = {:d}\n'.format(params.seed)
  content += 'TRACE_LEVEL = {:d}'.format(params.trace_level)
  # Write the file
  with open(basename+'.par', 'w') as f:
    f.write(content)
  return basename
