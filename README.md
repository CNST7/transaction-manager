# Transation Manager

# Stack

- python 3.12
- django 5.2.3
- djangorestframework 3.16.0
- sqlite3

## RUN

Nie zdążyłem zrobić docker-compose, więc żeby uruchomić projekt należy utworzyć virtualne środowisko poprzez `venv` lub użyć `uv` czy `poetry`.

> update - zdążyłem tutaj krótki opis: [docker compose](##docker-compose)

```shell
cd backend
python -m venv venv

pip install -r requirements.txt
```

Ustaw pythonpath, podmień `SCIEŻKA-DO-PROJEKTU` na ścieżkę w której znajduje się projekt

```
export PYTHONPATH=$PYTHONPATH:SCIEŻKA-DO-PROJEKTU/transaction-manager/backend/transactionManager
```

Uruchomienie testów:

```shell
cd backend
pytest
```

Uruchomienie projektu:
przejdź do folderu w którym znaduje się plik `manage.py`

> SCIEŻKA-DO-PROJEKTU/transaction-manager/backend/transactionManager

a następnie uruchom komendy:

```
python manage.py migrate
python manage.py runserver
```

projekt będzie dostępny lokalnie pod adresem: http://127.0.0.1:8000/

## ADR

- Architektura - modularny monolit. Dobre rozwiązanie na start, możliwość rozbicia na mikroserwisy gdy projekt zacznie się bardziej rozbudowywać.

- Użyłem `transaction_id` jako PrimaryKey w modelu `Transactions` w celu uproszczenia problemu. Innym rozwiązaniem byłoby tworzenie samemu id transakcji zamiast korzystać z dostarczonego id.
  Minusem takiego rozwiązania jest to, że przy wgraniu kolejnego pliku csv dane mogą zostać nadpisane jeśli `transaction_id` powtórzy się w drugim pliku.

- Zahardkodowałem `currency_exchange` w celu uproszczenia. Dane te można by pobierać ze zmiennych środowiskowych lub api banku. Wydaje mi sie, że dobrym pomysłem byłoby przechowywanie ich w systemie, żeby wiedzieć jakim kursem zostały przeliczone dane podczas tworzenia raportów.

- Użyłem typu `Decimal` do obliczania oraz przechowywania danych o kwotach

## TODO

- lepsza konteneryzacja
- postresql jako baza danych
- uporządkowanie testów
- validacja csv - użycie `ModelSerializer'a` aby constrainy pochodziły z jednego źródła
- `product_id` i `customer_id` jako klucze obce
- pola lub model na metadane tranzakcji:
  - kto wgrywał plik
  - kiedy
  - powiązane dane tranzacykcyjne
- logowanie
- handlowanie wyjątków
- zadania dodatkowe
- równoległe odpalanie testów
  - pytest-xdist
    > narazie bez, bo dłużej trwa utworzenie procesów niż odpalanie ich szeregowo.
    > Może to być przydatne przy większej ich ilości
- pre-commit
  - narzędzia do statycznej analizy
  - uruchamianie testów
  - lintowanie (black)
- ustawienia produkcyjne
- ci/cd
- rozbicie `requirements.txt` (nie potrzebujemy narzędzi developerskich na produkcji)
- celery, redis (np. do cache'owania raportów)
- `uv` zamiast `venv`'a
- `SECRET_KEY` nie powinien być na gicie!
- zmienne w `settings.py` ze zmiennych środowiskowych (plik `.env`)
- brakuje volumenu dla bazy danych

## docker compose

Zrobiłem na szybko, ale bez postgres'a. :\
Nie wiem czy utworzą się logi w `logs/` w kontenerze. (Możliwe że brakuje `chmod`'a w Dockerfile)
Nie zdążyłem przetesować czy wszystko jest poprawnie skonteneryzowane.

Po uruchomieniu całość powinna działać na http://127.0.0.1/
Bez dockera http://127.0.0.1:8000/
