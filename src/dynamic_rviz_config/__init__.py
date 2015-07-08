import yaml
import rospy
import tempfile

class RVizConfig:
    def __init__(self, base_file=None):
        if base_file:
            self.data = yaml.load( base_file )
        else:
            self.data = {}
            
    def add_display(self, name, class_name, topic=None, color=None, fields={}):
        print name, topic
        d = {'Name': name, 'Class': class_name, 'Enabled': True}
        if topic:
            d['Topic'] = topic
        if color:
            d['Color'] = '%d; %d; %d'%color
        d.update(fields)
        self.data['Visualization Manager']['Displays'].append(d)
        
    def set_tool_topic(self, name, topic):
        for m in self.data['Visualization Manager']['Tools']:
            if m.get('Class', '')==name:
                m['Topic'] = topic
                return
        
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
        
    def set_goal(self, topic):
        self.set_tool_topic('rviz/SetGoal', topic)
        
    def __repr__(self):
        return yaml.dump( self.data, default_flow_style=False)

    def run(self, debug=False):
        temp = tempfile.NamedTemporaryFile()
        temp.write(str(self))
        if debug:
            print str(self)
        temp.flush()

        import subprocess
        subprocess.call(['rosrun','rviz','rviz', '-d', temp.name])
        temp.close()
