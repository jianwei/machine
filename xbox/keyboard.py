import sys,json
from pathlib import Path
from pynput import keyboard
path = str(Path(__file__).resolve().parents[1])
sys.path.append(path)
from redisConn.index import redisDB
redis = redisDB()
# 前 w
# 后 s 
# 上 u
# 下 i
# 左 j
# 右 k
def on_press(key):
    try:
        cmd = {}
        # print('alphanumeric key {0} pressed'.format(key.char))
        if (key.char=="w"): 
            cmd["wheel"] =  "MF"
            cmd["speed"] =  10
        if (key.char=="s"): 
            cmd["wheel"] =  "MB"
            cmd["speed"] =  10
        if (key.char=="u"): 
            cmd["slide"] =  "ML"
            cmd["distance"] =  10
        if (key.char=="i"): 
            cmd["slide"] =  "MR"
            cmd["distance"] =  10
        if (key.char=="j"): 
            cmd["slide"] = "MU"
            cmd["distance"] =  10
        if (key.char=="k"): 
            cmd["slide"] =  "MD"
            cmd["distance"] =  10
        print (cmd)
        redis.set("machine_cmd", json.dumps(cmd))
    except AttributeError:
        pass
        # print('special key {0} pressed'.format(key))

def on_release(key):
    # print('{0} released'.format( key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
