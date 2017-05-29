#!/usr/bin/env python3.4
# - coding: utf-8 -

import tafsmio
import numpy
import argparse
import sys

###########################

def p2n(plane,ien):
  node = numpy.array([])
  for i in range(0,len(plane[0])):
    if plane[1][i]==0:
      node=numpy.append(node,ien[plane[0][i]][0])
      node=numpy.append(node,ien[plane[0][i]][1])
      node=numpy.append(node,ien[plane[0][i]][2])
      node=numpy.append(node,ien[plane[0][i]][3])
    elif plane[1][i]==1:                      
      node=numpy.append(node,ien[plane[0][i]][0])
      node=numpy.append(node,ien[plane[0][i]][1])
      node=numpy.append(node,ien[plane[0][i]][5])
      node=numpy.append(node,ien[plane[0][i]][4])
    elif plane[1][i]==2:                      
      node=numpy.append(node,ien[plane[0][i]][6])
      node=numpy.append(node,ien[plane[0][i]][1])
      node=numpy.append(node,ien[plane[0][i]][2])
      node=numpy.append(node,ien[plane[0][i]][5])
    elif plane[1][i]==3:                      
      node=numpy.append(node,ien[plane[0][i]][6])
      node=numpy.append(node,ien[plane[0][i]][1])
      node=numpy.append(node,ien[plane[0][i]][2])
      node=numpy.append(node,ien[plane[0][i]][7])
    elif plane[1][i]==4:                      
      node=numpy.append(node,ien[plane[0][i]][0])
      node=numpy.append(node,ien[plane[0][i]][1])
      node=numpy.append(node,ien[plane[0][i]][2])
      node=numpy.append(node,ien[plane[0][i]][4])
    elif plane[1][i]==5:                      
      node=numpy.append(node,ien[plane[0][i]][4])
      node=numpy.append(node,ien[plane[0][i]][5])
      node=numpy.append(node,ien[plane[0][i]][6])
      node=numpy.append(node,ien[plane[0][i]][7])
  node = numpy.unique(node)
  return  node

################################

def output(node,name):
    node_o = numpy.array(node,'>i4')
    node_o.tofile(open(name,'wb'))


###########################
def main():
  parser = argparse.ArgumentParser(description="""
  Desctiption
  """
  )
  parser.add_argument("config",metavar="config files",help="mesh config files")
  parser.add_argument("rng",metavar="rng number",nargs=2,type=int,help="rng number")
  parser.add_argument("output",metavar="output file Name",help="ouput file name")


  options = parser.parse_args()
  #input = args[0]
  #input  = "mesh.cfg"
  #base_factory = tafsmio.ParserFactory(input)
 # print (options.config)
  #print (input)
  base_factory = tafsmio.ParserFactory(options.config)
  base_parser = base_factory.build()
  base_config = base_parser.parse()
 
  base_nen = base_config.get("nen")
  base_rng = base_config.getData("rng",int).reshape(-1,6)
  base_ien = base_config.getData("ien",int).reshape(-1,base_nen)  
 
  ien = numpy.array(base_ien)
  mrng = numpy.array(base_rng)
  
  plane1 = numpy.where(mrng==options.rng[0])
  plane2 = numpy.where(mrng==options.rng[1])
  print(plane1)
  node1 = p2n(plane1,ien)
  node2 = p2n(plane2,ien)

  dup_node = list(set(node1) & set(node2))
  dup_node= numpy.sort(dup_node)
  output(dup_node,options.output)

if __name__ == "__main__":
  try:
    sys.exit(main())
  except IOError:
    exit(1)
