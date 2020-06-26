# Pythonized ComputerCraft API

1. Enable localhost in mod server config

    In case of singleplayer it's located inside your saves folder.
    In case of multiplayer check your server folder.

    Edit `computercraft-server.toml`

    ```toml
    [[http.rules]]
		host = "127.0.0.0/8"
		action = "allow"  # change here deny to allow
    ```

2. Create module named `examplemod.py`:

    ```python
    async def hello(api):
        await api.print('Hello world!')
    ```

3. Start a server:

    ```bash
    python -m computercraft.server examplemod
    ```

4. In minecraft, open up any computer and type:

    ```bash
    wget http://127.0.0.1:8080/ py
    py hello
    ```

`py` is short Lua program that interacts with the server.
Argument is the name of coroutine inside the module.
`api` object contains almost everything *as is* in ComputerCraft documentation:

```python
async def program(api):
    await api.disk.eject('right')
    await api.print(await api.os.getComputerLabel())
    # ...
```

Using python coroutines allows launching commands in parallel, effectively replacing `parallel` API:

```python
async def program(api):
    # Since os.sleep is mostly waiting for events, it doesn't block execution of parallel threads
    # and this snippet takes approximately 2 seconds to complete.
    await asyncio.gather(api.os.sleep(2), api.os.sleep(2))
```
