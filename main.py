from pythonScripts.beNG import *
from pythonScripts.feNG import *

if __name__ == '__main__':
    init_dialogues()
    scripts = convert_all_scripts()
    manager = DialogueManager()
    if len(scripts) > 0:
        manager.load_script(scripts[0])
    manager.mainloop()
