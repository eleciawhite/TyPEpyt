; Auto-generated. Do not edit!


(cl:in-package typepyt-msg)


;//! \htmlinclude JointAngles.msg.html

(cl:defclass <JointAngles> (roslisp-msg-protocol:ros-message)
  ((hip
    :reader hip
    :initarg :hip
    :type cl:float
    :initform 0.0)
   (shoulder
    :reader shoulder
    :initarg :shoulder
    :type cl:float
    :initform 0.0)
   (elbow
    :reader elbow
    :initarg :elbow
    :type cl:float
    :initform 0.0)
   (wrist
    :reader wrist
    :initarg :wrist
    :type cl:float
    :initform 0.0))
)

(cl:defclass JointAngles (<JointAngles>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <JointAngles>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'JointAngles)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name typepyt-msg:<JointAngles> is deprecated: use typepyt-msg:JointAngles instead.")))

(cl:ensure-generic-function 'hip-val :lambda-list '(m))
(cl:defmethod hip-val ((m <JointAngles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader typepyt-msg:hip-val is deprecated.  Use typepyt-msg:hip instead.")
  (hip m))

(cl:ensure-generic-function 'shoulder-val :lambda-list '(m))
(cl:defmethod shoulder-val ((m <JointAngles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader typepyt-msg:shoulder-val is deprecated.  Use typepyt-msg:shoulder instead.")
  (shoulder m))

(cl:ensure-generic-function 'elbow-val :lambda-list '(m))
(cl:defmethod elbow-val ((m <JointAngles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader typepyt-msg:elbow-val is deprecated.  Use typepyt-msg:elbow instead.")
  (elbow m))

(cl:ensure-generic-function 'wrist-val :lambda-list '(m))
(cl:defmethod wrist-val ((m <JointAngles>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader typepyt-msg:wrist-val is deprecated.  Use typepyt-msg:wrist instead.")
  (wrist m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <JointAngles>) ostream)
  "Serializes a message object of type '<JointAngles>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'hip))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'shoulder))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'elbow))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'wrist))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <JointAngles>) istream)
  "Deserializes a message object of type '<JointAngles>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'hip) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'shoulder) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'elbow) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'wrist) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<JointAngles>)))
  "Returns string type for a message object of type '<JointAngles>"
  "typepyt/JointAngles")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'JointAngles)))
  "Returns string type for a message object of type 'JointAngles"
  "typepyt/JointAngles")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<JointAngles>)))
  "Returns md5sum for a message object of type '<JointAngles>"
  "bc7aa8d1069f4ed465de7f6e207623f0")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'JointAngles)))
  "Returns md5sum for a message object of type 'JointAngles"
  "bc7aa8d1069f4ed465de7f6e207623f0")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<JointAngles>)))
  "Returns full string definition for message of type '<JointAngles>"
  (cl:format cl:nil "float32 hip~%float32 shoulder~%float32 elbow~%float32 wrist~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'JointAngles)))
  "Returns full string definition for message of type 'JointAngles"
  (cl:format cl:nil "float32 hip~%float32 shoulder~%float32 elbow~%float32 wrist~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <JointAngles>))
  (cl:+ 0
     4
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <JointAngles>))
  "Converts a ROS message object to a list"
  (cl:list 'JointAngles
    (cl:cons ':hip (hip msg))
    (cl:cons ':shoulder (shoulder msg))
    (cl:cons ':elbow (elbow msg))
    (cl:cons ':wrist (wrist msg))
))
