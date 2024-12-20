"""create node and store created nodes into a []"""

from app.services.pipelineDesign import Node, Position,setup_environment,install_dependencies,pyTest

def createNodes():
    setupNode=Node("setup_node",Position(0,0),setup_environment)
    setupNode.output_port="python_env"

    installNode=Node("install_node",Position(1,0), install_dependencies)
    installNode.input_port="python_env"
    installNode.output_port="dependencies_installed"

    pytestNode=Node("pytest_node",Position(2,0),pyTest)
    pytestNode.input_port="dependencies_installed"

    return [setupNode,installNode,pytestNode]

