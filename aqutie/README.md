# INSTALLATION

I'm assuming you're using linux to do this. If you're on windows then set up WSL and do it from there.

AQutie requires python 3 (and the python-pip, python-venv packages) and whatever the basic development package group for your distro is to run (base-devel on arch linux) to run. Clone this repository, then either run `install.sh`
or create a virtual environment, and execute 

```
source <your python environment>/bin/activate
python -m pip install -r requirements
```

# USAGE

replace the contents of `token.txt` with your discord bot API token, then execute

```
source env/bin/activate; python bot.py
```

if you used a different python environment directory then modify the above line as needed.

## notice.txt and help.txt

you probably don't need to modify help.txt unless you add new features

you can modify notice.txt to whatever you need it to be; this will also display when someone uses the !help command

# DISCLAIMER

Use gematric software at your own risk -- I claim no responsibility for psychic damage or impairment of sanity caused by the use of AQutie or her inclusion to your discord server

# CONTRIBUTION

I welcome forks of AQutie -- may a thousand gematric discord bots rise.

I will try and respond to pull requests and issues that are opened, but understand this project is basically no longer under active development

# (KNOWN) ISSUES

right now the `!random` command spits out a malformed response. this is not a priority for me to fix.

adding entries that contains newlines breaks the database, and they need to be cleaned up when re-starting AQutie (otherwise she fails when loading in the library file). This is probably the last thing I will devote time to fixing.
