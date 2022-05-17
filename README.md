# Scrapers
> Scrapers abound!


## Features

## Composition
    | assets
    | modules
        db.py
        scrapers.py
        utils.py
        | tests
            test_db.py
            test_scrapers.py
            test_utils.py
    .editorconfig
    .gitignore
    config.example.ini
    main.py
    requirements.txt

## Tests
```sh
pytest (run all tests)
pytest -s (with i/o logging)
pytest modules/tests/test_db.py (run separate testcase)
pytest -v -m slow (run only decorated tag-mark: @pytest.mark.slow)
pytest -v -m "not slow" (inverse - exclude tests decorated with 'slow')
```
