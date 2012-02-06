FILE(REMOVE_RECURSE
  "../srv_gen"
  "../src/hrl_srvs/srv"
  "../srv_gen"
  "CMakeFiles/ROSBUILD_gensrv_cpp"
  "../srv_gen/cpp/include/hrl_srvs/Bool_None.h"
  "../srv_gen/cpp/include/hrl_srvs/Float_Int.h"
  "../srv_gen/cpp/include/hrl_srvs/FloatFloat_Int.h"
  "../srv_gen/cpp/include/hrl_srvs/Int_None.h"
  "../srv_gen/cpp/include/hrl_srvs/None_Float.h"
  "../srv_gen/cpp/include/hrl_srvs/None_FloatArray.h"
  "../srv_gen/cpp/include/hrl_srvs/FloatFloat_None.h"
  "../srv_gen/cpp/include/hrl_srvs/Int_Int.h"
  "../srv_gen/cpp/include/hrl_srvs/Float_None.h"
  "../srv_gen/cpp/include/hrl_srvs/String_None.h"
  "../srv_gen/cpp/include/hrl_srvs/None_Bool.h"
  "../srv_gen/cpp/include/hrl_srvs/FloatArray_None.h"
  "../srv_gen/cpp/include/hrl_srvs/FloatArray_Float.h"
  "../srv_gen/cpp/include/hrl_srvs/None_Int32.h"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/ROSBUILD_gensrv_cpp.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
