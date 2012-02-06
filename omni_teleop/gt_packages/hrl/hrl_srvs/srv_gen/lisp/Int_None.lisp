; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude Int_None-request.msg.html

(cl:defclass <Int_None-request> (roslisp-msg-protocol:ros-message)
  ((a
    :reader a
    :initarg :a
    :type cl:fixnum
    :initform 0))
)

(cl:defclass Int_None-request (<Int_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Int_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Int_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Int_None-request> is deprecated: use hrl_srvs-srv:Int_None-request instead.")))

(cl:ensure-generic-function 'a-val :lambda-list '(m))
(cl:defmethod a-val ((m <Int_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:a-val is deprecated.  Use hrl_srvs-srv:a instead.")
  (a m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Int_None-request>) ostream)
  "Serializes a message object of type '<Int_None-request>"
  (cl:let* ((signed (cl:slot-value msg 'a)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Int_None-request>) istream)
  "Deserializes a message object of type '<Int_None-request>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'a) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Int_None-request>)))
  "Returns string type for a service object of type '<Int_None-request>"
  "hrl_srvs/Int_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_None-request)))
  "Returns string type for a service object of type 'Int_None-request"
  "hrl_srvs/Int_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Int_None-request>)))
  "Returns md5sum for a message object of type '<Int_None-request>"
  "4eec2979cc688371cc0e7f01aea37ad1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Int_None-request)))
  "Returns md5sum for a message object of type 'Int_None-request"
  "4eec2979cc688371cc0e7f01aea37ad1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Int_None-request>)))
  "Returns full string definition for message of type '<Int_None-request>"
  (cl:format cl:nil "int8 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Int_None-request)))
  "Returns full string definition for message of type 'Int_None-request"
  (cl:format cl:nil "int8 a~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Int_None-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Int_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Int_None-request
    (cl:cons ':a (a msg))
))
;//! \htmlinclude Int_None-response.msg.html

(cl:defclass <Int_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass Int_None-response (<Int_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Int_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Int_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Int_None-response> is deprecated: use hrl_srvs-srv:Int_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Int_None-response>) ostream)
  "Serializes a message object of type '<Int_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Int_None-response>) istream)
  "Deserializes a message object of type '<Int_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Int_None-response>)))
  "Returns string type for a service object of type '<Int_None-response>"
  "hrl_srvs/Int_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_None-response)))
  "Returns string type for a service object of type 'Int_None-response"
  "hrl_srvs/Int_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Int_None-response>)))
  "Returns md5sum for a message object of type '<Int_None-response>"
  "4eec2979cc688371cc0e7f01aea37ad1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Int_None-response)))
  "Returns md5sum for a message object of type 'Int_None-response"
  "4eec2979cc688371cc0e7f01aea37ad1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Int_None-response>)))
  "Returns full string definition for message of type '<Int_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Int_None-response)))
  "Returns full string definition for message of type 'Int_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Int_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Int_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Int_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Int_None)))
  'Int_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Int_None)))
  'Int_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Int_None)))
  "Returns string type for a service object of type '<Int_None>"
  "hrl_srvs/Int_None")
