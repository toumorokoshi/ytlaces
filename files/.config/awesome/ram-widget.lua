--- Main ram widget shown on wibar
local watch = require("awful.widget.watch")
local wibox = require("wibox")

local ram_widget = wibox.widget {
  markup = '',
  align = 'center',
  valign = 'center',
  widget = wibox.widget.textbox
}


local total, used, free, shared, buff_cache, available, total_swap, used_swap, free_swap
local GIGABYTE = 1024 * 1024

watch('bash -c "free | grep -z Mem.*Swap.*"', 1,
    function(widget, stdout, stderr, exitreason, exitcode)
        total, used, free, shared, buff_cache, available, total_swap, used_swap, free_swap =
            stdout:match('(%d+)%s*(%d+)%s*(%d+)%s*(%d+)%s*(%d+)%s*(%d+)%s*Swap:%s*(%d+)%s*(%d+)%s*(%d+)')

        widget.markup = string.format("RAM: %.1f GB / %.1f GB ", used / GIGABYTE, total / GIGABYTE)

    end,
    ram_widget
)

return ram_widget
