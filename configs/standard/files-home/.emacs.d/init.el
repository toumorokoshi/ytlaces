(add-to-list 'package-archives '("melpa" . "https://melpa.org/packages/") t)
; customized keybindings
(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-enabled-themes '(tango-dark))
 '(package-selected-packages
   '(protobuf-mode company lsp-ui lsp-mode go-mode counsel ivy projectile markdown-mode yaml-mode vertico)))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 )
(setq viper-mode t)
(require 'viper)
(require 'yaml-mode)
(require 'ivy)
(advice-add 'split-window-right :after 'balance-windows)
(advice-add 'split-window-down :after 'balance-windows)
(advice-add 'delete-window ':after 'balance-windows)
; customized keybindings
(global-unset-key (kbd "M-c"))
(global-unset-key (kbd "M-x"))
(keymap-global-set "M-c" 'execute-extended-command)
(keymap-global-set "M-x g" 'avy-goto-char-2)
(keymap-global-set "M-s" 'save-buffer)
(keymap-global-set "M-x h" 'windmove-left)
(keymap-global-set "M-x j" 'windmove-down)
(keymap-global-set "M-x k" 'windmove-up)
(keymap-global-set "M-x l" 'windmove-right)
(keymap-global-set "M-x 0" 'delete-window)
(keymap-global-set "M-x 2" 'split-window-below)
(keymap-global-set "M-x 3" 'split-window-right)
(keymap-global-set "M-x t" 'term)
(keymap-global-set "M-n" 'mc/mark-next-lines)
; project-level keybindings
(keymap-global-set "M-x p f" 'project-find-file)
; (setq ivy-use-virtual-buffers t)
;(setq enable-recursive-minibuffers t)
; configuring projectile
;; configure vertico
(vertico-mode)
(desktop-save-mode)
(require 'multiple-cursors)
; lsp-mode
(require 'lsp-mode)
(add-hook 'go-mode-hook #'lsp)
(company-mode)
(lsp-mode)

; custom keybindings
(defun yft-switch-project (dir)
  "switch to a current emacs project"
  (interactive (list (read-directory-name "Add to known projects: ")))
  (projectile-add-known-project dir)
  (projectile-switch-project dir)
  (desktop-change-dir dir)
  (find-file dir)
)
