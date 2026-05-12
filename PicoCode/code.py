import board
import busio
import time
import json
from adafruit_bno08x.i2c import BNO08X_I2C

# HARDWARE IDs (From the BNO085 Datasheet)
# 0x05 = Rotation Vector (Quat)
# 0x04 = Linear Acceleration
# 0x02 = Gyroscope
# 0x03 = Magnetic Field
REPORTS = [0x05, 0x04, 0x02, 0x03]

try:
    i2c = busio.I2C(board.GP5, board.GP4)
    bno = BNO08X_I2C(i2c)
    
    # Enable every feature using its raw Hardware ID
    for report_id in REPORTS:
        bno.enable_feature(report_id)
    
    print("--- SCUN-GUN: FULL TELEMETRY LOCKED ---")

except Exception as e:
    print(json.dumps({"status": "critical_failure", "msg": str(e)}))

while True:
    try:
        # Get data objects
        q = bno.quaternion
        a = bno.linear_acceleration
        g = bno.gyro
        m = bno.magnetic
        
        # Check that we have a full "Frame" of data
        if all((q, a, g, m)):
            print(json.dumps({
                "qw": round(q[3], 4), "qx": round(q[0], 4), "qy": round(q[1], 4), "qz": round(q[2], 4),
                "ax": round(a[0], 4), "ay": round(a[1], 4), "az": round(a[2], 4),
                "gx": round(g[0], 4), "gy": round(g[1], 4), "gz": round(g[2], 4),
                "mx": round(m[0], 4), "my": round(m[1], 4), "mz": round(m[2], 4)
            }))
            
    except Exception:
        pass
        
    time.sleep(0.01) # 100Hz
