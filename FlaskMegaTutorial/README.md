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


## Using HTTPie

```
(venv) $ http GET http://localhost:5000/api/users
(venv) $ http POST http://localhost:5000/api/users username=alice password=dog \
    email=alice@example.com "about_me=Hello, my name is Alice!"
(venv) $ http PUT http://localhost:5000/api/users/2 "about_me=Hi, I am Miguel"

(venv) $ http --auth <username>:<password> POST http://localhost:5000/api/tokens
(venv) $ http GET http://localhost:5000/api/users/1 \
    "Authorization:Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"
```