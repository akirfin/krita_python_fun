"""

let's have some fun with python coding 03

Arc Welding! (now we're cooking with GAS)

"""

from krita import Krita

import particle
        # particle.Particle
        # particle.Cloud
        # particle.Spawner
        # particle.System


class ArcWeldingToolExtension(Extension):
    """
    Add tool to Krita.
    (this NOT official way to add new tools.)
    """

    def __init__(self):
        super(ArcWeldingToolExtension, self).__init__()


    def setup(self):
        pass


    def createActions(self, window):
        self._arc_welding_tool_context = particle.System()
        activate_arc_welding_action = create_action(window, "activate_arc_welding", "Activate Arc Welding", "menu/path")
        activate_arc_welding_action.trigger(self.act_activate_arc_welding)


    def act_activate_arc_welding(self, checked=None):
        """
        activate arc welding tool.
        """
        self._tool_context.show()
