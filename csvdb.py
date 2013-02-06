# Designed to read CSV files
# Scott Beamer (sbeamer@eecs.berkeley.edu)
# Fall 2011
# Pulled and modified from my Fall 2010 CS 281A project

from copy import deepcopy

class reader:
  def __init__(self):
    """Return a new blank reader"""
    self.data = []


  def __len__(self):
    """Return the number of points in the reader"""
    return len(self.data)


  def read_file(self, filename, delim=','):
    """Read in filename and append it to data"""
    f = open(filename, 'r')
    lines = f.readlines()
    self.read_input(lines,delim)


  def read_input(self, lines, delim=','):
    """Read in list of strings and append it to data"""
    fields_full = lines[0].strip().split(delim)
    grab_name = lambda s: s[0:s.find('(')] if ('(' in s) else s
    grab_type = lambda s: s[s.find('(')+1:s.find(')')] if ('(' in s) else 's'
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
    """Return a list of all values for field"""
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
    """Return a list of all the unique values for field"""
    l = list(set(map(lambda x: x.get(field,None), self.data)))
    l.sort()
    return l


  def filter_points(self, criteria):
    """Return a new reader whose points don't match criteria

    criteria is a tuple (or list of tuples) of (field,value)
    """
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
    """Return a new reader whose points match criteria

    criteria is a tuple (or list of tuples) of (field,value)
    """
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
    """Make all values of fields type float"""
    if not isinstance(fields,list):
      fields = [fields]
    for f in fields:
      def float_f(x): x[f] = float(x[f])
      map(float_f, self.data)


  def to_int(self, fields):
    """Make all values of fields type int"""
    if not isinstance(fields,list):
      fields = [fields]
    for f in fields:
      def int_f(x): x[f] = int(x[f])
      map(int_f, self.data)
  