; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude None_Float-request.msg.html

(cl:defclass <None_Float-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass None_Float-request (<None_Float-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Float-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Float-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Float-request> is deprecated: use hrl_srvs-srv:None_Float-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Float-request>) ostream)
  "Serializes a message object of type '<None_Float-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Float-request>) istream)
  "Deserializes a message object of type '<None_Float-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Float-request>)))
  "Returns string type for a service object of type '<None_Float-request>"
  "hrl_srvs/None_FloatRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Float-request)))
  "Returns string type for a service object of type 'None_Float-request"
  "hrl_srvs/None_FloatRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Float-request>)))
  "Returns md5sum for a message object of type '<None_Float-request>"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Float-request)))
  "Returns md5sum for a message object of type 'None_Float-request"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Float-request>)))
  "Returns full string definition for message of type '<None_Float-request>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Float-request)))
  "Returns full string definition for message of type 'None_Float-request"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Float-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Float-request>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Float-request
))
;//! \htmlinclude None_Float-response.msg.html

(cl:defclass <None_Float-response> (roslisp-msg-protocol:ros-message)
  ((value
    :reader value
    :initarg :value
    :type cl:float
    :initform 0.0))
)

(cl:defclass None_Float-response (<None_Float-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Float-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Float-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Float-response> is deprecated: use hrl_srvs-srv:None_Float-response instead.")))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <None_Float-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:value-val is deprecated.  Use hrl_srvs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Float-response>) ostream)
  "Serializes a message object of type '<None_Float-response>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Float-response>) istream)
  "Deserializes a message object of type '<None_Float-response>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Float-response>)))
  "Returns string type for a service object of type '<None_Float-response>"
  "hrl_srvs/None_FloatResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Float-response)))
  "Returns string type for a service object of type 'None_Float-response"
  "hrl_srvs/None_FloatResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Float-response>)))
  "Returns md5sum for a message object of type '<None_Float-response>"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Float-response)))
  "Returns md5sum for a message object of type 'None_Float-response"
  "1b1594d2b74931ef8fe7be8e2d594455")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Float-response>)))
  "Returns full string definition for message of type '<None_Float-response>"
  (cl:format cl:nil "float64 value~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Float-response)))
  "Returns full string definition for message of type 'None_Float-response"
  (cl:format cl:nil "float64 value~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Float-response>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Float-response>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Float-response
    (cl:cons ':value (value msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'None_Float)))
  'None_Float-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'None_Float)))
  'None_Float-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Float)))
  "Returns string type for a service object of type '<None_Float>"
  "hrl_srvs/None_Float")
