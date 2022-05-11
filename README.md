# Pythonized CC Tweaked (ComputerCraft) API

This fork uses restrictedpython to keep people from hacking you


1. IF YOU ARE HOSTING AS LOCALHOST (not a replit or external server)

   Before you start Minecraft, enable localhost in mod server config

    In case of singleplayer it's located inside your saves folder.
    In case of multiplayer check your server folder.

    Edit `computercraft-server.toml`

    ```toml
    [[http.rules]]
		host = "127.0.0.0/8"
		action = "allow"  # change here deny to allow
    ```

3. Install & start python language server

    Choose one of the following:

    Docker way:

    ```sh
    docker run -it -p 8080:8080 neumond/python-computer-craft
    ```

    Install & run manually:

    ```sh
    pip install cc-secure
    python -m cc-secure.server
    ```

4. Start Minecraft, open up any computer and type:

    ```sh
    wget http://127.0.0.1:8080/ py
    py
    ```
    or, if you are running on a replit or an external server, you can change the adress that is being `wget` ed to the replit or external server's ip or adress
    
    ex.    

    ```sh
    wget http://a_repl.somebody.repl.co py
    py
    ```
    
    or

    ```sh
    wget http://420.696.969.9 py
    py
    ```
    (that ip is not real, instad, replace the ip with the one your server is on)

    Now you have python REPL in computercraft!
    To quit REPL type `exit()` and press enter.

    To run any program:

    ```sh
    py program.py  # relative to current dir
    py /path/to/program.py
    ```

`py` is short Lua program that interacts with the server.
`cc` module contains almost everything *as is* in ComputerCraft documentation:

```python
from cc import disk, os

disk.eject('right')
print(os.getComputerLabel())
```

Opening a file:

```python
from cc import fs

with fs.open('filename', 'r') as f:
    for line in f:
        print(line)
```

Waiting for event (`os.captureEvent` instead `os.pullEvent`):

```python
from cc import os

timer_id = os.startTimer(2)
for e in os.captureEvent('timer'):
    if e[0] == timer_id:
        print('Timer reached')
        break
```

Using modems:

```python
from cc import peripheral

modem = peripheral.wrap('back')
listen_channel = 5
# this automatically opens and closes modem on listen_channel
for msg in modem.receive(listen_channel):
    print(repr(msg))
    if msg.content == 'stop':
        break
    else:
        modem.transmit(msg.reply_channel, listen_channel, msg.content)
```

Using parallel:

```python
from cc import parallel, os

def fn():
    os.sleep(2)
    print('done')

parallel.waitForAll(fn, fn, fn)
```

Importing in-game files as modules:

```python
from cc import import_file

p = import_file('/disk/program.py')  # absolute
m = import_file('lib.py', __file__)  # relative to current file
```

More examples can be found in this repository.
