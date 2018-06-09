## Virtualenv workflow

### Create virtual env

#### python3.4 and above
```bash
python3 -m venv venv
```

#### python versions lower than 3.4
First install the tool called **virtualenv**.
Then:
```bash
virtualenv venv
```

### Activate virtualenv
```bash
source venv/bin/activate
```

### Deactivate virtualenv
```bash
deactivate
```

### Tips
Add to **venv/bin/activate the following line at the top

```
export FLASK_APP=microbolog.py
```

This way anytime you activate the virtual env you'll already get set this
env variable needed for flask
