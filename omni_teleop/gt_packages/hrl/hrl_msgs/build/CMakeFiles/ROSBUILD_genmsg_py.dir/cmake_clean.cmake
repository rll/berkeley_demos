FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/hrl_msgs/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/hrl_msgs/msg/__init__.py"
  "../src/hrl_msgs/msg/_StringArray.py"
  "../src/hrl_msgs/msg/_FloatArray.py"
  "../src/hrl_msgs/msg/_FloatArrayBare.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
