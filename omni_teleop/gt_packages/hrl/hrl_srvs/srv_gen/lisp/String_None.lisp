; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude String_None-request.msg.html

(cl:defclass <String_None-request> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:string
    :initform ""))
)

(cl:defclass String_None-request (<String_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <String_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'String_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<String_None-request> is deprecated: use hrl_srvs-srv:String_None-request instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <String_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:data-val is deprecated.  Use hrl_srvs-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <String_None-request>) ostream)
  "Serializes a message object of type '<String_None-request>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'data))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'data))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <String_None-request>) istream)
  "Deserializes a message object of type '<String_None-request>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'data) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'data) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<String_None-request>)))
  "Returns string type for a service object of type '<String_None-request>"
  "hrl_srvs/String_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'String_None-request)))
  "Returns string type for a service object of type 'String_None-request"
  "hrl_srvs/String_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<String_None-request>)))
  "Returns md5sum for a message object of type '<String_None-request>"
  "992ce8a1687cec8c8bd883ec73ca41d1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'String_None-request)))
  "Returns md5sum for a message object of type 'String_None-request"
  "992ce8a1687cec8c8bd883ec73ca41d1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<String_None-request>)))
  "Returns full string definition for message of type '<String_None-request>"
  (cl:format cl:nil "string data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'String_None-request)))
  "Returns full string definition for message of type 'String_None-request"
  (cl:format cl:nil "string data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <String_None-request>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'data))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <String_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'String_None-request
    (cl:cons ':data (data msg))
))
;//! \htmlinclude String_None-response.msg.html

(cl:defclass <String_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass String_None-response (<String_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <String_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'String_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<String_None-response> is deprecated: use hrl_srvs-srv:String_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <String_None-response>) ostream)
  "Serializes a message object of type '<String_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <String_None-response>) istream)
  "Deserializes a message object of type '<String_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<String_None-response>)))
  "Returns string type for a service object of type '<String_None-response>"
  "hrl_srvs/String_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'String_None-response)))
  "Returns string type for a service object of type 'String_None-response"
  "hrl_srvs/String_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<String_None-response>)))
  "Returns md5sum for a message object of type '<String_None-response>"
  "992ce8a1687cec8c8bd883ec73ca41d1")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'String_None-response)))
  "Returns md5sum for a message object of type 'String_None-response"
  "992ce8a1687cec8c8bd883ec73ca41d1")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<String_None-response>)))
  "Returns full string definition for message of type '<String_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'String_None-response)))
  "Returns full string definition for message of type 'String_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <String_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <String_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'String_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'String_None)))
  'String_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'String_None)))
  'String_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'String_None)))
  "Returns string type for a service object of type '<String_None>"
  "hrl_srvs/String_None")
