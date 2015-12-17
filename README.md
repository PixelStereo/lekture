# lekture
lekture is an osc sequencer

this is a work in progress… don't expect a working version in the following weeks ;-)

Development is done under python 2.7.

##Install
You need to install PyQt5, PyOSC and PyBonjour module

    brew install PyQt5 --with-python --without-python3
    pip install PyOSC

###TO DO LIST
* *project file must be encoded in utf-8 to allow accents and special characters*
* *Implement editing of a cue (JSON strings?) - Dirty Flag + manual save*    
* *Implement auto-save*    
* *Write & implement span library (make span - make prefs - load - etc…)*     
* *Implement OSC-writer for some rewriting rules*     
