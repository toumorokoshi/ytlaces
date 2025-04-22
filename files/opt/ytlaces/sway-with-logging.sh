#!/usr/bin/env bash
exec > ~/var/log/sway.log
exec sway > ~/.cache/sway.log 2>&1