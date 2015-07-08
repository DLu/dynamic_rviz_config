
class Displays(list):
    def __init__(self):
        None
        
    def add_display(self, name, class_name, topic=None, color=None, fields={}):
        print name, topic
        d = {'Name': name, 'Class': class_name, 'Enabled': True}
        if topic:
            d['Topic'] = topic
        if color:
            d['Color'] = '%d; %d; %d'%color
        d.update(fields)
        self.append(d)

    def add_group(self, name, displays):
        self.add_display(name, 'rviz/Group', fields={'Displays': displays})
        
    def add_model(self, parameter='robot_description'):
        self.add_display('RobotModel', 'rviz/RobotModel', fields={'Robot Description': parameter})
        
    def add_map(self, topic='/map', name='Map'):
        self.add_display(name, 'rviz/Map', topic)
        
    def add_laserscan(self, topic='/base_scan', color=(46, 255, 0)):
        self.add_display(topic, 'rviz/LaserScan', topic, color, 
            {'Size (m)': .1, 'Style': 'Spheres', 'Color Transformer': 'FlatColor'})

    def add_pose_array(self, topic='/particlecloud'):
        self.add_display('AMCL Cloud', 'rviz/PoseArray', topic)
        
    def add_footprint(self, topic, color=(0,170,255)):
        self.add_display('Robot Footprint', 'rviz/Polygon', topic, color)
        
    def add_path(self, topic, name, color=None):
        self.add_display(name, 'rviz/Path', topic, color)

    def add_pose(self, topic):
        self.add_display('Current Goal', 'rviz/Pose', topic)

import yaml

def display_representer(dumper, data):
    return dumper.represent_sequence(u'tag:yaml.org,2002:seq', list(data))

yaml.add_representer(Displays, display_representer)
