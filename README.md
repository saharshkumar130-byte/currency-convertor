# Modular Currency Converter

## Overview
A modular Python command-line application that converts between USD, EUR and CAD,
lets you manage exchange rates, and keeps a history of conversions with a report.
Built for the VITyarthi *Build Your Own Project* evaluation.

## Features
- Convert amounts between USD / EUR / CAD with full input validation
- View, update and reset exchange rates (persisted in `data/rates.json`)
- Conversion history: list, delete, clear (persisted in `data/history.json`)
- Analytics report: total conversions, most-used pair, totals per currency
- Rotating log file (`logs/app.log`) and custom exceptions for clear errors
- 21 unit tests

## Technologies
Python 3.8+ (standard library only: `json`, `logging`, `dataclasses`, `unittest`), Git.

## Project Structure
```
currency_converter/
├── main.py                 # entry point
├── converter/
│   ├── config.py           # paths, currencies, default rates
│   ├── exceptions.py       # custom exception classes
│   ├── logger.py           # logging setup
│   ├── validators.py       # input validation
│   ├── rates.py            # Module 2: rate management
│   ├── converter.py        # Module 1: conversion logic
│   ├── history.py          # Module 3: history + analytics
│   └── cli.py              # menu-driven interface
├── tests/                  # unit tests
├── data/  logs/  docs/
├── README.md  statement.md
```

## Install & Run
```bash
git clone <your-repo-url>
cd currency_converter
python main.py
```
No packages to install.

## Testing
```bash
python -m unittest discover -s tests -t .
```

## Sample Session
```
===== Currency Converter =====
1. Convert currency ...
Choose an option: 1
Enter the amount: 100
Source currency (USD/EUR/CAD): usd
Target currency (USD/EUR/CAD): eur
100 USD is equal to 85.00 EUR
```
*(Add your own screenshots here.)*

## Documentation
Design diagrams and non-functional requirements: see [`docs/architecture.md`](docs/architecture.md).
Problem statement: [`statement.md`](statement.md).
