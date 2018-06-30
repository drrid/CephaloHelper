from pywinauto.application import Application
from pywinauto import keyboard, mouse
import time


app = Application().start("C:/Users/Tarek/Desktop/BN cephalo/NNTViewer.exe")
time.sleep(1)
keyboard.SendKeys('{DOWN}')
time.sleep(0.3)
keyboard.SendKeys('{ENTER}')
time.sleep(1.5)
mouse.click(button='left', coords=(100, 400))
time.sleep(0.3)
app.window_(title_re = "iRYS*").MenuSelect("Dossier->Enregistrer l'image sous")
mouse.click(button='left', coords=(300, 400))
time.sleep(0.5)
keyboard.SendKeys('%t')
time.sleep(0.3)
keyboard.SendKeys('{DOWN}')
time.sleep(0.3)
keyboard.SendKeys('{DOWN}')
time.sleep(0.3)
keyboard.SendKeys('{ENTER}')
time.sleep(0.3)
keyboard.SendKeys('{ENTER}')
time.sleep(1.5)
keyboard.SendKeys('%{F4}')
