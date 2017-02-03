#!/usr/bin/python

import sys
import math
import time

class Queue(object):
  def __init__(self, value=None):
    self.lifetimeSize = 0
    if value is None:
        self.value = []
    else:
        self.value = list(value)
  def remove(self):
    return self.value.pop(0)
  def add(self, element):
    self.lifetimeSize+=1
    self.value.append(element)

class Stack(object):
  def __init__(self, value=None):
    self.lifetimeSize = 0
    if value is None:
        self.value = []
    else:
        self.value = list(value)
  def remove(self):
    return self.value.pop()
  def add(self, element):
    self.lifetimeSize+=1
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

  while not frontier.value == []:
    node = frontier.remove()
    explored.append(node.state)
    
    if goalTest(node.state):
      create_write_file(
        node, explored, expanded, frontier.lifetimeSize, max_search_depth, "%s" % (time.time() - startTime))
      return 'success'

    game = Game(node.state)
    expanded += 1
    for neighbor in game.neighbors()[::order]:
      if neighbor._state not in explored and neighbor._state not in frontier.value:
        children = node.expand(neighbor._state, neighbor._action)
        max_search_depth = children.depth if children.depth>=max_search_depth else max_search_depth
        frontier.add(children)
  print 'failure'

def search_ast(initialState):
  print 'Search ast not implemented yet'

def search_ida(initialState):
  print 'Search ida not implemented yet'

def create_write_file(node, explored, expanded, lifetimeSize, max_search_depth, time):
  x, result = node, []
  while x.parent:
    result.append(x.move)
    x = x.parent
  print 'path_to_goal: ', result[::-1]
  print 'cost_of_path: ', len(result)
  print 'nodes_expanded:', expanded
  print 'fringe_size:', len(explored)
  print 'max_fringe_size: ', lifetimeSize
  print 'search_depth: ', node.depth
  print 'max_search_depth: ', max_search_depth
  print 'running_time: ', format(float(time), '.8f')
  print 'max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by the ru_maxrss attribute in the resource module, reported in megabytes'
  # f = open('output.txt','w')
  # f.write(str(node))
  # f.close()

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
