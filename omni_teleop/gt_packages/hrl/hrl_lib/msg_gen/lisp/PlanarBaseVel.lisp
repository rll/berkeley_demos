; Auto-generated. Do not edit!


(cl:in-package hrl_lib-msg)


;//! \htmlinclude PlanarBaseVel.msg.html

(cl:defclass <PlanarBaseVel> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (xvel
    :reader xvel
    :initarg :xvel
    :type cl:float
    :initform 0.0)
   (yvel
    :reader yvel
    :initarg :yvel
    :type cl:float
    :initform 0.0)
   (angular_velocity
    :reader angular_velocity
    :initarg :angular_velocity
    :type cl:float
    :initform 0.0))
)

(cl:defclass PlanarBaseVel (<PlanarBaseVel>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PlanarBaseVel>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PlanarBaseVel)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_lib-msg:<PlanarBaseVel> is deprecated: use hrl_lib-msg:PlanarBaseVel instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <PlanarBaseVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:header-val is deprecated.  Use hrl_lib-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'xvel-val :lambda-list '(m))
(cl:defmethod xvel-val ((m <PlanarBaseVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:xvel-val is deprecated.  Use hrl_lib-msg:xvel instead.")
  (xvel m))

(cl:ensure-generic-function 'yvel-val :lambda-list '(m))
(cl:defmethod yvel-val ((m <PlanarBaseVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:yvel-val is deprecated.  Use hrl_lib-msg:yvel instead.")
  (yvel m))

(cl:ensure-generic-function 'angular_velocity-val :lambda-list '(m))
(cl:defmethod angular_velocity-val ((m <PlanarBaseVel>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:angular_velocity-val is deprecated.  Use hrl_lib-msg:angular_velocity instead.")
  (angular_velocity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PlanarBaseVel>) ostream)
  "Serializes a message object of type '<PlanarBaseVel>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xvel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yvel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angular_velocity))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PlanarBaseVel>) istream)
  "Deserializes a message object of type '<PlanarBaseVel>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xvel) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yvel) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angular_velocity) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PlanarBaseVel>)))
  "Returns string type for a message object of type '<PlanarBaseVel>"
  "hrl_lib/PlanarBaseVel")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PlanarBaseVel)))
  "Returns string type for a message object of type 'PlanarBaseVel"
  "hrl_lib/PlanarBaseVel")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PlanarBaseVel>)))
  "Returns md5sum for a message object of type '<PlanarBaseVel>"
  "c844e0872ecf385742618d1ca7390275")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PlanarBaseVel)))
  "Returns md5sum for a message object of type 'PlanarBaseVel"
  "c844e0872ecf385742618d1ca7390275")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PlanarBaseVel>)))
  "Returns full string definition for message of type '<PlanarBaseVel>"
  (cl:format cl:nil "Header header~%float64 xvel~%float64 yvel~%float64 angular_velocity~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PlanarBaseVel)))
  "Returns full string definition for message of type 'PlanarBaseVel"
  (cl:format cl:nil "Header header~%float64 xvel~%float64 yvel~%float64 angular_velocity~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PlanarBaseVel>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PlanarBaseVel>))
  "Converts a ROS message object to a list"
  (cl:list 'PlanarBaseVel
    (cl:cons ':header (header msg))
    (cl:cons ':xvel (xvel msg))
    (cl:cons ':yvel (yvel msg))
    (cl:cons ':angular_velocity (angular_velocity msg))
))
