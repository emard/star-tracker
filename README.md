# motor speed and gcode to drive it


Z axis setting has 400 steps per mm
1.8° motor for 200 steps does one full turn
M6 thread has 1 mm thread pitch so 1 turn = 1 mm

0.5 mm/s = 1 turn/s = 60 rpm
30 mm/min = 60 turn/min
55 mm/min = 110 turn/min

;motor connector [2B 2A 1A 1B] = [2- 2+ 1+ 1-]

;screen /dev/ttyACM0


; relative mode
G91
; set steps per unit we need 200 full steps per unit
; but if motor is driven in 1/16 microsteps (Configuration_adv.h TMC drivers)
; #define Z2_MICROSTEPS   128
; we must multiply full steps per revoltion by microsteps:
; 200*16=3200
M92 Z3200
; now feedrate (F parameter) means directly RPM

; set motor Z2 max current 100mA
M906 I1 Z100
; set motor Z max current 100mA
M906 Z100
; print settings
M906
; run one minute 110 RPM
G0 Z110 F110
; run few seconds 60 RPM
G0 Z10 F60

; high speed limit
M203 Z10000

; running: connect motors to X Y Z axis

;read steps per unit
M92

;set steps per unit (1 unit = 1 mm)
M92 X3200 Y3200 Z3200

;set motor inactivity timeout 1 s (save power)
M18 S1 X Y Z

;read endstop status (test them with blue jumpers)
M119

;set absolute mode
G90

;set relative mode
G91

;motor go to position XYZ=1,2,3 mm
;at feed rate 10 mm/minute
G1 X1 Y2 Z3 F10

; full stroke is about 300 mm

;turn 12/24V FAN LED ON
M106
;turn 12/24V FAN LED OFF
M107

;read motor current setting
M906
;set X Y Z current [mA]
M906 X1200 Y1200 Z1200
;StealthChop on X axis (silent)
M569 S1 X
;SpreadCycle on X axis (noisy)
M569 S0 X
