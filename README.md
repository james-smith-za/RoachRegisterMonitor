# Roach Register Monitor documentation

## Usage 
`python RoachMonitor.py`

Fill in the hostname or IP of the ROACH you intend to monitor, browse to the `.fpg` file which is loaded onto the ROACH, click "Connect" and away you go!

Use the long box to filter the registers according to name, and the checkbox on each one to pin the ones you want to the display. When you're done, just remove the text in the box to stick with the ones you want.

When you're editing a register value, it'll turn red to indicate it hasn't been written yet (press Enter or click the button to write it.) The program will strip anything that isn't a digit from the string and write the resulting number to the register.

## Requirements
* PyQt4
* casperfpga (https://github.com/ska-sa/casperfpga/)
* casperfpga's dependencies

## Screenshot
![Screenshot of RoachRegisterMonitor window, filtering registers using the string "coarse".](https://github.com/james-smith-za/RoachRegisterMonitor/blob/master/screenshot.png)

