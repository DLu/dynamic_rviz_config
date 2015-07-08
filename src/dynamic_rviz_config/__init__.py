import yaml
import rospy
import tempfile
from dynamic_rviz_config.displays import Displays

VIZ_MAN = 'Visualization Manager'

class RVizConfig:
    def __init__(self, base_file=None):
        if base_file:
            self.data = yaml.load( base_file )
        else:
            self.data = {}

    def get_visualization(self):
        if VIZ_MAN not in self.data:
            self.data[VIZ_MAN] = {}
        return self.data[VIZ_MAN]            

    def get_displays(self):
        if 'Displays' not in self.get_visualization():
            self.data[VIZ_MAN]['Displays'] = Displays()
        return self.data[VIZ_MAN]['Displays']    
        
    def set_tool_topic(self, name, topic):
        for m in self.data[VIZ_MAN]['Tools']:
            if m.get('Class', '')==name:
                m['Topic'] = topic
                return

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
