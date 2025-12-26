#!/bin/sh
# NOTE: should be sourced
# this is the root init file for bash/zsh
# (maybe fish, if I can figure out how to make it cross-compatible)

. "$HOME"/.ytlaces/rc.d/common

if [ -n "$ZSH_VERSION" ]; then
    . "$HOME"/.ytlaces/rc.d/zsh.sh
fi
