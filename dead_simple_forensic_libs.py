###################### Psutil Example ######################
# Gives information on:
#     Processes - good for malware, anti-forensics, etc
#     CPU
#     Memory
#     Disks - gives us other places to look for files
#     Network - good for malware, malicious sites etc.
#     Other system info
#
# See the docs at: http://pythonhosted.org/psutil/
############################################################

import psutil
import datetime

SEPARATOR = '\n*******************\n'

# Network. Options = all, inet, tcp, udp etc.
for conn in psutil.net_connections(kind='tcp'):
    print conn
print SEPARATOR

# Disk partitions
print psutil.disk_partitions()
print SEPARATOR

# Disk cap vs. used
print psutil.disk_usage('/')
print SEPARATOR

# Other sys info: Grab the users and boot time
print psutil.users()
print datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
print SEPARATOR

# Processes: Can examine further, recurse children, kill etc.
for proc in psutil.process_iter():
    try:
        pinfo = proc.as_dict(attrs=['pid', 'name'])
    except psutil.NoSuchProcess:
        pass
    else:
        print(pinfo)


# ############# VSS Method for OS Locked Files ##############
# #
# # Example derived from:
# # http://pen-testing.sans.org/blog/2013/04/12/using-volume-shadow-copies
# # -from-python
# # Not preferred method to pull from vss- instead use pyvshadow like below.
# # 1) cmd as admin, vssadmin list shadows (sometimes does not get all)
# # 2) Get volume shadow volume and plug into code
# #
# ###########################################################
#
import os

# We're in unicode, so escape the slashes by doubling the amount
print os.path.isfile(u'\\\\?\\GLOBALROOT\Device\HarddiskVolumeShadowCopy1'
                     u'\$Extend\$UsnJrnl:$J')



# # ################### PyTSK3 Example ######################
# # # Read the docs here: https://github.com/py4n6/pytsk/wiki/Development
# # #########################################################
# #
#
import pytsk3
import os
print 'opening drive'
img = pytsk3.Img_Info("\\\\.\\C:")
fs_info = pytsk3.FS_Info(img)
print 'opening file'
file_entry = fs_info.open('/$MFT')
dest_file = open(os.getcwd() + '\mft', 'wb')
print 'reading file'
for attr in file_entry:
    if attr.info.type == pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA:
        offset = 0

        size = attr.info.size
        print 'size is', size

        while offset < size:
            available_to_read = min(1024*1024, size - offset)
            data = file_entry.read_random(offset, available_to_read, attr.info.type, attr.info.id)
            if not data:
                break
            offset += len(data)
            dest_file.write(data)
        dest_file.close()
        break





########### Iterating VSS With Pyvshadow ##################

# What happens when we're missing VSS on vssadmin? Try pyvshadow to find them
# Check out the docs here: https://github.com/libyal/libvshadow/wiki/Development

###########################################################
import pytsk3
import pyvshadow

vshadow_volume = pyvshadow.volume()

# Logical or physical works here
vshadow_volume.open("\\\\.\\C:")

#What members do we have?
print pyvshadow.store.__dict__
print pyvshadow.volume.__dict__

for store in vshadow_volume.get_stores():
    print store.get_copy_set_identifier(), store.get_creation_time()

# from http://plaso.googlecode.com/git-history/4da4719ec97bbb4f929b14bea635e4cc3d4ffec2/lib/vss.py
class VShadowImgInfo(pytsk3.Img_Info):
  """Extending the TSK Img_Info to allow VSS images to be read in."""

  def __init__(self, store):
    self._store = store
    super(VShadowImgInfo, self).__init__()

  # Implementing an interface
  def read(self, offset, size):  # pylint: disable=C6409
    self._store.seek(offset)
    return self._store.read(size)

  # Implementing an interface
  def get_size(self):  # pylint: disable=C6409
    return self._store.get_size()

store = vshadow_volume.get_store(0)
img = VShadowImgInfo(store)
print 'opening vshadow fs'
fs_info = pytsk3.FS_Info(img)
print 'done opening vshadow fs'
file_entry = fs_info.open('/$MFT')


for attr in file_entry:
    if attr.info.type == pytsk3.TSK_FS_ATTR_TYPE_NTFS_DATA:
        offset = 0
        size = attr.info.size

        dest_file = open(os.getcwd() + '\mft_vshadow', 'wb')
        while offset < size:
            available_to_read = min(1024*1024, size - offset)
            data = file_entry.read_random(offset, available_to_read, attr.info.type, attr.info.id)
            if not data:
                break
            offset += len(data)
            dest_file.write(data)

        dest_file.close()


vshadow_volume.close()