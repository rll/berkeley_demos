FILE(REMOVE_RECURSE
  "../srv_gen"
  "../src/hrl_srvs/srv"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_gensrv_py"
  "../src/hrl_srvs/srv/__init__.py"
  "../src/hrl_srvs/srv/_Bool_None.py"
  "../src/hrl_srvs/srv/_Float_Int.py"
  "../src/hrl_srvs/srv/_FloatFloat_Int.py"
  "../src/hrl_srvs/srv/_Int_None.py"
  "../src/hrl_srvs/srv/_None_Float.py"
  "../src/hrl_srvs/srv/_None_FloatArray.py"
  "../src/hrl_srvs/srv/_FloatFloat_None.py"
  "../src/hrl_srvs/srv/_Int_Int.py"
  "../src/hrl_srvs/srv/_Float_None.py"
  "../src/hrl_srvs/srv/_String_None.py"
  "../src/hrl_srvs/srv/_None_Bool.py"
  "../src/hrl_srvs/srv/_FloatArray_None.py"
  "../src/hrl_srvs/srv/_FloatArray_Float.py"
  "../src/hrl_srvs/srv/_None_Int32.py"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_py.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
