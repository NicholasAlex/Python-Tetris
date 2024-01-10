class Colors:
    darkGrey = (26, 31, 40)
    green = (47,230, 23)
    red = (232, 18, 18)
    orange = (236, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    white = (255, 255, 255)
    darkBlue = (44, 44, 127)
    lightBlue = (59, 85, 162)

    @classmethod
    def getCellColors(cls):
        return [cls.darkGrey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]