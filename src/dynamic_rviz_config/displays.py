
class Displays(list):
    def __init__(self):
        None
        
    def add_display(self, name, class_name, topic=None, color=None, fields={}, enabled=True):
        d = {'Name': name, 'Class': class_name, 'Enabled': enabled}
        if topic:
            d['Topic'] = topic
        if color:
            d['Color'] = '%d; %d; %d'%color
        d.update(fields)
        self.append(d)

    def add_group(self, name, displays):
        self.add_display(name, 'rviz/Group', fields={'Displays': displays})
        
    def add_model(self, parameter='robot_description', tf_prefix=None):
        fields = {'Robot Description': parameter}
        if tf_prefix:
            fields['TF Prefix'] = tf_prefix
        self.add_display('RobotModel', 'rviz/RobotModel', fields=fields)
        
    def add_map(self, topic='/map', name='Map', alpha=None, scheme=None):
        fields = {}
        if alpha:
            fields['Alpha'] = alpha
        if scheme:
            fields['Color Scheme'] = scheme    
        self.add_display(name, 'rviz/Map', topic, fields=fields)
        
    def add_laserscan(self, topic='/base_scan', name=None, color=(46, 255, 0), size=0.1, alpha=None):
        if name is None:
            name = topic
        fields = {'Size (m)': size, 'Style': 'Spheres', 'Color Transformer': 'FlatColor'}
        if alpha:
            fields['Alpha'] = alpha
        self.add_display(name, 'rviz/LaserScan', topic, color, fields)

    def add_pose_array(self, topic='/particlecloud'):
        self.add_display('AMCL Cloud', 'rviz/PoseArray', topic)
        
    def add_footprint(self, topic, color=(0,170,255)):
        self.add_display('Robot Footprint', 'rviz/Polygon', topic, color)
        
    def add_path(self, topic, name, color=None):
        self.add_display(name, 'rviz/Path', topic, color)

    def add_pose(self, topic, name='Current Goal', color=None, arrow_shape=None):
        fields = {}
        if arrow_shape:
            fields['Head Length'] = arrow_shape[0]
            fields['Head Radius'] = arrow_shape[1]
            fields['Shaft Length'] = arrow_shape[2]
            fields['Shaft Radius'] = arrow_shape[3]
            fields['Shape'] = 'Arrow'
        self.add_display(name, 'rviz/Pose', topic, color, fields)
        
    def add_grid(self):
        self.add_display('Grid', 'rviz/Grid')    
        
    def add_tf(self, scale=None):
        fields = {}
        if scale:
            fields['Marker Scale'] = scale
        self.add_display('TF', 'rviz/TF', fields=fields)    

import yaml

def display_representer(dumper, data):
    return dumper.represent_sequence(u'tag:yaml.org,2002:seq', list(data))

yaml.add_representer(Displays, display_representer)
