大動脈と弁のメッシュをくっつけるプログラムです。
実行するには
```
sh start_imp.sh
```
___
start_imp.shの中身を見ると、find_dupli_point_in_rng.pyとadhere_imp.pyを実行しています。　　
<br />
<br />
find_dupli_point_in_rng.pyは二つのrngの被っている点のIDを出すものです。
コマンドは、
```
./find_dupli_point_in_rng.py VALVE/MESH.FEM/mesh.cfg 10 11 node_id_valve
```
pyファイル、cfgファイル、rng番号二つ、output名の順です。
<br />
<br />

adhere_imp.pyはメッシュを回転させ、移動し、くっつけます。
コマンドは、
```
./adhere_imp.py VALVE/MESH.FEM/mesh.cfg PATCH_AORTA_new/MESH.FEM/mesh.cfg node_id_valve node_id_aorta
```
pyファイル、cfgファイル*2、find_dupli_point_in_rng.pyで生成されたnode idファイル二つを読み込みます。


____
旧バージョンはstart.sh, プログラムはadhere.py
adhere.pyは二つのメッシュファイルのcfgを指定し、-pの後ろは、弁、大動脈の接合する面の縁上の3点(ID)をそれぞれとってください。