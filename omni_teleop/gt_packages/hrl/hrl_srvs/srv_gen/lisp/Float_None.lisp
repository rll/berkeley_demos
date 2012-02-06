; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude Float_None-request.msg.html

(cl:defclass <Float_None-request> (roslisp-msg-protocol:ros-message)
  ((value
    :reader value
    :initarg :value
    :type cl:float
    :initform 0.0))
)

(cl:defclass Float_None-request (<Float_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Float_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Float_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Float_None-request> is deprecated: use hrl_srvs-srv:Float_None-request instead.")))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <Float_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:value-val is deprecated.  Use hrl_srvs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Float_None-request>) ostream)
  "Serializes a message object of type '<Float_None-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'value))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Float_None-request>) istream)
  "Deserializes a message object of type '<Float_None-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'value) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Float_None-request>)))
  "Returns string type for a service object of type '<Float_None-request>"
  "hrl_srvs/Float_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_None-request)))
  "Returns string type for a service object of type 'Float_None-request"
  "hrl_srvs/Float_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Float_None-request>)))
  "Returns md5sum for a message object of type '<Float_None-request>"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Float_None-request)))
  "Returns md5sum for a message object of type 'Float_None-request"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Float_None-request>)))
  "Returns full string definition for message of type '<Float_None-request>"
  (cl:format cl:nil "float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Float_None-request)))
  "Returns full string definition for message of type 'Float_None-request"
  (cl:format cl:nil "float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Float_None-request>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Float_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Float_None-request
    (cl:cons ':value (value msg))
))
;//! \htmlinclude Float_None-response.msg.html

(cl:defclass <Float_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass Float_None-response (<Float_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Float_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Float_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Float_None-response> is deprecated: use hrl_srvs-srv:Float_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Float_None-response>) ostream)
  "Serializes a message object of type '<Float_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Float_None-response>) istream)
  "Deserializes a message object of type '<Float_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Float_None-response>)))
  "Returns string type for a service object of type '<Float_None-response>"
  "hrl_srvs/Float_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_None-response)))
  "Returns string type for a service object of type 'Float_None-response"
  "hrl_srvs/Float_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Float_None-response>)))
  "Returns md5sum for a message object of type '<Float_None-response>"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Float_None-response)))
  "Returns md5sum for a message object of type 'Float_None-response"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Float_None-response>)))
  "Returns full string definition for message of type '<Float_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Float_None-response)))
  "Returns full string definition for message of type 'Float_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Float_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Float_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Float_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Float_None)))
  'Float_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Float_None)))
  'Float_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_None)))
  "Returns string type for a service object of type '<Float_None>"
  "hrl_srvs/Float_None")
