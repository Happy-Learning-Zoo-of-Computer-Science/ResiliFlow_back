"""serialize created nodes into a pipeline1 yaml file"""
"""deserialize pipeline1.yaml into node structure (array)"""

import yaml
import os
from pipelineDesign import Node,Position

file_path = "/Users/hsiangjou/Desktop/PBL G5/project/Data/pipeline.yaml"

def deserialize():
      file_path = "./Data/pipeline.yaml"

      if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} do not exist")
      
      with open(file_path, 'r') as file:
            data=yaml.safe_load(file)

      nodes = []

      for entry in data:
        nodeId = entry['id']  
        position = Position(entry['x'], entry['y'])  
        action = entry['action']  

        node = Node(nodeId, position, action)

        node.input_ports = entry.get('inputPort', [])
        node.output_ports = entry.get('outputPort', [])

        nodes.append(node) 

      return nodes

"""nodes = deserialize()
for node in nodes:
     print(repr(node))"""

#serialize the deserialed yaml file which pass from frontend into github action yaml format
def compile(nodes):
    folder = "./githubAction"
    os.makedirs(folder, exist_ok=True)

    github_action = {
        'name': 'Python application',  
        'on': {
            'push': {'branches': ['']}, 
            'pull_request': {'branches': ['']} 
        },
        'permissions': {
            'contents': 'read'  
        }
    }

    job_part = {
        'jobs': {
            'build': {
                'runs-on': 'ubuntu-latest',  
                'steps': [
                    {'uses': 'actions/checkout@v4'},  
                    
                    *[{
                        'name': node.id,  
                        'run': f'echo "{node.action}"'  
                    } for node in nodes]
                ]
            }
        }
    }

    github_action.update(job_part)
    file_path = os.path.join(folder, "GAFormat.yaml")

    with open(file_path, "w") as file:
        yaml.dump(github_action, file, default_flow_style=False)

    return folder
