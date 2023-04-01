# jupyter reference

Start a [notebook](http://localhost:8888/tree)

```bash
# start notebook
jupyter notebook --no-browser </dev/null &>/dev/null & disown
```

```bash
# list running notebookk
jupyter notebook list
# shut down notebook
jupyter notebook stop
# convert notebook to python script
jupyter nbconvert --to=script upload-data.ipynb
```