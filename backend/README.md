# Transaction Manager Backend

## Local development workflow

1. **Create and activate a virtual environment**

   ```sh
   cd backend
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set PYTHONPATH**

   ```sh
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/transactionManager
   ```

4. **Apply migrations**

   ```sh
   cd backend/transactionManager
   python manage.py migrate --settings=transactionManager.settings_dev
   ```

5. **Run development server**

   ```sh
   python manage.py runserver --settings=transactionManager.settings_dev
   ```

   API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Docker watch

If whole stack is needed you can use docker watch for development

```sh
docker compose up -w
```

or

```sh
docker compose watch
```

## Testing

Run tests:

```sh
pytest backend
```

To skip slow, integration tests:

```sh
pytest backend -m "not integration"
```

## VS Code

Configuration is already there.
Just press F5 in vscode with python interpreter set at `backend/venv/bin/python`
Also test suite is available through the VS Code Python tests tab.

Comment following line in [.vscode/settings.json](../.vscode/settings.json#4) to run integration tests.

```json
// "-m", "not integration",
```
