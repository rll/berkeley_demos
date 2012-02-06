FILE(REMOVE_RECURSE
  "../msg_gen"
  "../src/phantom_omni/msg"
  "../msg_gen"
  "CMakeFiles/ROSBUILD_genmsg_py"
  "../src/phantom_omni/msg/__init__.py"
  "../src/phantom_omni/msg/_OmniFeedback.py"
  "../src/phantom_omni/msg/_PhantomButtonEvent.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_genmsg_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
