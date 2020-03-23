### Manipulate the database

```bash
# Seed the database
python3 src/seed.py seed
# Droping the database ~ rm db/app.db
python3 src/seed.py drop
# All tuples in the database
python3 src/seed.py select
# Some info about the tables
python3 src/seed.py desc
```


### Execute the app

```
python3 za_warudo
# TODO change to app/ ?
```


### Execute the tests

```
export PYTHONPATH='za_warudo/'
python3 tests/TestListMethods.py
```

### Requirements
```bash
pip install -r requirements.txt
```

### Documentation

Generated by pdoc3. Available [here](https://poulposaure.gitlab.io/poo/za_warudo/)

## UI fix

In `~/.local/lib/python3.5/site-packages/ttkthemes/png/breeze/breeze.tcl`,
add the following lines:

```tcl
        # Treeview
        ttk::style configure Treeview -background white
        ttk::style configure Treeview.Item -padding {2 0 0 0}
        ttk::style map Treeview \
            -background [list selected $colors(-selectbg)] \
            -foreground [list selected $colors(-selectfg)]
```

### TODO

- unit testing tkinter



