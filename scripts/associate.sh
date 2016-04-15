#!/bin/sh

defaults write com.apple.LaunchServices LSHandlers -array-add \
"<dict><key>LSHandlerContentTag</key>
<string>lekture</string><key>LSHandlerContentTagClass</key>
<string>public.filename-extension</string><key>LSHandlerRoleAll</key>
<string>org.pixel-stereo.lekture</string></dict>"

/System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -kill -domain local -domain system -domain user