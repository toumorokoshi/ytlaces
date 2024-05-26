#!/usr/bin/env bash
# SCRIPT NO LONGER IN USE.
#
# script to change virtual terminals before and after a suspend/resume
# to try and work around an i915 issue with multiple displays
# see: https://bugzilla.redhat.com/show_bug.cgi?id=1506879
LIGHTDM_VT=7
SECONDARY_VT=2

if [[ "$2" == "suspend" ]]; then
	if [[ "$1" == "pre" ]]; then
		t="pre"
		vt=$SECONDARY_VT
	fi
	if [[ "$1" == "post" ]]; then
		t="post"
		vt=$LIGHTDM_VT
	fi
	logger "$t-suspend: switching to vt$vt"
	chvt "$vt"
fi
