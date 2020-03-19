# aqua_pi
aquarium control using a raspberry pi zero


## how to automatically reconnect wifi:
Go to /etc/ifplugd/action.d/ and rename the ifupdown file to ifupdown.original
Then do: cp /etc/wpa_supplicant/ifupdown.sh ./ifupdown
Finally: sudo reboot
That's all. Test this by turning off/on your AP; you should see that your Raspberry Pi properly reconnects.
