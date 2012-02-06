; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude FloatArray_None-request.msg.html

(cl:defclass <FloatArray_None-request> (roslisp-msg-protocol:ros-message)
  ((val
    :reader val
    :initarg :val
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass FloatArray_None-request (<FloatArray_None-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatArray_None-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatArray_None-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatArray_None-request> is deprecated: use hrl_srvs-srv:FloatArray_None-request instead.")))

(cl:ensure-generic-function 'val-val :lambda-list '(m))
(cl:defmethod val-val ((m <FloatArray_None-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:val-val is deprecated.  Use hrl_srvs-srv:val instead.")
  (val m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatArray_None-request>) ostream)
  "Serializes a message object of type '<FloatArray_None-request>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'val))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'val))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatArray_None-request>) istream)
  "Deserializes a message object of type '<FloatArray_None-request>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'val) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'val)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatArray_None-request>)))
  "Returns string type for a service object of type '<FloatArray_None-request>"
  "hrl_srvs/FloatArray_NoneRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_None-request)))
  "Returns string type for a service object of type 'FloatArray_None-request"
  "hrl_srvs/FloatArray_NoneRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatArray_None-request>)))
  "Returns md5sum for a message object of type '<FloatArray_None-request>"
  "65ac3f59e35977c61c27adccf4c68288")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatArray_None-request)))
  "Returns md5sum for a message object of type 'FloatArray_None-request"
  "65ac3f59e35977c61c27adccf4c68288")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatArray_None-request>)))
  "Returns full string definition for message of type '<FloatArray_None-request>"
  (cl:format cl:nil "float64[] val~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatArray_None-request)))
  "Returns full string definition for message of type 'FloatArray_None-request"
  (cl:format cl:nil "float64[] val~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatArray_None-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'val) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatArray_None-request>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatArray_None-request
    (cl:cons ':val (val msg))
))
;//! \htmlinclude FloatArray_None-response.msg.html

(cl:defclass <FloatArray_None-response> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass FloatArray_None-response (<FloatArray_None-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatArray_None-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatArray_None-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatArray_None-response> is deprecated: use hrl_srvs-srv:FloatArray_None-response instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatArray_None-response>) ostream)
  "Serializes a message object of type '<FloatArray_None-response>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatArray_None-response>) istream)
  "Deserializes a message object of type '<FloatArray_None-response>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatArray_None-response>)))
  "Returns string type for a service object of type '<FloatArray_None-response>"
  "hrl_srvs/FloatArray_NoneResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_None-response)))
  "Returns string type for a service object of type 'FloatArray_None-response"
  "hrl_srvs/FloatArray_NoneResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatArray_None-response>)))
  "Returns md5sum for a message object of type '<FloatArray_None-response>"
  "65ac3f59e35977c61c27adccf4c68288")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatArray_None-response)))
  "Returns md5sum for a message object of type 'FloatArray_None-response"
  "65ac3f59e35977c61c27adccf4c68288")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatArray_None-response>)))
  "Returns full string definition for message of type '<FloatArray_None-response>"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatArray_None-response)))
  "Returns full string definition for message of type 'FloatArray_None-response"
  (cl:format cl:nil "~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatArray_None-response>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatArray_None-response>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatArray_None-response
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'FloatArray_None)))
  'FloatArray_None-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'FloatArray_None)))
  'FloatArray_None-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_None)))
  "Returns string type for a service object of type '<FloatArray_None>"
  "hrl_srvs/FloatArray_None")
