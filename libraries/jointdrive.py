#JointDrive

import math
try:
    from libraries.servo_ax12a import ServoAx12a
except Exception as e:
    print(e)


# Class definition of ax12a-controller class, defines interface to the robot
#===============================================================================
# Implements the interface between leg- and servo class
# ------------------------------------------------------------------------------
# Provides all required methods that allow the leg class to control the servo
# Implements all necessary codomain conversion between leg- and servo values
# Limits values too valid servo values
# Servo uses ticks from 0 to 1023 for angle and speed
# Leg uses angles in radian and rotation per minute for speed
# Defines zero angle as average of min- and max value -> positive and negative angles are allowed
class JointDrive(ServoAx12a):

    # Definition of public class attributes
    #----------------------------------------------------------------------
    _ANGLE_RADIAN_ZERO = (ServoAx12a._ANGLE_MAX_DEGREE - ServoAx12a._ANGLE_MIN_DEGREE) * math.pi / 360  	            # Zero angle offset of servo in radian
    _ANGLE_UNIT = ServoAx12a._ANGLE_MAX_TICKS / ((ServoAx12a._ANGLE_MAX_DEGREE - ServoAx12a._ANGLE_MIN_DEGREE) * math.pi * 2 / 360)  # Ticks per rad
    

    # Private methods    
    #----------------------------------------------------------------------
    # Constructor, defines the folowing variables: counterClockWise, angleOffset, angleMax, angleMin
    # id -> id of servo,
    # ccw -> rotating direction,
    # aOffset -> angle offset,
    # aMax -> maximum angle allowed,
    # aMin -> minimum angle allowed
    def __init__(self, id, ccw = False, aOffset = 0.0, aMax = math.pi * 5/6, aMin = -(math.pi * 5/6)):
        ServoAx12a.__init__(self,id)
        self.counterClockWise=ccw
        self.angleOffset=aOffset
        self.angleMax=aMax
        self.angleMin=aMin
        
        #offset and CCW
        self.ccwValue=1
        if ccw==True:
            self.ccwValue=-1
        
        #Default moving speed
        self.setMovingSpeed(20)
        
        #aMin and aMax 
        aMaxTicks=self.__convertAngleToTicks(aMax)
        aMinTicks=self.__convertAngleToTicks(aMin)
        if aMinTicks>aMaxTicks:
            aMinTicks,aMaxTicks=aMaxTicks,aMaxTicks
        #print("maxticks1",aMaxTicks)
        #print("minticks1",aMinTicks)
        aMaxTicks=1023
        aMinTicks=0
        aMaxMinTicks=[]
        aMaxMinTicks.append(aMinTicks&255)
        aMaxMinTicks.append(aMinTicks>>8)
        aMaxMinTicks.append(aMaxTicks&255)
        aMaxMinTicks.append(aMaxTicks>>8)
        self._writeNBytePkt(0x06,aMaxMinTicks,False)
        
        
        
        
        
        
    # Converts angle in radian to servo ticks
    # angle -> in radian, returns angle in servo ticks
    def __convertAngleToTicks(self, angle):
        radPerTick=(300/1024)*(math.pi/180)
        ticks=512+int(((angle+self.angleOffset)*self.ccwValue)/radPerTick)
        #print("ticks",ticks)
        return ticks
    
    # Converts servo ticks to angle in radian
    # ticks -> servo ticks, returns angle in radian
    def __convertTicksToAngle(self, ticks):
        print(ticks)
        radPerTick=(300/1024)*(math.pi/180)
        angle = (( radPerTick*ticks -(math.pi*5/6)-self.angleOffset)*self.ccwValue)
        return angle
    
    # Converts speed in rpm to servo ticks
    # speed -> value in rpm
    def __convertSpeedToTicks(self, speed):
        return int((speed/self._SPEED_UNIT))
    
    # Converts ticks to speed in rpm
    # ticks -> servo ticks
    def __convertTicksToSpeed(self, ticks):
        return (ticks*self._SPEED_UNIT)

    # Public methods    
    #----------------------------------------------------------------------
    # Get current angle of servo
    # returns angle in radian
    def getCurrentJointAngle(self):
        return(self.__convertTicksToAngle(self.getPresentPosition()))

    # Set servo to desired angle
    # angle -> in radian,
    # speed -> speed of movement, speed < 0 -> no speed set, speed = 0 -> maximum speed
    def setDesiredJointAngle(self, angle, trigger = False):
        ticks=self.__convertAngleToTicks(angle)
        self.setGoalPosition(ticks, trigger)

    # Set servo to desired angle
    # angle -> in radian,
    # speed -> speed of movement in rpm, speed = 0 -> maximum speed
    def setDesiredAngleSpeed(self, angle, speed = 0, trigger = False):
        ticks=self.__convertAngleToTicks(angle)
        speedInTicks=self.__convertSpeedToTicks(speed)
        actionsTicks=[]
        actionsSpeed=[]
        actionsTicks.append(ticks&255)
        actionsTicks.append(ticks>>8)
        actionsSpeed.append(speedInTicks&255)
        actionsSpeed.append(speedInTicks>>8)
        self.setGoalPosSpeed(actionsTicks,actionsSpeed,trigger)
        
    
    # Set speed value of servo
    # speed -> angle speed in rpm
    def setSpeedValue(self, speed, trigger = False):
        speedInTicks=self.__convertSpeedToTicks(speed)
        self.setMovingSpeed(speedInTicks, trigger)

    # Start all Servos with have trigger=true set
    def startAllServos(self):
        self.servoBroadcastAction()
    
    def getOffset(self):
        return self.angleOffset

