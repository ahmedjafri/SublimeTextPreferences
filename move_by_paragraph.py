#
# Place in ~/Library/Application Support/Sublime Text 3/Packages/User/
#
# Author: Ahmed Jafri <ahmedjafri.com>
#
import sublime, sublime_plugin

class MoveByParagraphCommand(sublime_plugin.TextCommand):
    def run(self, edit, extend = False, forward = True):
        self.view.run_command("move_to", {"to": "hardbol", "extend": extend}) # move to beginning of line (hardbol)
        pt = self.view.sel()[0].b
        if forward:
            rg = self.view.find("\n\s*\n", pt) # Look for empty line
            new_pt = rg.b-1 if rg else self.view.size()
        else:
            rgs = self.view.find_all("\n[\s]*\n")
            new_pt = 0
            for rg in rgs:
                if rg.b < pt:
                    new_pt = rg.b-1
        new_pt_visible = self.view.visible_region().contains(new_pt)
        self.view.run_command("move", {"by": "lines", "forward": forward, "extend": extend})
        while (self.view.sel()[0].b < new_pt) == forward and self.view.sel()[0].b != pt:
            pt = self.view.sel()[0].b
            self.view.run_command("move", {"by": "lines", "forward": forward, "extend": extend})
        while self.view.sel()[0].b != new_pt:
            self.view.run_command("move", {"by": "characters", "forward": self.view.sel()[0].b < new_pt, "extend": extend})
        if not new_pt_visible:
            self.view.show_at_center(new_pt)