; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude FloatFloat_None-request.msg.html

(cl:defclass <FloatFloat_None-request> (roslisp-msg-protocol:ros-message)
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

(cl:defclass FloatFloat_None-request (<FloatFloat_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatFloat_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatFloat_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatFloat_None-request> is deprecated: use hrl_srvs-srv:FloatFloat_None-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <FloatFloat_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:a-val is deprecated.  Use hrl_srvs-srv:a instead.")
  (a m))

(cl:ensure-generic-function 'b-val :lambda-list '(m))
(cl:defmethod b-val ((m <FloatFloat_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:b-val is deprecated.  Use hrl_srvs-srv:b instead.")
  (b m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatFloat_None-request>) ostream)
  "Serializes a message object of type '<FloatFloat_None-request>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatFloat_None-request>) istream)
  "Deserializes a message object of type '<FloatFloat_None-request>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatFloat_None-request>)))
  "Returns string type for a service object of type '<FloatFloat_None-request>"
  "hrl_srvs/FloatFloat_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_None-request)))
  "Returns string type for a service object of type 'FloatFloat_None-request"
  "hrl_srvs/FloatFloat_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatFloat_None-request>)))
  "Returns md5sum for a message object of type '<FloatFloat_None-request>"
  "6f4f9f1b571de73ae8592a1438fd23f3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatFloat_None-request)))
  "Returns md5sum for a message object of type 'FloatFloat_None-request"
  "6f4f9f1b571de73ae8592a1438fd23f3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatFloat_None-request>)))
  "Returns full string definition for message of type '<FloatFloat_None-request>"
  (cl:format cl:nil "float64 a~%float64 b~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatFloat_None-request)))
  "Returns full string definition for message of type 'FloatFloat_None-request"
  (cl:format cl:nil "float64 a~%float64 b~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatFloat_None-request>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatFloat_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatFloat_None-request
    (cl:cons ':a (a msg))
    (cl:cons ':b (b msg))
))
;//! \htmlinclude FloatFloat_None-response.msg.html

(cl:defclass <FloatFloat_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass FloatFloat_None-response (<FloatFloat_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatFloat_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatFloat_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatFloat_None-response> is deprecated: use hrl_srvs-srv:FloatFloat_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatFloat_None-response>) ostream)
  "Serializes a message object of type '<FloatFloat_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatFloat_None-response>) istream)
  "Deserializes a message object of type '<FloatFloat_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatFloat_None-response>)))
  "Returns string type for a service object of type '<FloatFloat_None-response>"
  "hrl_srvs/FloatFloat_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_None-response)))
  "Returns string type for a service object of type 'FloatFloat_None-response"
  "hrl_srvs/FloatFloat_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatFloat_None-response>)))
  "Returns md5sum for a message object of type '<FloatFloat_None-response>"
  "6f4f9f1b571de73ae8592a1438fd23f3")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatFloat_None-response)))
  "Returns md5sum for a message object of type 'FloatFloat_None-response"
  "6f4f9f1b571de73ae8592a1438fd23f3")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatFloat_None-response>)))
  "Returns full string definition for message of type '<FloatFloat_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatFloat_None-response)))
  "Returns full string definition for message of type 'FloatFloat_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatFloat_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatFloat_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatFloat_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'FloatFloat_None)))
  'FloatFloat_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'FloatFloat_None)))
  'FloatFloat_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatFloat_None)))
  "Returns string type for a service object of type '<FloatFloat_None>"
  "hrl_srvs/FloatFloat_None")
