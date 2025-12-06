class State:
    def __init__(self, x, y, o, parent=None, action=None):
        self.x = x          # row
        self.y = y          # column
        self.o = o          # 0=nord, 1=est, 2=sud, 3=ouest
        self.parent = parent
        self.action = action  # command that led here ('a1','D','G', etc.)