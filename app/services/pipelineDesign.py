"""including define node structure"""


class Position:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Node:
    def __init__(self, nodeId: str, position: Position, action):
        self.id = nodeId
        self.label = ""
        self.position = position
        self.action = action
        self.input_port = ""
        self.output_port = ""

    def execute(self):
        self.action()

    # serialize created node into yaml format(for frontend)
    def toDict(self):
        return {
            "id": self.id,
            "label": self.label,
            "position":
                {
                    "x": self.position.x,
                    "y": self.position.y,
                },
            "__class": self.action + "NodeData",
            "inputPort": self.input_port,
            "outputPort": self.output_port
        }

    def __repr__(self):
        return f"[id={self.id}, position=({self.position.x}, {self.position.y}), action={self.action}, input_ports={self.input_port}, output_ports={self.output_port}]"


def setup_environment():
    print("setup environment")


def install_dependencies():
    print("install dependencies")


def pyTest():
    print("run pyTest")
