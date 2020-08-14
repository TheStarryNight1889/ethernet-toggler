import wmi
import pyuac
import pystray
import win32
from PIL import Image, ImageDraw
from pystray import Icon, Menu as menu, MenuItem as item

interfaces = []

def get_interfaces():
    c=wmi.WMI()
    o=c.query("select * from Win32_NetworkAdapter")
    for conn in o:
        if conn.NetConnectionID and conn.NetEnabled:
            interfaces.append(conn.NetConnectionID + "- ON")
        elif conn.NetConnectionID:
            interfaces.append(conn.NetConnectionID + "- OFF")

def toggle(adapter):
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()

    c=wmi.WMI()
    o=c.query("select * from Win32_NetworkAdapter")

    for conn in o :
        if conn.NetConnectionID == adapter:
            if conn.NetEnabled:
                conn.Disable() 
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
        toggle(interface)
        #icon.update_menu()


def setup(icon):
    icon.visible = True

get_interfaces()
items = []
for interface in interfaces:
    name = interface.split("-")
    items.append(item(interface, lambda icon: on_activate(icon, name[0])))

menu=menu(*items,menu.SEPARATOR,item("Quit",lambda icon: on_activate(icon,"Quit")))
icon = Icon('ethernet-toggler',icon=image('white', 'black'),title="ethernet-toggler",menu=menu)

icon.run(setup)
