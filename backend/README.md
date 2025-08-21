# Transaction Manager Backend

## Local development workflow

1. **Create and activate a virtual environment**

   ```sh
   python -m venv backend/.venv
   source backend/.venv/bin/activate
   ```

2. **Install dependencies**

   ```sh
   pip install -r backend/requirements.txt -r backend/requirements.dev.txt -r backend/requirements.test.txt
   ```

3. **Set PYTHONPATH**

   ```sh
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/transactionManager
   ```

4. **Apply migrations**

   ```sh
   python backend/transactionManager/manage.py migrate --settings=transactionManager.settings_dev
   ```

5. **Collect static files**

   ```sh
   python backend/transactionManager/manage.py collectstatic --settings=transactionManager.settings_dev --clear
   ```

6. **Run development server**

   ```sh
   python backend/transactionManager/manage.py runserver --settings=transactionManager.settings_dev
   ```

   > or F5 in vscode

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

## Contributing

### pre-commit

This project is using [pre-commit](https://pre-commit.com) tool.
Run `pre-commit install` once.
Now before each commit checks will be automaticly invoked.

If you want to manually run checks use:
`pre-commit run --all-files`

If you want to ignore checks on commit run:
`git commit --no-verify`
which is **_highly discouraged!_**

## VS Code

Configuration is already there.
Just press F5 in vscode with python interpreter set at `backend/.venv/bin/python`
Also test suite is available through the VS Code Python tests tab.

Comment following line in [.vscode/settings.json](../.vscode/settings.json#4) to run integration tests.

```json
// "-m", "not integration",
```
