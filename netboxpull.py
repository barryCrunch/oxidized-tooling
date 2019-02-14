import pynetbox
import os

def pullDevices(nb):
    return nb.dcim.devices.all()


def validateDevices(devices):
    validDevices = []
    for i in devices:
        if i.platform != None and i.primary_ip4 != None:
            validDevices.append(i)
    return validDevices

def writeDB(devices):
    with open('router.db', 'w') as file:
        for i in devices:
            if 'noenable' in i.tags:
                group = 'noenable'
            else:
                group = 'enable'
            d = {}
            d['name'] = i.name
            d['ip'] = i.primary_ip4
            d['model'] = i.platform.slug
            user = os.environ['USERNAME']
            passwd = os.environ['PASSWORD']
            file.write(f"{i.name.split(' ')[0]}:"
                        f"{i.primary_ip4.address.split('/')[0]}"
                        f":{i.platform.slug}:{user}:{passwd}:{group}\n")

if __name__ == '__main__':
    nb = pynetbox.api(
        os.environ['NETBOX_URL'],
        token=os.environ['NETBOX_TOKEN']
    )
    devices = pullDevices(nb)
    active_devices = validateDevices(devices)
    writeDB(active_devices)
