FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/hrl_lib/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/hrl_lib/msg/__init__.py"
  "../src/hrl_lib/msg/_StringArray.py"
  "../src/hrl_lib/msg/_NumpyArray.py"
  "../src/hrl_lib/msg/_PlanarBaseVel.py"
  "../src/hrl_lib/msg/_PlanarBaseVelLimits.py"
  "../src/hrl_lib/msg/_WrenchPoseArrayStamped.py"
  "../src/hrl_lib/msg/_Pose3DOF.py"
  "../src/hrl_lib/msg/_String.py"
  "../src/hrl_lib/msg/_VO_Data.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
