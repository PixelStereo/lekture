#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains a project manager for writing inter/multi-media scenario.

===============================================================================
pyprojekt
===============================================================================

First, you create a project. In this project you can add Scenario and Outputs.

A scenario contains an ordered list of Events.

A scenario outputs its event to a choosen Output.

If an output is given for an event, it will overwrite the scenario output for this event.

-------------------------------------------------------------------------------

    Copyright (c) 2015 Pixel Stereo

-------------------------------------------------------------------------------
Changelog:
-------------------------------------------------------------------------------
- v0.2.0  - 22 Dec. 2015
    ADD new Class Design. Project / Scenario / Event
    FIX outputs
    
- v0.1.0  - 18 Dec. 2015
    First draft"""