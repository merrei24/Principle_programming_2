import re
import json
from decimal import Decimal


class ReceiptParser:
    def __init__(self, text):
        self.text = text

    # ----------------------------
    # Extract product names
    # ----------------------------
    def extract_products(self):
        product_pattern = r'\d+\.\n(.+?)(?=\n\d+,\d{3}\s+x|\n\d+,\d{3}|\nСтоимость)'
        matches = re.findall(product_pattern, self.text, re.DOTALL)

        products = []
        for item in matches:
            clean = " ".join(item.split())
            products.append(clean)

        return products

    # ----------------------------
    # Extract all prices
    # ----------------------------
    def extract_prices(self):
        price_pattern = r'\d[\d\s]*,\d{2}'
        prices = re.findall(price_pattern, self.text)

        cleaned = []
        for p in prices:
            p = p.replace(" ", "")
            p = p.replace(",", ".")
            cleaned.append(str(Decimal(p)))

        return cleaned

    # ----------------------------
    # Extract total amount
    # ----------------------------
    def extract_total(self):
        total_pattern = r'ИТОГО:\s*\n?([\d\s]+,\d{2})'
        match = re.search(total_pattern, self.text)

        if match:
            total = match.group(1).replace(" ", "").replace(",", ".")
            return str(Decimal(total))
        return None

    # ----------------------------
    # Extract date and time
    # ----------------------------
    def extract_datetime(self):
        dt_pattern = r'Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})'
        match = re.search(dt_pattern, self.text)

        if match:
            return {
                "date": match.group(1),
                "time": match.group(2)
            }
        return {"date": None, "time": None}

    # ----------------------------
    # Extract payment method
    # ----------------------------
    def extract_payment_method(self):
        if "Банковская карта" in self.text:
            return "Bank Card"
        if "Наличные" in self.text:
            return "Cash"
        return None

    # ----------------------------
    # Structured JSON
    # ----------------------------
    def parse(self):
        return {
            "products": self.extract_products(),
            "prices": self.extract_prices(),
            "total_amount": self.extract_total(),
            "date": self.extract_datetime()["date"],
            "time": self.extract_datetime()["time"],
            "payment_method": self.extract_payment_method()
        }


if __name__ == "__main__":
    with open("raw.txt", "r", encoding="utf-8") as f:
        receipt_text = f.read()

    parser = ReceiptParser(receipt_text)
    data = parser.parse()

    print(json.dumps(data, indent=4, ensure_ascii=False))