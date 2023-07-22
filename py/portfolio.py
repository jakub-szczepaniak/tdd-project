import functools
import operator

from money import Money


class Portfolio:
    def __init__(self):
        self.moneys = []

    def add(self, *moneys):
        self.moneys.extend(moneys)

    def evaluate(self, bank, currency):
        total = 0.0
        failures = []

        for m in self.moneys:
            try:
                total += bank.convert(m, currency).amount
            except Exception as e:
                failures.append(e)

        if len(failures) == 0:
            return Money(total, currency)

        failure_message = ",".join(f.args[0] for f in failures)
        raise Exception(f"Missing exchange rate(s):[{failure_message}]")

    def __convert(self, aMoney, aCurrency):
        exchangeRates = {"EUR->USD": 1.2, "USD->KRW": 1100}

        if aMoney.currency == aCurrency:
            return aMoney.amount
        else:
            key = f"{aMoney.currency}->{aCurrency}"
            return aMoney.amount * exchangeRates[key]
