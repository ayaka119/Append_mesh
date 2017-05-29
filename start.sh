#!/bin/sh

set -x
./adhere.py VALVE/MESH.FEM/mesh.cfg PATCH_AORTA_new/MESH.FEM/mesh.cfg -p 1390644 1391316 1392309 318163 318187 294388
mv xyz_new PATCH_AORTA_new/MESH.FEM
cd PATCH_AORTA_new/MESH.FEM/
gen_xdmf.py mesh_r.cfg -o rotated.xmf
paraview rotated.xmf &
cd ../..

