--- Main ram widget shown on wibar
local watch = require("awful.widget.watch")
local wibox = require("wibox")

local cpu_widget = wibox.widget {
  markup = 'CPU:',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox
}

local total_prev = 0
local idle_prev = 0

watch("cat /proc/stat | grep '^cpu '", 1,
    function(widget, stdout, stderr, exitreason, exitcode)
        local user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice =
        stdout:match('(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s(%d+)%s')

        local total = user + nice + system + idle + iowait + irq + softirq + steal

        local diff_idle = idle - idle_prev
        local diff_total = total - total_prev
        local diff_usage = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10

        total_prev = total
        idle_prev = idle

        widget.markup = string.format("CPU: %.0f%% ", diff_usage)
        -- widget.markup = string.format("CPU: %.1f %", diff_usage)
    end,
    cpu_widget
)

return cpu_widget
