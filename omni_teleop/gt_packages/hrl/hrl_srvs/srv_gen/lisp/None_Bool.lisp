; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude None_Bool-request.msg.html

(cl:defclass <None_Bool-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass None_Bool-request (<None_Bool-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Bool-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Bool-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Bool-request> is deprecated: use hrl_srvs-srv:None_Bool-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Bool-request>) ostream)
  "Serializes a message object of type '<None_Bool-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Bool-request>) istream)
  "Deserializes a message object of type '<None_Bool-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Bool-request>)))
  "Returns string type for a service object of type '<None_Bool-request>"
  "hrl_srvs/None_BoolRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Bool-request)))
  "Returns string type for a service object of type 'None_Bool-request"
  "hrl_srvs/None_BoolRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Bool-request>)))
  "Returns md5sum for a message object of type '<None_Bool-request>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Bool-request)))
  "Returns md5sum for a message object of type 'None_Bool-request"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Bool-request>)))
  "Returns full string definition for message of type '<None_Bool-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Bool-request)))
  "Returns full string definition for message of type 'None_Bool-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Bool-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Bool-request>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Bool-request
))
;//! \htmlinclude None_Bool-response.msg.html

(cl:defclass <None_Bool-response> (roslisp-msg-protocol:ros-message)
  ((data
    :reader data
    :initarg :data
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass None_Bool-response (<None_Bool-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_Bool-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_Bool-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_Bool-response> is deprecated: use hrl_srvs-srv:None_Bool-response instead.")))

(cl:ensure-generic-function 'data-val :lambda-list '(m))
(cl:defmethod data-val ((m <None_Bool-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:data-val is deprecated.  Use hrl_srvs-srv:data instead.")
  (data m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_Bool-response>) ostream)
  "Serializes a message object of type '<None_Bool-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'data) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_Bool-response>) istream)
  "Deserializes a message object of type '<None_Bool-response>"
    (cl:setf (cl:slot-value msg 'data) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_Bool-response>)))
  "Returns string type for a service object of type '<None_Bool-response>"
  "hrl_srvs/None_BoolResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Bool-response)))
  "Returns string type for a service object of type 'None_Bool-response"
  "hrl_srvs/None_BoolResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_Bool-response>)))
  "Returns md5sum for a message object of type '<None_Bool-response>"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_Bool-response)))
  "Returns md5sum for a message object of type 'None_Bool-response"
  "8b94c1b53db61fb6aed406028ad6332a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_Bool-response>)))
  "Returns full string definition for message of type '<None_Bool-response>"
  (cl:format cl:nil "bool data~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_Bool-response)))
  "Returns full string definition for message of type 'None_Bool-response"
  (cl:format cl:nil "bool data~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_Bool-response>))
  (cl:+ 0
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_Bool-response>))
  "Converts a ROS message object to a list"
  (cl:list 'None_Bool-response
    (cl:cons ':data (data msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'None_Bool)))
  'None_Bool-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'None_Bool)))
  'None_Bool-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_Bool)))
  "Returns string type for a service object of type '<None_Bool>"
  "hrl_srvs/None_Bool")
