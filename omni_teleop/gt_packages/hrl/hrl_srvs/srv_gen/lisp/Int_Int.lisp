; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude Int_Int-request.msg.html

(cl:defclass <Int_Int-request> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Int_Int-request (<Int_Int-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Int_Int-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Int_Int-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Int_Int-request> is deprecated: use hrl_srvs-srv:Int_Int-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <Int_Int-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:a-val is deprecated.  Use hrl_srvs-srv:a instead.")
  (a m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Int_Int-request>) ostream)
  "Serializes a message object of type '<Int_Int-request>"
  (cl:let* ((signed (cl:slot-value msg 'a)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Int_Int-request>) istream)
  "Deserializes a message object of type '<Int_Int-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'a) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Int_Int-request>)))
  "Returns string type for a service object of type '<Int_Int-request>"
  "hrl_srvs/Int_IntRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_Int-request)))
  "Returns string type for a service object of type 'Int_Int-request"
  "hrl_srvs/Int_IntRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Int_Int-request>)))
  "Returns md5sum for a message object of type '<Int_Int-request>"
  "e4f49179affdfe2550700dff2405e153")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Int_Int-request)))
  "Returns md5sum for a message object of type 'Int_Int-request"
  "e4f49179affdfe2550700dff2405e153")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Int_Int-request>)))
  "Returns full string definition for message of type '<Int_Int-request>"
  (cl:format cl:nil "int8 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Int_Int-request)))
  "Returns full string definition for message of type 'Int_Int-request"
  (cl:format cl:nil "int8 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Int_Int-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Int_Int-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Int_Int-request
    (cl:cons ':a (a msg))
))
;//! \htmlinclude Int_Int-response.msg.html

(cl:defclass <Int_Int-response> (roslisp-msg-protocol:ros-message)
  ((r
    :reader r
    :initarg :r
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Int_Int-response (<Int_Int-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Int_Int-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Int_Int-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Int_Int-response> is deprecated: use hrl_srvs-srv:Int_Int-response instead.")))

(cl:ensure-generic-function 'r-val :lambda-list '(m))
(cl:defmethod r-val ((m <Int_Int-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:r-val is deprecated.  Use hrl_srvs-srv:r instead.")
  (r m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Int_Int-response>) ostream)
  "Serializes a message object of type '<Int_Int-response>"
  (cl:let* ((signed (cl:slot-value msg 'r)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Int_Int-response>) istream)
  "Deserializes a message object of type '<Int_Int-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'r) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Int_Int-response>)))
  "Returns string type for a service object of type '<Int_Int-response>"
  "hrl_srvs/Int_IntResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_Int-response)))
  "Returns string type for a service object of type 'Int_Int-response"
  "hrl_srvs/Int_IntResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Int_Int-response>)))
  "Returns md5sum for a message object of type '<Int_Int-response>"
  "e4f49179affdfe2550700dff2405e153")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Int_Int-response)))
  "Returns md5sum for a message object of type 'Int_Int-response"
  "e4f49179affdfe2550700dff2405e153")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Int_Int-response>)))
  "Returns full string definition for message of type '<Int_Int-response>"
  (cl:format cl:nil "int8 r~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Int_Int-response)))
  "Returns full string definition for message of type 'Int_Int-response"
  (cl:format cl:nil "int8 r~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Int_Int-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Int_Int-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Int_Int-response
    (cl:cons ':r (r msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Int_Int)))
  'Int_Int-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Int_Int)))
  'Int_Int-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_Int)))
  "Returns string type for a service object of type '<Int_Int>"
  "hrl_srvs/Int_Int")
