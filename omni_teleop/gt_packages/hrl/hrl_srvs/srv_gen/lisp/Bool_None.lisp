; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude Bool_None-request.msg.html

(cl:defclass <Bool_None-request> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass Bool_None-request (<Bool_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Bool_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Bool_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Bool_None-request> is deprecated: use hrl_srvs-srv:Bool_None-request instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <Bool_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:data-val is deprecated.  Use hrl_srvs-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Bool_None-request>) ostream)
  "Serializes a message object of type '<Bool_None-request>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'data) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Bool_None-request>) istream)
  "Deserializes a message object of type '<Bool_None-request>"
    (cl:setf (cl:slot-value msg 'data) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Bool_None-request>)))
  "Returns string type for a service object of type '<Bool_None-request>"
  "hrl_srvs/Bool_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Bool_None-request)))
  "Returns string type for a service object of type 'Bool_None-request"
  "hrl_srvs/Bool_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Bool_None-request>)))
  "Returns md5sum for a message object of type '<Bool_None-request>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Bool_None-request)))
  "Returns md5sum for a message object of type 'Bool_None-request"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Bool_None-request>)))
  "Returns full string definition for message of type '<Bool_None-request>"
  (cl:format cl:nil "bool data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Bool_None-request)))
  "Returns full string definition for message of type 'Bool_None-request"
  (cl:format cl:nil "bool data~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Bool_None-request>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Bool_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Bool_None-request
    (cl:cons ':data (data msg))
))
;//! \htmlinclude Bool_None-response.msg.html

(cl:defclass <Bool_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass Bool_None-response (<Bool_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Bool_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Bool_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<Bool_None-response> is deprecated: use hrl_srvs-srv:Bool_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Bool_None-response>) ostream)
  "Serializes a message object of type '<Bool_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Bool_None-response>) istream)
  "Deserializes a message object of type '<Bool_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Bool_None-response>)))
  "Returns string type for a service object of type '<Bool_None-response>"
  "hrl_srvs/Bool_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Bool_None-response)))
  "Returns string type for a service object of type 'Bool_None-response"
  "hrl_srvs/Bool_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Bool_None-response>)))
  "Returns md5sum for a message object of type '<Bool_None-response>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Bool_None-response)))
  "Returns md5sum for a message object of type 'Bool_None-response"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Bool_None-response>)))
  "Returns full string definition for message of type '<Bool_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Bool_None-response)))
  "Returns full string definition for message of type 'Bool_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Bool_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Bool_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Bool_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Bool_None)))
  'Bool_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Bool_None)))
  'Bool_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Bool_None)))
  "Returns string type for a service object of type '<Bool_None>"
  "hrl_srvs/Bool_None")
