FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/hrl_lib/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_cpp"
  "../msg_gen/cpp/include/hrl_lib/StringArray.h"
  "../msg_gen/cpp/include/hrl_lib/NumpyArray.h"
  "../msg_gen/cpp/include/hrl_lib/PlanarBaseVel.h"
  "../msg_gen/cpp/include/hrl_lib/PlanarBaseVelLimits.h"
  "../msg_gen/cpp/include/hrl_lib/WrenchPoseArrayStamped.h"
  "../msg_gen/cpp/include/hrl_lib/Pose3DOF.h"
  "../msg_gen/cpp/include/hrl_lib/String.h"
  "../msg_gen/cpp/include/hrl_lib/VO_Data.h"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_cpp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
