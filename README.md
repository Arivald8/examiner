# examiner
Examiner tool for use on Windows OS devices. Locks and unlocks a device for exam-like conditions.

Please note that in order for the tool to work as intended, you must disable Task Manager 
from appearing in the CTRL + ALT + DEL menu. In order to do this, disable it via
the Local Group Policy Editor:

    --> Local Group Policy Editor
        --> User Configuration
            --> Administrative Templates 
                --> System 
                    --> Ctrl + Alt + Del Options
                        --> Remove Task Manager.

