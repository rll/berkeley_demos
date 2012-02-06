FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/hrl_msgs/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_lisp"
  "../msg_gen/lisp/StringArray.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_StringArray.lisp"
  "../msg_gen/lisp/FloatArray.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_FloatArray.lisp"
  "../msg_gen/lisp/FloatArrayBare.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_FloatArrayBare.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
