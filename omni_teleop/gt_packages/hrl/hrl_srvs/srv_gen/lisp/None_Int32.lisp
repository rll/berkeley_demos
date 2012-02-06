; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude None_Int32-request.msg.html

(cl:defclass <None_Int32-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass None_Int32-request (<None_Int32-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Int32-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Int32-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Int32-request> is deprecated: use hrl_srvs-srv:None_Int32-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Int32-request>) ostream)
  "Serializes a message object of type '<None_Int32-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Int32-request>) istream)
  "Deserializes a message object of type '<None_Int32-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Int32-request>)))
  "Returns string type for a service object of type '<None_Int32-request>"
  "hrl_srvs/None_Int32Request")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Int32-request)))
  "Returns string type for a service object of type 'None_Int32-request"
  "hrl_srvs/None_Int32Request")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Int32-request>)))
  "Returns md5sum for a message object of type '<None_Int32-request>"
  "b3087778e93fcd34cc8d65bc54e850d1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Int32-request)))
  "Returns md5sum for a message object of type 'None_Int32-request"
  "b3087778e93fcd34cc8d65bc54e850d1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Int32-request>)))
  "Returns full string definition for message of type '<None_Int32-request>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Int32-request)))
  "Returns full string definition for message of type 'None_Int32-request"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Int32-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Int32-request>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Int32-request
))
;//! \htmlinclude None_Int32-response.msg.html

(cl:defclass <None_Int32-response> (roslisp-msg-protocol:ros-message)
  ((value
    :reader value
    :initarg :value
    :type cl:integer
    :initform 0))
)

(cl:defclass None_Int32-response (<None_Int32-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Int32-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Int32-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Int32-response> is deprecated: use hrl_srvs-srv:None_Int32-response instead.")))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <None_Int32-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:value-val is deprecated.  Use hrl_srvs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Int32-response>) ostream)
  "Serializes a message object of type '<None_Int32-response>"
  (cl:let* ((signed (cl:slot-value msg 'value)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Int32-response>) istream)
  "Deserializes a message object of type '<None_Int32-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'value) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Int32-response>)))
  "Returns string type for a service object of type '<None_Int32-response>"
  "hrl_srvs/None_Int32Response")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Int32-response)))
  "Returns string type for a service object of type 'None_Int32-response"
  "hrl_srvs/None_Int32Response")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Int32-response>)))
  "Returns md5sum for a message object of type '<None_Int32-response>"
  "b3087778e93fcd34cc8d65bc54e850d1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Int32-response)))
  "Returns md5sum for a message object of type 'None_Int32-response"
  "b3087778e93fcd34cc8d65bc54e850d1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Int32-response>)))
  "Returns full string definition for message of type '<None_Int32-response>"
  (cl:format cl:nil "int32 value~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Int32-response)))
  "Returns full string definition for message of type 'None_Int32-response"
  (cl:format cl:nil "int32 value~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Int32-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Int32-response>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Int32-response
    (cl:cons ':value (value msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'None_Int32)))
  'None_Int32-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'None_Int32)))
  'None_Int32-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Int32)))
  "Returns string type for a service object of type '<None_Int32>"
  "hrl_srvs/None_Int32")
