import Tkinter, tkSimpleDialog
import sys 

def _useroffset(self):

  # tk requires argv to have a value
  sys.argv = ['']


  # create tk instance and hide the main window
  root = Tkinter.Tk()
  root.withdraw()

  # Ask the user for the offset value and return this 
  offset = 0
  offset = tkSimpleDialog.askfloat("Offset", "", parent=root, initialvalue=0)
  root.destroy()

  return offset
