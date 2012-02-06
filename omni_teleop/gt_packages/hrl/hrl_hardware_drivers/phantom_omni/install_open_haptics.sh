# /bin/bash
rosdep install phantom_omni
unzip OpenHapticsAE_Linux_v3_0.zip
#firefox http://dsc.sensable.com/3dtouch/OpenHaptics_Academic_linux/downloadFile.asp?file=3dtouch/OpenHapticsAE_Linux_v3_0.zip
sudo dpkg -i "OpenHapticsAE_Linux_v3_0/PHANTOM Device Drivers/64-bit/phantomdevicedrivers_4.3-3_amd64.deb"
sudo dpkg -i "OpenHapticsAE_Linux_v3_0/OpenHaptics-AE 3.0/64-bit/openhaptics-ae_3.0-2_amd64.deb"
cd /usr/lib && sudo ln -s libraw1394.so libraw1394.so.8
cd /usr/lib && sudo ln -s libXm.so.3 libXm.so.4
./set_permissions_1394.sh
/usr/sbin/PHANToMConfiguration

