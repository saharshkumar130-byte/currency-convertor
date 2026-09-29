# Problem Statement

## Problem
Converting money between currencies by hand is error-prone, and simple scripts
usually offer no input validation, no way to update rates, and no record of past conversions.

## Scope
A command-line application that converts between USD, EUR and CAD using
locally stored exchange rates, lets the user maintain those rates, and keeps a
history of conversions with a summary report. Live internet rates are out of scope.

## Target Users
- Students and travellers who need quick, reliable conversions
- Small businesses working with a few fixed currencies
- Learners studying modular Python design

## High-Level Features
1. **Conversion module** - validated amount/currency input, accurate conversion
2. **Rate management module** - view, update, reset and persist exchange rates
3. **History & reporting module** - store, list, delete conversions and view analytics
4. Logging, custom error handling and unit tests
