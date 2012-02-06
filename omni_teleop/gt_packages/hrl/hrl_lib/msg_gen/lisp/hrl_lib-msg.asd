
(cl:in-package :asdf)

(defsystem "hrl_lib-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :geometry_msgs-msg
               :std_msgs-msg
)
  :components ((:file "_package")
    (:file "StringArray" :depends-on ("_package_StringArray"))
    (:file "_package_StringArray" :depends-on ("_package"))
    (:file "NumpyArray" :depends-on ("_package_NumpyArray"))
    (:file "_package_NumpyArray" :depends-on ("_package"))
    (:file "PlanarBaseVel" :depends-on ("_package_PlanarBaseVel"))
    (:file "_package_PlanarBaseVel" :depends-on ("_package"))
    (:file "PlanarBaseVelLimits" :depends-on ("_package_PlanarBaseVelLimits"))
    (:file "_package_PlanarBaseVelLimits" :depends-on ("_package"))
    (:file "WrenchPoseArrayStamped" :depends-on ("_package_WrenchPoseArrayStamped"))
    (:file "_package_WrenchPoseArrayStamped" :depends-on ("_package"))
    (:file "Pose3DOF" :depends-on ("_package_Pose3DOF"))
    (:file "_package_Pose3DOF" :depends-on ("_package"))
    (:file "String" :depends-on ("_package_String"))
    (:file "_package_String" :depends-on ("_package"))
    (:file "VO_Data" :depends-on ("_package_VO_Data"))
    (:file "_package_VO_Data" :depends-on ("_package"))
  ))