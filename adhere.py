#!/usr/bin/env python3.4
# - coding: utf-8 -

import tafsmio
import numpy
import argparse
import sys
import math

##################################

def base_vector(p1,p2,p3):
    p12 = p2-p1 
    p13 = p3-p1
    e = numpy.zeros((3,3),dtype=numpy.float)
    e_norm = numpy.zeros((3,3),dtype=numpy.float)
    
    e[0] = numpy.cross(p12,p13)  #normal vector
    e[1] = p12
    e[2] = numpy.cross(e[0],e[1])
    print(e[0]) 
    e_norm[2]=e[0]/numpy.linalg.norm(e[0])
    e_norm[0]=e[1]/numpy.linalg.norm(e[1])
    e_norm[1]=e[2]/numpy.linalg.norm(e[2])   
    e_norm= e_norm 
  #  e_new =e / (numpy.linalg.norm(e))
   # e[0].tofile(open('e1','wb'))
   # e[1].tofile(open('e2','wb'))
   # e[2].tofile(open('e3','wb'))
   # print(e[1],e[0],e[2])
   # print(e_new)
   # print(numpy.linalg.norm(e_new))
   # numpy.append(p1,p2)
   # numpy.append(p1,p3)
  #  p1.tofile(open('xyz','wb'))
    return e_norm

##################################

def rotation(e1,e_c,xyz_c):
    R = numpy.dot(e1.transpose(),numpy.linalg.inv(e_c.transpose()))
    print(R)
    xyz_new = numpy.dot(R.transpose(),xyz_c.transpose())
    xyz_new2 = xyz_new.transpose()
    return xyz_new2  

##################################

def center(p1,p2,p3):
    a=p2[0]-p1[0]
    b=p2[1]-p1[1]
    c=p3[0]-p1[0]
    d=p3[1]-p1[1]
    A=numpy.array([[2*a,2*b],[2*c,2*d]])
    B=numpy.array([p2[0]*p2[0]+p2[1]*p2[1]-p1[0]*p1[0]-p1[1]*p1[1],p3[0]*p3[0]+p3[1]*p3[1]-p1[0]*p1[0]-p1[1]*p1[1]])
    C=numpy.dot(numpy.linalg.inv(A),B)
    D=numpy.append(C,p1[2])
    return D


#################################    

    
def magnify(xyz_1,xyz,vc,pc,pv,pp):
    rp=math.sqrt((xyz_1[pp][0]-pc[0])*(xyz_1[pp][0]-pc[0])+(xyz_1[pp][1]-pc[1])*(xyz_1[pp][1]-pc[1]))
    rv=math.sqrt((xyz[pv][0]-vc[0])*(xyz[pv][0]-vc[0])+(xyz[pv][1]-vc[1])*(xyz[pv][1]-vc[1]))
 
    num=rv/rp
    return num

#################################

def move(xyz_2,vc,pc):
  #diff =numpy.zeros(3,dtype=numpy.float)
  diff = vc-pc
  #print(diff)
  for i in range(0,int(xyz_2.size/3)):
     xyz_2[i]=xyz_2[i]+diff
  return xyz_2


################################

def output(xyz):
  xyz1 = numpy.array(xyz,'>f8')
  xyz1.tofile(open('xyz_new','wb'))

################################

def main():
  parser = argparse.ArgumentParser(description="""
  Desctiption
  """
  )
  parser.add_argument("config",metavar="config files",nargs=2,help="mesh config files")
  #parser.add_argument("points",metavar="points",nargs=3,type="int",help="3 points' ID")
  parser.add_argument("-p","--points",nargs=6,type=int,help="3 points'ID of each mesh")

  options = parser.parse_args()
  base_factory = tafsmio.ParserFactory(options.config[0])
  base_parser = base_factory.build()
  base_config = base_parser.parse()
  
  change_factory = tafsmio.ParserFactory(options.config[1])
  change_parser = change_factory.build()
  change_config = change_parser.parse()

  base_nsd = base_config.get("nsd")
  base_xyz = base_config.getData("xyz",float).reshape(-1,base_nsd)
  change_nsd = change_config.get("nsd")
  change_xyz = change_config.getData("xyz",float).reshape(-1,change_nsd)

  xyz = numpy.array(base_xyz)
  xyz_c = numpy.array(change_xyz)

  e1 = base_vector(xyz[options.points[0]],xyz[options.points[1]],xyz[options.points[2]])
  e_c = base_vector(xyz_c[options.points[3]],xyz_c[options.points[4]],xyz_c[options.points[5]])

  xyz_1=rotation(e_c,e1,xyz_c)
  xyznn = numpy.array(xyz_1,'>f8')
  xyznn.tofile(open('xyz_rota','wb'))

 
  vc = center(xyz[options.points[0]],xyz[options.points[1]],xyz[options.points[2]])
  pc = center(xyz_1[options.points[3]],xyz_1[options.points[4]],xyz_1[options.points[5]])
  #print(vc,xyz[2343707]) 
  #print(pc,xyz_1[[266637]])
  num=magnify(xyz_1,xyz,vc,pc,options.points[0],options.points[3])
  xyz_2=num*xyz_1
  pc1=num*pc
  xyz_3=move(xyz_2,vc,pc1)
  output(xyz_3)

if __name__ == "__main__":
  try:
    sys.exit(main())
  except IOError:
    exit(1)
