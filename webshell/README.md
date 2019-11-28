# pico webshell

The webshell component is designed to provide all players with a Linux environment
containing useful tools for solving challenges. This helps level the playing field and
reduce barriers to entry in cases such as:

- Devices without the ability to access a shell or install software (e.g. school Chromebooks, iOS devices)
- Players who only have access to a Windows or macOS environment, but would like to run Linux tools
- Beginners who are not prepared to use a command line environment on their own device

The **[dispatcher](./dispatcher.Dockerfile)** container provides an [xterm.js](https://xtermjs.org/) terminal over HTTP/WS on port 8080 (typically proxied by the UI.)
When a player visits this page, a **[toolbox](./toolbox.Dockerfile)** container is spawned for them,
containing an interactive Linux shell and a variety of useful command-line tools.

Dispatcher containers are stateless and may be horizontally scaled and load-balanced as needed, though established websocket connections
must remain pinned to the originating container.

Logins to the toolbox container are authenticated against the **[pico API](../api)**,
which additionally allocates a Linux UID for each user.

Since each user will have a consistent UID across multiple spawned toolboxes, it is possible
to mount a shared volume over `/home` to persist users' home directories.
