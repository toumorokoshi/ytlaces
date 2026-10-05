# OSX configuration

## Additional setup

- [switch to the qwerty-no-option layout installed by this configuration](https://github.com/microsoft/vscode/issues/41024#issuecomment-1615127984):
  1. Open **System Settings** -> **Keyboard** -> **Text Input** -> **Input Sources** -> **Edit...**.
  2. Click the **+** button in the bottom left.
  3. Scroll to the bottom of the left sidebar and select **Others**.
  4. Select **QWERTY no option** and click **Add**.
  5. Select **QWERTY no option** in your menu bar input-source menu, or remove the default **U.S.** layout.- disable macOS auto-switching Spaces, so that focusing an app (e.g. Chrome) in AeroSpace doesn't switch other monitors to workspaces containing that app's windows:
  1. Open **System Settings** -> **Desktop & Dock** -> **Mission Control**.
  2. Turn off **When switching to an application, switch to a Space with open windows for the application**.

  Or run: `defaults write com.apple.dock workspaces-auto-swoosh -bool NO && killall Dock`
