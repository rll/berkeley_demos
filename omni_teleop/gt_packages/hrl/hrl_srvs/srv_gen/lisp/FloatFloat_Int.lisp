; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude FloatFloat_Int-request.msg.html

(cl:defclass <FloatFloat_Int-request> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:float
    :initform 0.0)
   (b
    :reader b
    :initarg :b
    :type cl:float
    :initform 0.0))
)

(cl:defclass FloatFloat_Int-request (<FloatFloat_Int-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatFloat_Int-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatFloat_Int-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatFloat_Int-request> is deprecated: use hrl_srvs-srv:FloatFloat_Int-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <FloatFloat_Int-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:a-val is deprecated.  Use hrl_srvs-srv:a instead.")
  (a m))

(cl:ensure-generic-function 'b-val :lambda-list '(m))
(cl:defmethod b-val ((m <FloatFloat_Int-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:b-val is deprecated.  Use hrl_srvs-srv:b instead.")
  (b m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatFloat_Int-request>) ostream)
  "Serializes a message object of type '<FloatFloat_Int-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'a))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'b))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatFloat_Int-request>) istream)
  "Deserializes a message object of type '<FloatFloat_Int-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'a) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'b) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatFloat_Int-request>)))
  "Returns string type for a service object of type '<FloatFloat_Int-request>"
  "hrl_srvs/FloatFloat_IntRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_Int-request)))
  "Returns string type for a service object of type 'FloatFloat_Int-request"
  "hrl_srvs/FloatFloat_IntRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatFloat_Int-request>)))
  "Returns md5sum for a message object of type '<FloatFloat_Int-request>"
  "d4639a349ca232ce2f49ae772369b637")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatFloat_Int-request)))
  "Returns md5sum for a message object of type 'FloatFloat_Int-request"
  "d4639a349ca232ce2f49ae772369b637")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatFloat_Int-request>)))
  "Returns full string definition for message of type '<FloatFloat_Int-request>"
  (cl:format cl:nil "float64 a~%float64 b~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatFloat_Int-request)))
  "Returns full string definition for message of type 'FloatFloat_Int-request"
  (cl:format cl:nil "float64 a~%float64 b~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatFloat_Int-request>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatFloat_Int-request>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatFloat_Int-request
    (cl:cons ':a (a msg))
    (cl:cons ':b (b msg))
))
;//! \htmlinclude FloatFloat_Int-response.msg.html

(cl:defclass <FloatFloat_Int-response> (roslisp-msg-protocol:ros-message)
  ((r
    :reader r
    :initarg :r
    :type cl:fixnum
    :initform 0))
)

(cl:defclass FloatFloat_Int-response (<FloatFloat_Int-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatFloat_Int-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatFloat_Int-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatFloat_Int-response> is deprecated: use hrl_srvs-srv:FloatFloat_Int-response instead.")))

(cl:ensure-generic-function 'r-val :lambda-list '(m))
(cl:defmethod r-val ((m <FloatFloat_Int-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:r-val is deprecated.  Use hrl_srvs-srv:r instead.")
  (r m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatFloat_Int-response>) ostream)
  "Serializes a message object of type '<FloatFloat_Int-response>"
  (cl:let* ((signed (cl:slot-value msg 'r)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatFloat_Int-response>) istream)
  "Deserializes a message object of type '<FloatFloat_Int-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'r) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatFloat_Int-response>)))
  "Returns string type for a service object of type '<FloatFloat_Int-response>"
  "hrl_srvs/FloatFloat_IntResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_Int-response)))
  "Returns string type for a service object of type 'FloatFloat_Int-response"
  "hrl_srvs/FloatFloat_IntResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatFloat_Int-response>)))
  "Returns md5sum for a message object of type '<FloatFloat_Int-response>"
  "d4639a349ca232ce2f49ae772369b637")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatFloat_Int-response)))
  "Returns md5sum for a message object of type 'FloatFloat_Int-response"
  "d4639a349ca232ce2f49ae772369b637")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatFloat_Int-response>)))
  "Returns full string definition for message of type '<FloatFloat_Int-response>"
  (cl:format cl:nil "int8 r~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatFloat_Int-response)))
  "Returns full string definition for message of type 'FloatFloat_Int-response"
  (cl:format cl:nil "int8 r~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatFloat_Int-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatFloat_Int-response>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatFloat_Int-response
    (cl:cons ':r (r msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'FloatFloat_Int)))
  'FloatFloat_Int-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'FloatFloat_Int)))
  'FloatFloat_Int-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_Int)))
  "Returns string type for a service object of type '<FloatFloat_Int>"
  "hrl_srvs/FloatFloat_Int")
