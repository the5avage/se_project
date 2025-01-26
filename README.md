## Steps to run

### 1. Create a virtual environment and activate it:

```shell
python -m venv .venv
source .venv/bin/activate  # On Linux
.venv\Scripts\activate # on Windows
```

### 2. Install dependencies:

```shell
pip install -r requirements.txt
```

### 3. Run tests:

```shell
pytest
```

### 4. Start the Flask app:

```shell
python app.py
```

### 5. Open http://127.0.0.1:5000 in your browser

### 6. Calculate Test Coverate
```shell
coverage run -m pytest
coverage report
```

