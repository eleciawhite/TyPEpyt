// Auto-generated. Do not edit!

// (in-package typepyt.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class JointAngles {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.hip = null;
      this.shoulder = null;
      this.elbow = null;
      this.wrist = null;
    }
    else {
      if (initObj.hasOwnProperty('hip')) {
        this.hip = initObj.hip
      }
      else {
        this.hip = 0.0;
      }
      if (initObj.hasOwnProperty('shoulder')) {
        this.shoulder = initObj.shoulder
      }
      else {
        this.shoulder = 0.0;
      }
      if (initObj.hasOwnProperty('elbow')) {
        this.elbow = initObj.elbow
      }
      else {
        this.elbow = 0.0;
      }
      if (initObj.hasOwnProperty('wrist')) {
        this.wrist = initObj.wrist
      }
      else {
        this.wrist = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type JointAngles
    // Serialize message field [hip]
    bufferOffset = _serializer.float32(obj.hip, buffer, bufferOffset);
    // Serialize message field [shoulder]
    bufferOffset = _serializer.float32(obj.shoulder, buffer, bufferOffset);
    // Serialize message field [elbow]
    bufferOffset = _serializer.float32(obj.elbow, buffer, bufferOffset);
    // Serialize message field [wrist]
    bufferOffset = _serializer.float32(obj.wrist, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type JointAngles
    let len;
    let data = new JointAngles(null);
    // Deserialize message field [hip]
    data.hip = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [shoulder]
    data.shoulder = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [elbow]
    data.elbow = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [wrist]
    data.wrist = _deserializer.float32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'typepyt/JointAngles';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'bc7aa8d1069f4ed465de7f6e207623f0';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 hip
    float32 shoulder
    float32 elbow
    float32 wrist
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new JointAngles(null);
    if (msg.hip !== undefined) {
      resolved.hip = msg.hip;
    }
    else {
      resolved.hip = 0.0
    }

    if (msg.shoulder !== undefined) {
      resolved.shoulder = msg.shoulder;
    }
    else {
      resolved.shoulder = 0.0
    }

    if (msg.elbow !== undefined) {
      resolved.elbow = msg.elbow;
    }
    else {
      resolved.elbow = 0.0
    }

    if (msg.wrist !== undefined) {
      resolved.wrist = msg.wrist;
    }
    else {
      resolved.wrist = 0.0
    }

    return resolved;
    }
};

module.exports = JointAngles;
