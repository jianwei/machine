class work:
    def __init__(self):
        pass

if __name__ == "__main__":
    m = work()
    try:
        m.loop()
    except KeyboardInterrupt:
        print("ctrl+c stop")
        m.send_cmd("STOP 0")