# A simple gesture daemon

Listens to gesture events on dbus (com.ubports.Unity.Gestures).

Only tested on Oneplus One. It needs [modified unity-system-compositor](https://github.com/wdehoog/unity-system-compositor/tree/xenial_-_add-media-keys) and a [modified unity8](https://github.com/wdehoog/unity8/tree/xenial_-_handle-media-keys) and enabled touch panel gestures:

```
echo 1 > /proc/touchpanel/music_enable
echo 1 > /proc/touchpanel/double_tap_enable
echo 1 > /proc/touchpanel/flashlight_enable
```

Supported gestures:
  * play-pause: send PlayPause to mpris2 players
  * next-song: send Next to mpris2 players
  * previous-song: send Previous to mpris2 players
  * media key (for example headset button):
    * click: pause/play
    * double click: next song
    * triple click: previous song
  * toggle-flash: toggles the flash-led

The upstart file gesture-daemon.conf can be put in ~/.config/upstart/ to have the daemon launched at startup. 
