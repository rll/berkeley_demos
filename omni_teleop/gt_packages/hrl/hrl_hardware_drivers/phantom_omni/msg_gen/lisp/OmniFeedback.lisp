; Auto-generated. Do not edit!


(cl:in-package phantom_omni-msg)


;//! \htmlinclude OmniFeedback.msg.html

(cl:defclass <OmniFeedback> (roslisp-msg-protocol:ros-message)
  ((force
    :reader force
    :initarg :force
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3))
   (position
    :reader position
    :initarg :position
    :type geometry_msgs-msg:Vector3
    :initform (cl:make-instance 'geometry_msgs-msg:Vector3)))
)

(cl:defclass OmniFeedback (<OmniFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <OmniFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'OmniFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name phantom_omni-msg:<OmniFeedback> is deprecated: use phantom_omni-msg:OmniFeedback instead.")))

(cl:ensure-generic-function 'force-val :lambda-list '(m))
(cl:defmethod force-val ((m <OmniFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader phantom_omni-msg:force-val is deprecated.  Use phantom_omni-msg:force instead.")
  (force m))

(cl:ensure-generic-function 'position-val :lambda-list '(m))
(cl:defmethod position-val ((m <OmniFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader phantom_omni-msg:position-val is deprecated.  Use phantom_omni-msg:position instead.")
  (position m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <OmniFeedback>) ostream)
  "Serializes a message object of type '<OmniFeedback>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'force) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <OmniFeedback>) istream)
  "Deserializes a message object of type '<OmniFeedback>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'force) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<OmniFeedback>)))
  "Returns string type for a message object of type '<OmniFeedback>"
  "phantom_omni/OmniFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'OmniFeedback)))
  "Returns string type for a message object of type 'OmniFeedback"
  "phantom_omni/OmniFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<OmniFeedback>)))
  "Returns md5sum for a message object of type '<OmniFeedback>"
  "e9083ac4fd95494e94fbb0c0f90b6c00")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'OmniFeedback)))
  "Returns md5sum for a message object of type 'OmniFeedback"
  "e9083ac4fd95494e94fbb0c0f90b6c00")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<OmniFeedback>)))
  "Returns full string definition for message of type '<OmniFeedback>"
  (cl:format cl:nil "# This is the force as estimated from the applied torques as well as the current~%# end effector position of the robot arm                           ~%geometry_msgs/Vector3  force                                                                  ~%geometry_msgs/Vector3  position  ~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'OmniFeedback)))
  "Returns full string definition for message of type 'OmniFeedback"
  (cl:format cl:nil "# This is the force as estimated from the applied torques as well as the current~%# end effector position of the robot arm                           ~%geometry_msgs/Vector3  force                                                                  ~%geometry_msgs/Vector3  position  ~%================================================================================~%MSG: geometry_msgs/Vector3~%# This represents a vector in free space. ~%~%float64 x~%float64 y~%float64 z~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <OmniFeedback>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'force))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <OmniFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'OmniFeedback
    (cl:cons ':force (force msg))
    (cl:cons ':position (position msg))
))
