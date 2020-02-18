# iterm2-scripts
Scripts for iTerm2

## Profile switcher

Will automatically switch profiles based on **any** iTerm2 variable (rather than the limited `user@host/path?jobName`.

### Installation

1. Checkout and link the profile switcher:
      ```bash
      git clone [THIS_REPO] [REPO_DIRECTORY]
      cd $HOME/Library/ApplicationSupport/iTerm2
      mkdir -p Scripts/AutoLaunch
      cd Scripts/AutoLaunch
      ln -s [REPO_DIRECTORY]/AutoLaunch/profile.py
      ```
1. Amend the config in `[REPO_DIRECTORY]/AutoLaunch/profile.py`
1. Now launch the script from the menu: Scripts -> AutoLaunch -> profile.py

### Example: changing profile when OS turns on "dark mode"

1. Create a profile with the title "Light" and give it an appropriate theme
1. Pipe dark mode in to user defined variable:
      ```bash
      # ~/.bash_profile
      function iterm2_print_user_vars() {
        DARK_MODE=$(defaults read -g AppleInterfaceStyle 2>/dev/null)
        UI_MODE="light"
        
        if [[ $DARK_MODE == "Dark" ]]; then
          UI_MODE="dark"
        fi

        iterm2_set_user_var ui_mode "$UI_MODE"
      }
      ```
1. Amend config in `[REPO_DIRECTORY]/AutoLaunch/profile.py`:
      ```python
      profile_maps = {"user.ui_mode": {"light": "Light",
                                       "dark": "Default"}}
      ```
1. Reload script by turning it off/on from the menu: Scripts -> AutoLaunch -> profile.py
