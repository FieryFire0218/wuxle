# Wuxle

Novel guessing game based on Wordle/Genshindle. Includes a web scraper used for data acquisition.

- Local URL: http://127.0.0.1:5000/

## Project structure

- Root
  - [.gitattributes](.gitattributes)
  - [LICENSE](LICENSE)
  - [README.md](README.md)
- GitHub config
  - [.github/](.github/)
    - [actions/](.github/actions)
    - [logs/](.github/logs)
    - [notifications/](.github/notifications)
    - [tools/](.github/tools)
    - [.gitignore](.github/.gitignore)
    - [trunk.yaml](.github/trunk.yaml)
    - [configs/.markdownlint.yaml](.github/configs/.markdownlint.yaml)
    - [plugins/trunk](.github/plugins/trunk)
- Data
  - [data/complete_data.csv](data/complete_data.csv)
  - [data/novels.json](data/novels.json)
- Docs
  - [docs/aboutdata.txt](docs/aboutdata.txt)
  - [docs/plan.txt](docs/plan.txt)
  - [docs/prettified_ex.html](docs/prettified_ex.html)
  - [docs/prettified_main.html](docs/prettified_main.html)
- Source
  - [src/app.py](src/app.py)
  - [src/compare.py](src/compare.py)
  - [src/csv_to_json.py](src/csv_to_json.py)
  - [src/scraping.py](src/scraping.py)
  - [src/templates/index.html](src/templates/index.html)
  - [src/static/style.css](src/static/style.css)
  - [src/__pycache__/](src/__pycache__/)

## Run locally (VS Code terminal)

- Option A:
  - Set FLASK_APP to [src/app.py](src/app.py) and run Flask:
    - Windows: `set FLASK_APP=src/app.py && python -m flask run`
    - macOS/Linux: `export FLASK_APP=src/app.py && python -m flask run`
- Option B:
  - Run directly if [src/app.py](src/app.py) has an entrypoint: `python src/app.py`

## Notes

- UI plans: see [docs/plan.txt](docs/plan.txt).
- Data notes: see [docs/aboutdata.txt](docs/aboutdata.txt).
- Styles and template live in [src/static/style.css](src/static/style.css) and [src/templates/index.html](src/templates/index.html).

## License

MIT License — see [LICENSE](LICENSE).