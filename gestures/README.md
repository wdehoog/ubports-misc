# A simple gesture daemon

Listens to gesture events on dbus (com.ubports.Unity.Gestures).

Only tested on Oneplus One. It needs a [modified kernel](https://github.com/ubports/android_kernel_oneplus_msm8974/pull/4), [modified unity-system-compositor](https://github.com/ubports/unity-system-compositor/pull/11)
 and enabled gestures (see /proc/touchpanel).

Supported gestures:
  * play-pause: send PlayPause to mpris2 players
  * next-song: send Next to mpris2 players
  * previous-song: send Previous to mpris2 players
  * toggle-flash: toggles the flash-led

The upstart file gesture-daemon.conf can be put in ~/.config/upstart/ to have the daemon launched at startup. 
