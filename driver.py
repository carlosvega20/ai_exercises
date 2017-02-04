import sys
import math
import time
import resource

class Queue(object):
  def __init__(self, value=None):
    if value is None:
        self.value = []
    else:
        self.value = list(value)
  def __len__(self):
    return len(self.value)
  def remove(self):
    return self.value.pop(0)
  def add(self, element):
    self.value.append(element)

class Stack(object):
  def __init__(self, value=None):
    if value is None:
        self.value = []
    else:
        self.value = list(value)
  def __len__(self):
    return len(self.value)
  def remove(self):
    return self.value.pop()
  def add(self, element):
    self.value.append(element)

#move elements
class Game:
  def __init__(self, state=None, action=''):
    self._state = [] if state is None else list(state)
    self._size = math.sqrt( len(self._state) )
    self._action = action
  def find_location(self):
    for i in self._state:
      if i is '0':
        index = self._state.index(i)
        y = int(math.floor(index/self._size))
        x = int(index-(y*self._size))
        return {'y': y, 'x': x}
  def move_up(self):
    init = self.find_location()
    end = {
      'y': init.get('y')-1 if init.get('y') != 0 else 0,
      'x': init.get('x')}
    return self.create_new_board(init, end, 'Up')
  def move_down(self):
    init = self.find_location()
    end = {
      'y': init.get('y')+1 if init.get('y')<self._size-1 else init.get('y'),
      'x': init.get('x')}
    return self.create_new_board(init, end, 'Down')
  def move_left(self):
    init = self.find_location()
    end = {
      'y': init.get('y'),
      'x': init.get('x')-1 if init.get('x') != 0 else 0}
    return self.create_new_board(init, end, 'Left')
  def move_right(self):
    init = self.find_location()
    end = {
      'y': init.get('y'),
      'x': init.get('x')+1 if init.get('x')<self._size-1 else init.get('x')}
    return self.create_new_board(init, end, 'Right')
  def create_new_board(self, init, end, action):
    nextState = []
    for k in self._state:
      index = self._state.index(k)
      y = int(math.floor(index/self._size))
      x = int(index-(y*self._size))
      if y is init.get('y') and x is init.get('x'):
        nextState.append(self._state[int(end.get('y')*self._size+end.get('x'))])
      elif y is end.get('y') and x is end.get('x'):
        nextState.append(self._state[int(init.get('y')*self._size+init.get('x'))])
      else:
        nextState.append(k)
    return Game(nextState, action)
  def neighbors(self):
    seq = (self.move_up(), self.move_down(), self.move_left(), self.move_right())
    seen = []
    return [x for x in seq if x._state not in seen and not seen.append(x._state)]

def goalTest(state):
  return state == [str(x) for x in range(len(state))]

class Node:
  def __init__(self, state, parent=None, move=''):
    self.state = state
    self.parent = parent
    self.move = move
    if parent:
      self.depth = parent.depth + 1
    else:
      self.depth = 0
  def __repr__(self):
        return "<Node %s>" % (self.state)
  def expand(self, newState, move=''):
    return Node(newState, self, move)

def graph_search(initialState, fringe, order=1):
  frontier = fringe([Node(initialState)])
  explored = []
  expanded = 0
  max_search_depth = 0
  startTime = time.time()
  max_fringe_size = 0

  while not frontier.value == []:
    node = frontier.remove()
    explored.append(node.state)
    
    if goalTest(node.state):
      create_write_file(
        node, explored, expanded, frontier, max_fringe_size, max_search_depth, "%s" % (time.time() - startTime))
      return 'success'

    game = Game(node.state)
    expanded += 1
    for neighbor in game.neighbors()[::order]:
      if neighbor._state not in explored and neighbor._state not in frontier.value:
        children = node.expand(neighbor._state, neighbor._action)
        max_search_depth = children.depth if children.depth>=max_search_depth else max_search_depth
        frontier.add(children)
        max_fringe_size = len(frontier) if len(frontier)>=max_fringe_size else max_fringe_size
  print 'failure'

def search_ast(initialState):
  print 'Search ast not implemented yet'

def search_ida(initialState):
  print 'Search ida not implemented yet'

def create_write_file(node, explored, expanded, frontier, max_fringe_size, max_search_depth, time):
  x, result = node, []
  while x.parent:
    result.append(x.move)
    x = x.parent

  path_to_goal = result[::-1]
  cost_of_path = len(result)
  nodes_expanded = expanded
  fringe_size = len(frontier)
  search_depth = node.depth
  running_time = format(float(time), '.8f')
  max_ram_usage = format(float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)/10000, '.8f')
  
  f = open('output.txt','w')
  f.write('path_to_goal: {} \ncost_of_path: {}\n'\
  'nodes_expanded: {}\nfringe_size: {}\n'\
  'max_fringe_size: {}\nsearch_depth: {}\n'\
  'max_search_depth: {}\nrunning_time: {}\n'\
  'max_ram_usage: {}\n'.format(
    path_to_goal,
    cost_of_path,
    nodes_expanded,
    fringe_size,
    max_fringe_size,
    search_depth,
    max_search_depth,
    running_time,
    max_ram_usage))
  f.close()

def bind(func, *args, **kwargs):
    return lambda: func(*args, **kwargs)

#Search Methods
# bfs (Breadth-First Search)
# dfs (Depth-First Search)
# ast (A-Star Search)
# ida (IDA-Star Search)
def search_method(method, initialState):
  return {
    'bfs': bind(graph_search, initialState, Queue),
    'dfs': bind(graph_search, initialState, Stack, -1),
    'ast': bind(search_ast, initialState),
    'ida': bind(search_ida, initialState)
  }.get(method)

search_method(sys.argv[1], sys.argv[2].split(','))()
