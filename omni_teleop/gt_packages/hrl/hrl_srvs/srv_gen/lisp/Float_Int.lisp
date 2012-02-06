; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude Float_Int-request.msg.html

(cl:defclass <Float_Int-request> (roslisp-msg-protocol:ros-message)
  ((value
    :reader value
    :initarg :value
    :type cl:float
    :initform 0.0))
)

(cl:defclass Float_Int-request (<Float_Int-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Float_Int-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Float_Int-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Float_Int-request> is deprecated: use hrl_srvs-srv:Float_Int-request instead.")))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <Float_Int-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:value-val is deprecated.  Use hrl_srvs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Float_Int-request>) ostream)
  "Serializes a message object of type '<Float_Int-request>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Float_Int-request>) istream)
  "Deserializes a message object of type '<Float_Int-request>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Float_Int-request>)))
  "Returns string type for a service object of type '<Float_Int-request>"
  "hrl_srvs/Float_IntRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_Int-request)))
  "Returns string type for a service object of type 'Float_Int-request"
  "hrl_srvs/Float_IntRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Float_Int-request>)))
  "Returns md5sum for a message object of type '<Float_Int-request>"
  "9f744029c1815d8e33a503bee0560de0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Float_Int-request)))
  "Returns md5sum for a message object of type 'Float_Int-request"
  "9f744029c1815d8e33a503bee0560de0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Float_Int-request>)))
  "Returns full string definition for message of type '<Float_Int-request>"
  (cl:format cl:nil "float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Float_Int-request)))
  "Returns full string definition for message of type 'Float_Int-request"
  (cl:format cl:nil "float64 value~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Float_Int-request>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Float_Int-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Float_Int-request
    (cl:cons ':value (value msg))
))
;//! \htmlinclude Float_Int-response.msg.html

(cl:defclass <Float_Int-response> (roslisp-msg-protocol:ros-message)
  ((retval
    :reader retval
    :initarg :retval
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Float_Int-response (<Float_Int-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Float_Int-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Float_Int-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Float_Int-response> is deprecated: use hrl_srvs-srv:Float_Int-response instead.")))

(cl:ensure-generic-function 'retval-val :lambda-list '(m))
(cl:defmethod retval-val ((m <Float_Int-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:retval-val is deprecated.  Use hrl_srvs-srv:retval instead.")
  (retval m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Float_Int-response>) ostream)
  "Serializes a message object of type '<Float_Int-response>"
  (cl:let* ((signed (cl:slot-value msg 'retval)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Float_Int-response>) istream)
  "Deserializes a message object of type '<Float_Int-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'retval) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Float_Int-response>)))
  "Returns string type for a service object of type '<Float_Int-response>"
  "hrl_srvs/Float_IntResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_Int-response)))
  "Returns string type for a service object of type 'Float_Int-response"
  "hrl_srvs/Float_IntResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Float_Int-response>)))
  "Returns md5sum for a message object of type '<Float_Int-response>"
  "9f744029c1815d8e33a503bee0560de0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Float_Int-response)))
  "Returns md5sum for a message object of type 'Float_Int-response"
  "9f744029c1815d8e33a503bee0560de0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Float_Int-response>)))
  "Returns full string definition for message of type '<Float_Int-response>"
  (cl:format cl:nil "int8 retval~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Float_Int-response)))
  "Returns full string definition for message of type 'Float_Int-response"
  (cl:format cl:nil "int8 retval~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Float_Int-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Float_Int-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Float_Int-response
    (cl:cons ':retval (retval msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Float_Int)))
  'Float_Int-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Float_Int)))
  'Float_Int-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Float_Int)))
  "Returns string type for a service object of type '<Float_Int>"
  "hrl_srvs/Float_Int")
