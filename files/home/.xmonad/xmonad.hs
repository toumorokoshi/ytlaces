import GHC.IO.Handle
import XMonad
import XMonad.Layout.Spacing
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.SetWMName
import XMonad.Util.CustomKeys
import XMonad.Util.Run
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.ManageDocks
import qualified Data.Map as M

main = do
  staloneTray <- spawnPipe myStaloneTray
  leftBar <- spawnPipe myXmonadBar
  rightBar <- spawnPipe myStatusBar
  xmonad $ docks defaultConfig {
               manageHook = myManageHook
             , workspaces = myWorkspaces
             , modMask = mod4Mask
             , terminal = "termite"
             , borderWidth = 2
             , handleEventHook = docksEventHook
             , layoutHook = avoidStruts $ myLayout
             -- setWMName to LG3D for java app compatability
             -- ewmhDesktopsStartup fixes issues with chrome
             , startupHook = ewmhDesktopsStartup >> setWMName "LG3D"
             , logHook = myLogHook leftBar
             -- keybindings
             , keys = customKeys delkeys inskeys
             , focusFollowsMouse = True
  }

-- status bar about the machine (uses dzen2 + conky)
myStatusBar = "conky -c $HOME/.xmonad/conky_dzen | dzen2 -w '1920' -x '2000' -ta 'r' -dock"
-- status bar about xmonad
myXmonadBar = "dzen2 -x '200' -w '2000' -ta 'l' -dock"
myStaloneTray = "stalonetray"

-- automatically move apps to a specific page
myManageHook = composeAll
    [ className =? "emacs" --> doShift "1:code"
    , className =? "google-chrome" --> doShift "1:chrome"
    , className =? "ChainGame" --> doCenterFloat
    ]

-- workspaces
myWorkspaces = ["1:⌨", "2:W", "3:C", "4:M", "5:X", "6:♻", "7:Z"]

myLogHook :: Handle -> X ()
myLogHook h = dynamicLogWithPP $ defaultPP {
        ppCurrent           =   dzenColor "#ebac54" "#1B1D1E" . pad
      , ppVisible           =   dzenColor "white" "#1B1D1E" . pad
      , ppHidden            =   dzenColor "white" "#1B1D1E" . pad
      , ppHiddenNoWindows   =   dzenColor "#7b7b7b" "#1B1D1E" . pad
      , ppUrgent            =   dzenColor "#ff0000" "#1B1D1E" . pad
      , ppWsSep             =   " "
      , ppSep               =   " | "
      , ppOutput = hPutStrLn h
}


-- screen layout
myLayout = tiled ||| Mirror tiled ||| Full
 where
    -- default tiling algorithm partitions to two panes
    tiled = spacing 5 $ Tall nmaster delta ratio
    -- default number of windows in master pane
    nmaster = 1
    -- Default proportion of screen occuped by master pane
    ratio = 2/3
    -- percent of screen to increment when resizing panes
    delta = 5/100

delkeys :: XConfig l -> [(KeyMask, KeySym)]
delkeys XConfig {modMask = modm} = []

inskeys :: XConfig l -> [((KeyMask, KeySym), X ())]
inskeys conf@(XConfig {modMask = modm}) =
        --take a screenshot of entire display
        [ ((modm, xK_Print ), spawn "scrot screen_%Y-%m-%d-%H-%M-%S.png")

           --take a screenshot of focused window
        , ((modm .|. controlMask, xK_Print ), spawn "scrot window_%Y-%m-%d-%H-%M-%S.png -u")]
