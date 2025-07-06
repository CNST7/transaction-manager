# Backend

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
- `uv` zamiast `venv`
- `SECRET_KEY` nie powinien być na gicie!
- zmienne w `settings.py` ze zmiennych środowiskowych (plik `.env`)
- brakuje volumenu dla bazy danych
- dokumentacja (swagger)
- serwowanie plików statycznych

## docker compose

Zrobiłem na szybko, ale bez postgres'a. :\
Nie wiem czy utworzą się logi w `logs/` w kontenerze. (Możliwe że brakuje `chmod`'a w Dockerfile)
Nie zdążyłem przetesować czy wszystko jest poprawnie skonteneryzowane.
