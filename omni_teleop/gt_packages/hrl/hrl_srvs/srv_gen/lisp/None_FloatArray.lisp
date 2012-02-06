; Auto-generated. Do not edit!


(cl:in-package hrl_srvs-srv)


;//! \htmlinclude None_FloatArray-request.msg.html

(cl:defclass <None_FloatArray-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass None_FloatArray-request (<None_FloatArray-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_FloatArray-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_FloatArray-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_FloatArray-request> is deprecated: use hrl_srvs-srv:None_FloatArray-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_FloatArray-request>) ostream)
  "Serializes a message object of type '<None_FloatArray-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_FloatArray-request>) istream)
  "Deserializes a message object of type '<None_FloatArray-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_FloatArray-request>)))
  "Returns string type for a service object of type '<None_FloatArray-request>"
  "hrl_srvs/None_FloatArrayRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_FloatArray-request)))
  "Returns string type for a service object of type 'None_FloatArray-request"
  "hrl_srvs/None_FloatArrayRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_FloatArray-request>)))
  "Returns md5sum for a message object of type '<None_FloatArray-request>"
  "0db98d790b5b039efb61505385ae8369")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_FloatArray-request)))
  "Returns md5sum for a message object of type 'None_FloatArray-request"
  "0db98d790b5b039efb61505385ae8369")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_FloatArray-request>)))
  "Returns full string definition for message of type '<None_FloatArray-request>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_FloatArray-request)))
  "Returns full string definition for message of type 'None_FloatArray-request"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_FloatArray-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_FloatArray-request>))
  "Converts a ROS message object to a list"
  (cl:list 'None_FloatArray-request
))
;//! \htmlinclude None_FloatArray-response.msg.html

(cl:defclass <None_FloatArray-response> (roslisp-msg-protocol:ros-message)
  ((value
    :reader value
    :initarg :value
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass None_FloatArray-response (<None_FloatArray-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <None_FloatArray-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'None_FloatArray-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name hrl_srvs-srv:<None_FloatArray-response> is deprecated: use hrl_srvs-srv:None_FloatArray-response instead.")))

(cl:ensure-generic-function 'value-val :lambda-list '(m))
(cl:defmethod value-val ((m <None_FloatArray-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader hrl_srvs-srv:value-val is deprecated.  Use hrl_srvs-srv:value instead.")
  (value m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <None_FloatArray-response>) ostream)
  "Serializes a message object of type '<None_FloatArray-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'value))))
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
   (cl:slot-value msg 'value))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <None_FloatArray-response>) istream)
  "Deserializes a message object of type '<None_FloatArray-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'value) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'value)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<None_FloatArray-response>)))
  "Returns string type for a service object of type '<None_FloatArray-response>"
  "hrl_srvs/None_FloatArrayResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_FloatArray-response)))
  "Returns string type for a service object of type 'None_FloatArray-response"
  "hrl_srvs/None_FloatArrayResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<None_FloatArray-response>)))
  "Returns md5sum for a message object of type '<None_FloatArray-response>"
  "0db98d790b5b039efb61505385ae8369")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'None_FloatArray-response)))
  "Returns md5sum for a message object of type 'None_FloatArray-response"
  "0db98d790b5b039efb61505385ae8369")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<None_FloatArray-response>)))
  "Returns full string definition for message of type '<None_FloatArray-response>"
  (cl:format cl:nil "float64[] value~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'None_FloatArray-response)))
  "Returns full string definition for message of type 'None_FloatArray-response"
  (cl:format cl:nil "float64[] value~%~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <None_FloatArray-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'value) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <None_FloatArray-response>))
  "Converts a ROS message object to a list"
  (cl:list 'None_FloatArray-response
    (cl:cons ':value (value msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'None_FloatArray)))
  'None_FloatArray-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'None_FloatArray)))
  'None_FloatArray-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'None_FloatArray)))
  "Returns string type for a service object of type '<None_FloatArray>"
  "hrl_srvs/None_FloatArray")
