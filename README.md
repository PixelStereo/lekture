# lekture
lekture is an osc sequencer

this is a work in progress… don't expect a working version in the following weeks ;-)

Development is done under python 2.7.

##Install
You need to install PyQt5, PyOSC and PyBonjour module

    brew install PyQt5 --with-python --without-python3
    pip install PyOSC
    pip install PyBonjour  --allow-external PyBonjour --allow-unverified PyBonjour

###TO DO LIST
* *Write &implement a device manager (MIDI including MSC / OSC tcp&udp / Minuit tcp&udp / OLA for DMX / SERIAL / PJLINK / VISCA )*    
* *Implement editing of a cue (JSON strings?) - Dirty Flag + manual save*    
* *Implement auto-save*    
* *Implement zero-conf discovery & output table*     
* *Implement Minuit output*     
* *Write & implement lekture library (make lekture - make prefs - load - etc…)*     
* *Implement OSC-writer*     
