# Matrix Portal API Portal
### A Portal for a Portal

This codebase for an Adafruit Matrix Portal is intended to serve as a simple way to connect to and display updates from any API that returns short strings of text.

An in-progress project by James Carey.

Uses the font [creep2](https://github.com/raymond-w-ko/creep2) by [Raymond W. Ko](https://github.com/raymond-w-ko).

## Set-Up
#### Required Materials:
- A MatrixPortal M4 controller from Adafruit
- A connected LED Matrix
- USB-C power cable
#### Optional Materials:
- A connected speaker, for audio playback

### Updating the CircuitPython version
1. First, download the latest version of CircuitPython for your device (a MatrixPortal M4) from [the CircuitPython site here](https://circuitpython.org/board/matrixportal_m4/).
2. Connect the MatrixPortal to your computer using a USB-C cable. It will show up as a new device or drive. *(You may have a pop-up window asking if you want to connect to the 'accessory,' press 'yes')* If it shows up as `MATRIXPORTAL`, it does not have  If it shows up named `CIRCUITPYTHON`, it is running some version of CircuitPython already. 
3. Drag-and-drop the .uf2 file onto the drive of the MatrixPortal, which should automatically reset

### Connecting to the Serial Console
The Serial Console is the main way to tell what's happening with the MatrixPortal that's not just what's on the screen or files on the device.

To connect with the Serial Console on Mac:
1. Plug your MatrixPortal into your computer via USB-C
2. Open Terminal
3.  Run the following command to find out the port (like an internal address) to connect to your MatrixPortal on: 
	```shell 
	ls /dev/tty.*
	```
4. The above command will return a list of devices. We're looking for one that includes the phrase `usbmodem`. It will look like `/dev/tty.usbmodem10001`.
5. Use the device found above with the `screen` command. `screen` is a pre-installed program in MacOS that allows for using the terminal as a 'screen' for another device. For example:
	```shell
	screen /dev/tty.usbmodem10001
	```
	*Hint: remember that you can autofill (and cycle between autofills) in Terminal using the* tab *key.*
6. Once you have connected to the `screen`, you should see a message from the MatrixPortal prompting you to reset it or enter the REPL. The REPL is the interactive shell, which will allow you to run CircuitPython directly in a live coding environement on the device. If you do not see this message, or if you want to reset the device, use the key combination `ctrl - D`.
7. `print()` statements from your CircuitPython code will output to this terminal, so if you have a `screen` connection open you can check your code for bugs or see what processes the MatrixPortal is running through.
8. If you use the key combination `ctrl - D` you will preform a **soft reset** on the device. This will allow you to re-run the `code.py` file or enter the REPL while still connected to the `screen`. If you change any of the files on the MatrixPortal drive, the device will also automatically soft-reset. If you press the **reset** button on the device or "power-cycle" it by unplugging the USB-C cable and plugging it back in again you will preform a **hard reset** and will have to re-connect using `screen` again. *Hint: most of the time, even after a hard reset, the `/dev/tty.usbmodem` name will remain the same, so you don't have to discover it again and can just repeat your `screen` command, but this might not always be the case.*
