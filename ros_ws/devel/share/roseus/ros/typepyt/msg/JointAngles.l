;; Auto-generated. Do not edit!


(when (boundp 'typepyt::JointAngles)
  (if (not (find-package "TYPEPYT"))
    (make-package "TYPEPYT"))
  (shadow 'JointAngles (find-package "TYPEPYT")))
(unless (find-package "TYPEPYT::JOINTANGLES")
  (make-package "TYPEPYT::JOINTANGLES"))

(in-package "ROS")
;;//! \htmlinclude JointAngles.msg.html


(defclass typepyt::JointAngles
  :super ros::object
  :slots (_hip _shoulder _elbow _wrist ))

(defmethod typepyt::JointAngles
  (:init
   (&key
    ((:hip __hip) 0.0)
    ((:shoulder __shoulder) 0.0)
    ((:elbow __elbow) 0.0)
    ((:wrist __wrist) 0.0)
    )
   (send-super :init)
   (setq _hip (float __hip))
   (setq _shoulder (float __shoulder))
   (setq _elbow (float __elbow))
   (setq _wrist (float __wrist))
   self)
  (:hip
   (&optional __hip)
   (if __hip (setq _hip __hip)) _hip)
  (:shoulder
   (&optional __shoulder)
   (if __shoulder (setq _shoulder __shoulder)) _shoulder)
  (:elbow
   (&optional __elbow)
   (if __elbow (setq _elbow __elbow)) _elbow)
  (:wrist
   (&optional __wrist)
   (if __wrist (setq _wrist __wrist)) _wrist)
  (:serialization-length
   ()
   (+
    ;; float32 _hip
    4
    ;; float32 _shoulder
    4
    ;; float32 _elbow
    4
    ;; float32 _wrist
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _hip
       (sys::poke _hip (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _shoulder
       (sys::poke _shoulder (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _elbow
       (sys::poke _elbow (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _wrist
       (sys::poke _wrist (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _hip
     (setq _hip (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _shoulder
     (setq _shoulder (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _elbow
     (setq _elbow (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _wrist
     (setq _wrist (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get typepyt::JointAngles :md5sum-) "bc7aa8d1069f4ed465de7f6e207623f0")
(setf (get typepyt::JointAngles :datatype-) "typepyt/JointAngles")
(setf (get typepyt::JointAngles :definition-)
      "float32 hip
float32 shoulder
float32 elbow
float32 wrist

")



(provide :typepyt/JointAngles "bc7aa8d1069f4ed465de7f6e207623f0")


