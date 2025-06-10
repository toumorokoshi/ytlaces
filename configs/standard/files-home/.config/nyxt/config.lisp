; enable vi mode on all buffers
(define-configuration buffer
  ((default-modes
    (pushnew 'nyxt/mode/vi:vi-normal-mode %slot-value%))))

; custom keybindings
(define-configuration input-buffer
  ((override-map
    (let ((map (make-keymap "override-map")))
      (define-key map
        "M-x" 'execute-command
        "M-p" 'switch-buffer
      )
    ))))