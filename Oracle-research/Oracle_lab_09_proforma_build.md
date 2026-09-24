# Lab 09 — Pro-Forma Build: ABG Engine and Known Answer

Run: `python proforma.py`

`proforma.py` is a standard-library-only, five-year ABG training-case model. It uses the
Lab 09 assumptions and FY2025 opening balance sheet exactly as published. The assumptions
in the file are annotated as history, guidance, judgment, or fact. The model computes cash
last and calls `assert_balanced` before it values equity.

## Validation against the Lab 09 known answer

| Line | FY2026E | FY2030E |
|---|---:|---:|
| Revenue | 18,323.0 | 19,678.3 |
| Operating income | 844.2 | 971.4 |
| Net income | 413.6 | 527.5 |
| Free cash flow to equity | 211.4 | 342.3 |
| Cash, year end | 101.8 | 719.8 |
| Assets − liabilities − equity | 0.0 | 0.0 |
| Value per share | $291.75 | $291.75 |

The output reports a 79.8% terminal-value share, which is about 80% as required. For the
swap-and-break test, replacing the computed 2026 `cash` value with `OPENING["cash"]` makes
the balance-sheet check stop with `FY2026E balance-sheet gap: -61.4`.

## Floor-plan explanation and reflection

Floor-plan financing is inventory lending, commonly provided by manufacturers' finance arms
or banks. It rises with dealer inventory, so the model projects it from inventory and includes
the change as a financing source in FCFE; interest is based on the opening balance. Removing
that line leaves inventory funded from cash, which is why cash becomes sharply negative.

Cash is the final line because it is the residual result of the income statement, non-cash
charges, working-capital movements, financing, debt repayment, and buybacks. A negative
61.4 balance-sheet gap means the cash line has been held at opening cash instead of recording
the year's computed change in cash, so the model must refuse valuation.
