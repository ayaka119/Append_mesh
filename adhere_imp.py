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

def center(x,y):
  sumx= sum(x)
  sumy= sum(y)
  sumx2=sum([ix ** 2 for ix in x])
  sumy2=sum([iy ** 2 for iy in y])
  sumxy=sum([ix * iy for (ix,iy) in zip(x,y)])

  F=numpy.array([[sumx2,sumxy,sumx],
                 [sumxy,sumy2,sumy],
                 [sumx,sumy,len(x)]])

  #G=numpy.array([[-sum([ix ** 3 + ix*iy ** 2 for (ix,iy) in zip(x,y)])]
  #               [-sum([ix ** 2 *iy + iy ** 3 for (ix,iy) in zip(x,y)])]
  #               [-sum([ix ** 2 + iy ** 2 for (ix,iy) in zip(x,y)])]])

  g1=[-sum([ix ** 3 + ix*iy ** 2 for (ix,iy) in zip(x,y)])]
  g2=[-sum([ix ** 2 *iy + iy ** 3 for (ix,iy) in zip(x,y)])]
  g3=[-sum([ix ** 2 + iy ** 2 for (ix,iy) in zip(x,y)])]
  G=numpy.array([g1,g2,g3])
           
  T=numpy.linalg.inv(F).dot(G)
  return T

#################################    

    
def magnify(xyz_1,xyz,vc,pc,pv,pp):
    rp=math.sqrt((xyz_1[pp][0]-pc[0])*(xyz_1[pp][0]-pc[0])+(xyz_1[pp][1]-pc[1])*(xyz_1[pp][1]-pc[1]))
    rv=math.sqrt((xyz[pv][0]-vc[0])*(xyz[pv][0]-vc[0])+(xyz[pv][1]-vc[1])*(xyz[pv][1]-vc[1]))
 
    num=rv/rp
    return num

#################################

def move(xyz_2,vc,pc):
    diff = vc-pc
    for i in range(0,int(xyz_2.size/3)):
       xyz_2[i]=xyz_2[i]+diff
    return xyz_2


################################

def output(xyz):
    xyz1 = numpy.array(xyz,'>f8')
    xyz1.tofile(open('xyz_new','wb'))

################################
def putinarray(node_id,xyz):
  node_x=numpy.array([])
  node_y=numpy.array([])
  for element in node_id:
    node_x=numpy.append(node_x,xyz[element][0])
    node_y=numpy.append(node_y,xyz[element][1])

  return [node_x, node_y]

###############################

def main():
  parser = argparse.ArgumentParser(description="""
  Desctiption
  """
  )
  parser.add_argument("config",metavar="config files",nargs=2,help="mesh config files")
  parser.add_argument("node",metavar="node files",nargs=2,help="node files")

 
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


  node_id_v=numpy.fromfile(options.node[0],dtype=">i4")
  node_id_p=numpy.fromfile(options.node[1],dtype=">i4")

  e1 = base_vector(xyz[node_id_v[1]],xyz[node_id_v[2]],xyz[node_id_v[3]])
  e_c = base_vector(xyz_c[node_id_p[1]],xyz_c[node_id_p[2]],xyz_c[node_id_p[3]])
  xyz_1=rotation(e_c,e1,xyz_c)
  
  
  (node_x_v,node_y_v)=putinarray(node_id_v,xyz)
  (node_x_p,node_y_p)=putinarray(node_id_p,xyz_1)
 

  vc = center(node_x_v,node_y_v)
  vc=numpy.insert(vc,2,xyz[node_id_v[1]][2])
  pc = center(node_x_p,node_y_p)
  pc=numpy.insert(pc,2,xyz_1[node_id_p[1]][2])
  print(vc,xyz[2343707]) 
  print(pc,xyz_1[266637])
  num=vc[3]/pc[3]
  xyz_2=num*xyz_1
  pc1=num*pc[0:3]
  vc=vc[0:3]
  xyz_3=move(xyz_2,vc,pc1)
  output(xyz_3)

if __name__ == "__main__":
  try:
    sys.exit(main())
  except IOError:
    exit(1)
