# Python Notes

## Package Management

Update all modules

```bash
pip3 list -o | cut -f1 -d' ' | tr " " "\n" | awk '{if(NR>=3)print}' | cut -d' ' -f1 | xargs -n1 pip3 install -U
```

## Using venv

*venv* is the built in utility for creating python virtual environments

Create the Virtual Environment. *name* creates a directory for the environment and a reference. The examples below use zoomcamp as the name

```bash
# install delivered utility for virutal environments
sudo apt-install python3.10-venv
# in directory from which you want setup the virtual environment
python -m venv zoomcamp
# activate (from) within the directory
. ./zoomcamp/bin/activate
# activating will return a prompt
(zoomcamp) ✔ ~/repos/crswk/2023-dezoomcamp/week2/work [main|✚ 2…8]
# deactivate the virtual environment
deactivate
# remove (from within directory)
rm -r <name>
```

To add packages use

```bash
pip install -r requirements.txt
```

If you get an error that PIP is not installed use

```bash
python -m ensurepip --upgrade
```

## PostgreSQL

Create a connection directly

```bash
postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{db}'
engine = create_engine(postgresql_url)
```
