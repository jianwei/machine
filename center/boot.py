import os


class boot():
    def __init__(self):
        pass

    def open_camera(self):
        print ("---------------------------------------open camera--------------------------------------")
        cmd = "cd ../StrongSORT/ && python3 track.py --source 0  &"
        os.system(cmd)
        pass



if __name__ == '__main__':
    b = boot()
    b.open_camera()
