import json


class Settings:
    def __init__(self, filename="settings.json"):
        self.text = ""
        try:
            self.text = open("default.json").read()
        except Exception:
            print("File %s not found" % "default.json")
            return
        j = json.loads(self.text)
        try:
            self.ip = j["ip"]
            self.port = j["port"]
            self.camport = j["camport"]
            self.blue_on_right = j["blue_on_right"]
            self.P = j["PID"]["P"]
            self.I = j["PID"]["I"]
            self.D = j["PID"]["D"]
            self.speed = j["speed"]
            self.goal = j["goal"]
            self.switch_lr = j["switch_lr"]
            self.arm_angles = j["arm_angles"]
        except Exception:
            print("loading default.json failed: keys missing")
            pass
        
        print("loading %s" % filename)
        self.update(filename = filename)

    def update(self, filename ):
        try:
            self.text = open(filename).read()
        except Exception:
            print("File %s not found" % filename)
            return
        j = json.loads(self.text)
        try:
            self.ip = j["ip"]
            self.port = j["port"]
            self.camport = j["camport"]
            self.blue_on_right = j["blue_on_right"]
            self.P = j["PID"]["P"]
            self.I = j["PID"]["I"]
            self.D = j["PID"]["D"]
            self.speed = j["speed"]
            self.goal = j["goal"]
            self.switch_lr = j["switch_lr"]
            self.arm_angles:dict[str, int] = j["arm_angles"]
        except Exception:
            print("loading %s failed: keys missing" % filename)
            return

