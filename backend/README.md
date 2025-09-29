# Transaction Manager Backend

## Local development workflow

1. **Install dependencies**

   ```sh
   uv sync --directory backend --locked
   ```

2. **Set PYTHONPATH**

   ```sh
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend/transactionManager
   ```

3. **PC restart might be required at this point**

4. **Apply migrations**

   > assuming venv created by `uv sync` is active

   ```sh
   ./backend/transactionManager/manage.py migrate --settings=transactionManager.settings_dev
   ```

5. **Collect static files**

   > assuming venv created by `uv sync` is active

   ```sh
   ./backend/transactionManager/manage.py collectstatic --settings=transactionManager.settings_dev --no-input --clear
   ```

6. **Run development server**

   > assuming venv created by `uv sync` is active

   ```sh
   ./backend/transactionManager/manage.py runserver --settings=transactionManager.settings_dev
   ```

   > or F5 in vscode

   API will be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Docker watch

If whole stack is needed use docker watch for development

```sh
docker compose watch
```

## Testing

> assuming venv created by `uv sync` is active

Run all tests:

```sh
pytest backend
```

To skip slow, integration tests:

> Runs only unit tests

```sh
pytest backend -m "not integration"
```

To run only integration tests:

```sh
pytest backend -m "integration"
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

Configuration is already here. Press `F5` in vscode to run development server.
Also test suite is available through the VS Code testing tab.

**To make integration tests visible in testing tab** comment out following line in [.vscode/settings.json](../.vscode/settings.json#4).

```json
// "-m", "not integration",
```
