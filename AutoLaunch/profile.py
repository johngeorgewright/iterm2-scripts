import asyncio
import iterm2

"""
This is where you put your configuration.

Edit this hash once you've set up your iTerm2 Profiles and created any 
[user-defined](https://iterm2.com/documentation-scripting-fundamentals.html#setting-user-defined-variables)
[variables](https://iterm2.com/documentation-variables.html).

```
[variable_name]: {
    [variable_value]: [profile_name]
}
```

The order of variable names matter. The earlier the name
the higher in precence. If there is no value, this will continue
to the next variable (and so on) until a value is found.
"""
profile_maps = {
    "user.aws_profile_ui_mode": {"labl-dark": "Labl Dark",
                                 "labl-light": "Labl Light"},
    "user.aws_profile": {"threads-production": "Production"},
    "user.ui_mode": {"dark": "Default",
                     "light": "Light"}
}


async def SwitchProfile(connection, session, profile_name):
    app = await iterm2.async_get_app(connection)
    print("Switching profile to: " + profile_name)
    partialProfiles = await iterm2.PartialProfile.async_query(connection)
    for partial in partialProfiles:
        if partial.name == profile_name:
            full = await partial.async_get_full_profile()
            await session.async_set_profile(full)


def AddToStack(stack, stack_index, profile_name, profile_map):
    if profile_name in profile_map:
        stack[stack_index] = profile_map[profile_name]
    else:
        stack[stack_index] = None


async def SelectProfile(connection, session, stack):
    for profile_name in stack:
        if profile_name is not None:
            await SwitchProfile(connection, session, profile_name)
            break


async def MonitorSession(connection, session, stack, stack_index, variable, profile_map):
    profile_name = await session.async_get_variable(variable)
    AddToStack(stack, stack_index, profile_name, profile_map)
    await SelectProfile(connection, session, stack)

    async with iterm2.VariableMonitor(
            connection,
            iterm2.VariableScopes.SESSION,
            variable,
            session.session_id) as mon:
        while True:
            profile_name = await mon.async_get()
            AddToStack(stack, stack_index, profile_name, profile_map)
            print("Profile stack has been updated")
            print(stack)
            await SelectProfile(connection, session, stack)


def CreateTasks(connection, session):
    stack = list(map(lambda _x: None, profile_maps)) + ['Default']
    for i, (variable, profile_map) in enumerate(profile_maps.items()):
        asyncio.create_task(MonitorSession(
            connection, session, stack, i, variable, profile_map))


async def main(connection):
    app = await iterm2.async_get_app(connection)

    for window in app.terminal_windows:
        for tab in window.tabs:
            for session in tab.sessions:
                CreateTasks(connection, session)

    async with iterm2.NewSessionMonitor(connection) as mon:
        while True:
            session_id = await mon.async_get()
            session = app.get_session_by_id(session_id)
            CreateTasks(connection, session)

iterm2.run_forever(main)
