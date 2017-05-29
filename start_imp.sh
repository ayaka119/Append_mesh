#! /bin/sh
#
# start_imp.sh
# Copyright (C) 2016 ayoshi <ayoshi@kw0-44>
#
# Distributed under terms of the MIT license.
#

set -x
./find_dupli_point_in_rng.py VALVE/MESH.FEM/mesh.cfg 10 11 node_id_valve
./find_dupli_point_in_rng.py PATCH_AORTA_new/MESH.FEM/mesh.cfg 1 6 node_id_aorta
./adhere_imp.py Valve/MESH.FEM/mesh.cfg PATCH_AORTA_new/MESH.FEM/mesh.cfg node_id_valve node_id_aorta
#rm node_id_valve node_id_aorta
mv xyz_new PATCH_AORTA_new/MESH.FEM
cd PATCH_AORTA_new/MESH.FEM
gen_xdmf.py mesh_r.cfg -o rotated.xmf
paraview rotated.xmf &
cd ../..
