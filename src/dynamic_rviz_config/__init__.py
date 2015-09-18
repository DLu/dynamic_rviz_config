import yaml
import rospy
import tempfile
from dynamic_rviz_config.displays import Displays

VIZ_MAN = 'Visualization Manager'

STD_TOOLS = ['rviz/Interact', 'rviz/MoveCamera', 'rviz/Select', 'rviz/FocusCamera',
            'rviz/Measure', 'rviz/SetInitialPose', 'rviz/SetGoal', 'rviz/PublishPoint']
            
STD_PANELS = ['rviz/Displays', 'rviz/Tool Properties', 'rviz/Views']            
            
def get_screen_resolutions():
    import subprocess
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    lines = output.strip().split('\n')
    R = []
    for line in lines:
        R.append( tuple( map(int, line.split('x') )))
    return R
            

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
        
    def add_standard_tools(self):
        v = self.get_visualization()
        if 'Tools' not in v:
            v['Tools'] = []
        for tool in STD_TOOLS:
            v['Tools'].append({'Class': tool})
        
    def set_tool_topic(self, name, topic):
        for m in self.data[VIZ_MAN]['Tools']:
            if m.get('Class', '')==name:
                m['Topic'] = topic
                return
    def set_fixed_frame(self,frame='map'):
        v = self.get_visualization()
        if 'Global Options' not in v:
            v['Global Options'] = {'Fixed Frame':frame}
        else:
            v['Global Options']['Fixed Frame'] = frame

    def set_goal(self, topic='goal'):
        self.set_tool_topic('rviz/SetGoal', topic)

    def set_initial_pose(self, topic='initialpose'):
        self.set_tool_topic('rviz/SetInitialPose', topic)
        
    def set_view(self, fields):
        self.get_visualization()['Views'] = {'Current': fields}    
        
    def set_full_window(self, monitor=0):
        R = get_screen_resolutions()[monitor]
        self.data['Window Geometry'] = {'X': 0, 'Y': 0, 'Width': R[0], 'Height': R[1]}
        
    def add_standard_panels(self):
        if 'Panels' not in self.data:
            self.data['Panels'] = []
        for tool in STD_PANELS:
            self.data['Panels'].append({'Class': tool, 'Name': tool.split('/')[-1]})
        
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
