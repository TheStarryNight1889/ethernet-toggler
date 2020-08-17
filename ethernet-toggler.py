import wmi
import ctypes
import sys
import pystray
import win32
from PIL import Image, ImageDraw
from pystray import Icon, Menu as menu, MenuItem as item
interface = "Ethernet"


def toggle():
    c=wmi.WMI()
    o=c.query("select * from Win32_NetworkAdapter")
    for conn in o :
        if conn.NetConnectionID == interface:
            if conn.NetEnabled:
                print(conn.Disable()) 
            else:
                conn.Enable()


def image(color1, color2, width=64, height=64):
    result = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(result)

    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)

    return result


def on_activate(icon, interface):
    if interface=="Quit":
        print('stopping...')
        icon.stop()
    else:
        toggle()


def setup(icon):
    icon.visible = True


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        menu=menu(item("Enable/Disable",lambda icon: on_activate(icon,interface)),menu.SEPARATOR,item("Quit",lambda icon: on_activate(icon,"Quit")))
        icon = Icon('ethernet-toggler',icon=image('white', 'black'),title="ethernet-toggler",menu=menu)

        icon.run(setup)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)

