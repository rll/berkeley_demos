; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude FloatArray_Float-request.msg.html

(cl:defclass <FloatArray_Float-request> (roslisp-msg-protocol:ros-message)
  ((val
    :reader val
    :initarg :val
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass FloatArray_Float-request (<FloatArray_Float-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatArray_Float-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatArray_Float-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatArray_Float-request> is deprecated: use hrl_srvs-srv:FloatArray_Float-request instead.")))

(cl:ensure-generic-function 'val-val :lambda-list '(m))
(cl:defmethod val-val ((m <FloatArray_Float-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:val-val is deprecated.  Use hrl_srvs-srv:val instead.")
  (val m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatArray_Float-request>) ostream)
  "Serializes a message object of type '<FloatArray_Float-request>"
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
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatArray_Float-request>) istream)
  "Deserializes a message object of type '<FloatArray_Float-request>"
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatArray_Float-request>)))
  "Returns string type for a service object of type '<FloatArray_Float-request>"
  "hrl_srvs/FloatArray_FloatRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_Float-request)))
  "Returns string type for a service object of type 'FloatArray_Float-request"
  "hrl_srvs/FloatArray_FloatRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatArray_Float-request>)))
  "Returns md5sum for a message object of type '<FloatArray_Float-request>"
  "dd682166edb796173ec88e7ce3d59245")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatArray_Float-request)))
  "Returns md5sum for a message object of type 'FloatArray_Float-request"
  "dd682166edb796173ec88e7ce3d59245")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatArray_Float-request>)))
  "Returns full string definition for message of type '<FloatArray_Float-request>"
  (cl:format cl:nil "float64[] val~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatArray_Float-request)))
  "Returns full string definition for message of type 'FloatArray_Float-request"
  (cl:format cl:nil "float64[] val~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatArray_Float-request>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'val) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatArray_Float-request>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatArray_Float-request
    (cl:cons ':val (val msg))
))
;//! \htmlinclude FloatArray_Float-response.msg.html

(cl:defclass <FloatArray_Float-response> (roslisp-msg-protocol:ros-message)
  ((val
    :reader val
    :initarg :val
    :type cl:float
    :initform 0.0))
)

(cl:defclass FloatArray_Float-response (<FloatArray_Float-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <FloatArray_Float-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'FloatArray_Float-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<FloatArray_Float-response> is deprecated: use hrl_srvs-srv:FloatArray_Float-response instead.")))

(cl:ensure-generic-function 'val-val :lambda-list '(m))
(cl:defmethod val-val ((m <FloatArray_Float-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:val-val is deprecated.  Use hrl_srvs-srv:val instead.")
  (val m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <FloatArray_Float-response>) ostream)
  "Serializes a message object of type '<FloatArray_Float-response>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'val))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <FloatArray_Float-response>) istream)
  "Deserializes a message object of type '<FloatArray_Float-response>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'val) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<FloatArray_Float-response>)))
  "Returns string type for a service object of type '<FloatArray_Float-response>"
  "hrl_srvs/FloatArray_FloatResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_Float-response)))
  "Returns string type for a service object of type 'FloatArray_Float-response"
  "hrl_srvs/FloatArray_FloatResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<FloatArray_Float-response>)))
  "Returns md5sum for a message object of type '<FloatArray_Float-response>"
  "dd682166edb796173ec88e7ce3d59245")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'FloatArray_Float-response)))
  "Returns md5sum for a message object of type 'FloatArray_Float-response"
  "dd682166edb796173ec88e7ce3d59245")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<FloatArray_Float-response>)))
  "Returns full string definition for message of type '<FloatArray_Float-response>"
  (cl:format cl:nil "float64 val~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'FloatArray_Float-response)))
  "Returns full string definition for message of type 'FloatArray_Float-response"
  (cl:format cl:nil "float64 val~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <FloatArray_Float-response>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <FloatArray_Float-response>))
  "Converts a ROS message object to a list"
  (cl:list 'FloatArray_Float-response
    (cl:cons ':val (val msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'FloatArray_Float)))
  'FloatArray_Float-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'FloatArray_Float)))
  'FloatArray_Float-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'FloatArray_Float)))
  "Returns string type for a service object of type '<FloatArray_Float>"
  "hrl_srvs/FloatArray_Float")
