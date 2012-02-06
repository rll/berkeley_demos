FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/phantom_omni/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_lisp"
  "../msg_gen/lisp/OmniFeedback.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_OmniFeedback.lisp"
  "../msg_gen/lisp/PhantomButtonEvent.lisp"
  "../msg_gen/lisp/_package.lisp"
  "../msg_gen/lisp/_package_PhantomButtonEvent.lisp"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_lisp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
