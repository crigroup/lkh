#! /usr/bin/env python
import os
import numpy as np
import networkx as nx


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

def write_tsplib(filename, graph, params, sigfigs=3, nodelist=None,
                                        demand=None, capacity=None, depot=None):
  """
  Write the problem file used by the `lkh_solver` to solve a TSP/ATSP
  instance.

  Parameters
  ----------
  filename: str
    Path where the file will be written. Use `.tsp` for symmetric TSP problems
    and `.atsp` for asymmetric TSP problems.
  graph: NetworkX graph
    The input graph. For symmetric TSP it must be of type `nx.Graph`, for the
    asymmetric it must be of type `nx.DiGraph`
  params: SolverParameters
    Parameters to be pased to the LKH solver. See :class:`SolverParameters` for
    details.
  nodelist: list
    The rows and columns are ordered according to the nodes in `nodelist`.

  Returns
  -------
  basename: str
    The basename is equal to the `filename` without the file extension
  """
  problem_name, extension = os.path.splitext(os.path.basename(filename))
  if extension.lower() == '.tsp':
    problem_type = 'TSP'
    if graph.is_directed():
      raise ValueError('Mismatch between file extension and graph type')
  elif extension.lower() == '.atsp':
    problem_type = 'ATSP'
    if not graph.is_directed():
      raise ValueError('Mismatch between file extension and graph type')
  elif extension.lower() == '.m-pdtsp':
    problem_type = 'm-PDTSP'
    if demand is None:
      raise AttributeError('Missing required arg for m-PDTSP: demand')
    if capacity is None:
      raise AttributeError('Missing required arg for m-PDTSP: capacity')
    if depot is None:
      raise AttributeError('Missing required arg for m-PDTSP: depot')
  else:
    raise ValueError('File extension is not supported'.format(extension))
  num_nodes = graph.number_of_nodes()
  ## TSP/ATSP File
  content =  'NAME: {}\n'.format(problem_name)
  content += 'TYPE: {}\n'.format(problem_type)
  content += 'COMMENT: Task with {} nodes\n'.format(num_nodes)
  content += 'DIMENSION: {}\n'.format(num_nodes)
  if problem_type == 'm-PDTSP':
    content += 'CAPACITY: {}\n'.format(capacity)
    content += 'DEMAND_DIMENSION: {}\n'.format(demand.shape[1])
  content += 'EDGE_WEIGHT_TYPE: EXPLICIT\n'
  content += 'EDGE_WEIGHT_FORMAT: FULL_MATRIX \n'
  # Add the EDGE_WEIGHT_SECTION
  content += 'EDGE_WEIGHT_SECTION\n'
  matrix = np.asarray(nx.to_numpy_matrix(graph, nodelist, weight='weight'))
  matrix = np.int0(matrix * (10**sigfigs))
  content += '\n'.join(' '.join(str(i) for i in row) for row in matrix)
  if problem_type == 'm-PDTSP':
    # Add the DEMAND_SECTION
    content += '\nDEMAND_SECTION'
    for i,row in enumerate(demand):
      content += '\n{} '.format(i+1)
      content += ' '.join(map(str, row))
    # Add the DEPOT_SECTION
    content += '\nDEPOT_SECTION\n{0}\n-1'.format(depot+1)
  # Write the file
  with open(filename, 'w') as f:
    f.write(content)
    f.write('\nEOF')
  # Return the full base name of the file
  path = os.path.dirname(filename)
  basename = os.path.join(path, problem_name)
  return basename
