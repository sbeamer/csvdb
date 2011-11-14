# Designed to read CSV files
# Scott Beamer (sbeamer@eecs.berkeley.edu)
# Fall 2011
# Pulled and modified from my Fall 2010 CS 281A project

from copy import deepcopy

class reader:
  def __init__(self):
    self.data = []


  def __len__(self):
    return len(self.data)


  def read_input(self, filename, delim=','):
    f = open(filename, 'r')
    lines = f.readlines()
    fields_full = lines[0].strip().split(delim)
    grab_name = lambda s: s[0:s.find('(')]
    grab_type = lambda s: s[s.find('(')+1:s.find(')')]
    fields = map(grab_name, fields_full)
    types = map(grab_type, fields_full)
    width = len(fields)
    for line in lines[1:]:
      split = line.strip().split(delim)
      if len(split) != width:
        print 'Error: line has wrong number of fields'
        print ' Expect(%u):' % width, fields
        print ' Got:(%u)' % len(split), split
        return None
      self.data += [dict(zip(fields,split))]
    make_floats = []
    make_ints = []
    for (field, type) in zip(fields, types):
      if type == 'f':
        make_floats += [field]
      elif type == 'i':
        make_ints += [field]      
    self.to_float(make_floats)
    self.to_int(make_ints)


  def get_field(self, field):
    if not isinstance(field,list):
      field = [field]
    grabbed = []
    def grabber(x):
      point = []
      for f in field:
        point += [x.get(f,None)]
      return point
    return map(grabber, self.data)


  def get_values(self, field):
    l = list(set(map(lambda x: x.get(field,None), self.data)))
    l.sort()
    return l


  def filter_points(self, criteria):
    if not isinstance(criteria,list):
      criteria = [criteria]
    def search(x):
      for c in criteria:
        if x[c[0]] != c[1]:
          return True
      return False
    copy = reader()
    copy.data = filter(search, self.data)
    return copy


  def grab_points(self, criteria):
    if not isinstance(criteria,list):
      criteria = [criteria]
    def search(x):
      for c in criteria:
        if x.get(c[0],None) != c[1]:
          return False
      return True
    copy = reader()
    copy.data = filter(search, self.data)
    return copy


  def to_float(self, fields):
    if not isinstance(fields,list):
      fields = [fields]
    for f in fields:
      def float_f(x): x[f] = float(x[f])
      map(float_f, self.data)


  def to_int(self, fields):
    if not isinstance(fields,list):
      fields = [fields]
    for f in fields:
      def int_f(x): x[f] = int(x[f])
      map(int_f, self.data)
  