; Auto-generated. Do not edit!


(cl:in-package hrl_lib-msg)


;//! \htmlinclude PlanarBaseVelLimits.msg.html

(cl:defclass <PlanarBaseVelLimits> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (xvel_pos_max
    :reader xvel_pos_max
    :initarg :xvel_pos_max
    :type cl:float
    :initform 0.0)
   (xvel_neg_max
    :reader xvel_neg_max
    :initarg :xvel_neg_max
    :type cl:float
    :initform 0.0)
   (yvel_pos_max
    :reader yvel_pos_max
    :initarg :yvel_pos_max
    :type cl:float
    :initform 0.0)
   (yvel_neg_max
    :reader yvel_neg_max
    :initarg :yvel_neg_max
    :type cl:float
    :initform 0.0)
   (avel_max
    :reader avel_max
    :initarg :avel_max
    :type cl:float
    :initform 0.0))
)

(cl:defclass PlanarBaseVelLimits (<PlanarBaseVelLimits>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <PlanarBaseVelLimits>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'PlanarBaseVelLimits)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_lib-msg:<PlanarBaseVelLimits> is deprecated: use hrl_lib-msg:PlanarBaseVelLimits instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:header-val is deprecated.  Use hrl_lib-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'xvel_pos_max-val :lambda-list '(m))
(cl:defmethod xvel_pos_max-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:xvel_pos_max-val is deprecated.  Use hrl_lib-msg:xvel_pos_max instead.")
  (xvel_pos_max m))

(cl:ensure-generic-function 'xvel_neg_max-val :lambda-list '(m))
(cl:defmethod xvel_neg_max-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:xvel_neg_max-val is deprecated.  Use hrl_lib-msg:xvel_neg_max instead.")
  (xvel_neg_max m))

(cl:ensure-generic-function 'yvel_pos_max-val :lambda-list '(m))
(cl:defmethod yvel_pos_max-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:yvel_pos_max-val is deprecated.  Use hrl_lib-msg:yvel_pos_max instead.")
  (yvel_pos_max m))

(cl:ensure-generic-function 'yvel_neg_max-val :lambda-list '(m))
(cl:defmethod yvel_neg_max-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:yvel_neg_max-val is deprecated.  Use hrl_lib-msg:yvel_neg_max instead.")
  (yvel_neg_max m))

(cl:ensure-generic-function 'avel_max-val :lambda-list '(m))
(cl:defmethod avel_max-val ((m <PlanarBaseVelLimits>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_lib-msg:avel_max-val is deprecated.  Use hrl_lib-msg:avel_max instead.")
  (avel_max m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <PlanarBaseVelLimits>) ostream)
  "Serializes a message object of type '<PlanarBaseVelLimits>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xvel_pos_max))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'xvel_neg_max))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yvel_pos_max))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'yvel_neg_max))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'avel_max))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <PlanarBaseVelLimits>) istream)
  "Deserializes a message object of type '<PlanarBaseVelLimits>"
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
    (cl:setf (cl:slot-value msg 'xvel_pos_max) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'xvel_neg_max) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yvel_pos_max) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yvel_neg_max) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'avel_max) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<PlanarBaseVelLimits>)))
  "Returns string type for a message object of type '<PlanarBaseVelLimits>"
  "hrl_lib/PlanarBaseVelLimits")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'PlanarBaseVelLimits)))
  "Returns string type for a message object of type 'PlanarBaseVelLimits"
  "hrl_lib/PlanarBaseVelLimits")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<PlanarBaseVelLimits>)))
  "Returns md5sum for a message object of type '<PlanarBaseVelLimits>"
  "79d6a8bc99f5988deabb3198a791ba92")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'PlanarBaseVelLimits)))
  "Returns md5sum for a message object of type 'PlanarBaseVelLimits"
  "79d6a8bc99f5988deabb3198a791ba92")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<PlanarBaseVelLimits>)))
  "Returns full string definition for message of type '<PlanarBaseVelLimits>"
  (cl:format cl:nil "# max allowable velocities in positive and negative X and Y directions~%# and max allowable angular velocity.~%Header header~%float64 xvel_pos_max~%float64 xvel_neg_max~%float64 yvel_pos_max~%float64 yvel_neg_max~%float64 avel_max~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'PlanarBaseVelLimits)))
  "Returns full string definition for message of type 'PlanarBaseVelLimits"
  (cl:format cl:nil "# max allowable velocities in positive and negative X and Y directions~%# and max allowable angular velocity.~%Header header~%float64 xvel_pos_max~%float64 xvel_neg_max~%float64 yvel_pos_max~%float64 yvel_neg_max~%float64 avel_max~%~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.secs: seconds (stamp_secs) since epoch~%# * stamp.nsecs: nanoseconds since stamp_secs~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <PlanarBaseVelLimits>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     8
     8
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <PlanarBaseVelLimits>))
  "Converts a ROS message object to a list"
  (cl:list 'PlanarBaseVelLimits
    (cl:cons ':header (header msg))
    (cl:cons ':xvel_pos_max (xvel_pos_max msg))
    (cl:cons ':xvel_neg_max (xvel_neg_max msg))
    (cl:cons ':yvel_pos_max (yvel_pos_max msg))
    (cl:cons ':yvel_neg_max (yvel_neg_max msg))
    (cl:cons ':avel_max (avel_max msg))
))
