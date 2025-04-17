from dataclasses import field
from typing import Dict, List, Optional
import fitz
from pathlib import Path
import random
from faker import Faker
from datetime import datetime

fake = Faker()

# Your form choices
US_STATES = [state[0] for state in [
    ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
    ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
    ('DE', 'Delaware'), ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'),
    ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'),
    ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
    ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'),
    ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
    ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
    ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'),
    ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'),
    ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
    ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
    ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'), ('WY', 'Wyoming'),
]]

DESCRIPTION_CHOICES = ['SEMI TRUCK', 'STRAIGHT TRUCK', 'TRUCK', 'TRAILER']

name_pdf_template_map = {
    1: "basa_1.pdf",
    2: "basa_2.pdf",
    3: "basa_3.pdf",
    4: "basa_4.pdf",
    5: "basa_5.pdf",
}

def generate_random_vin():
    # Generate a basic fake VIN (17 uppercase letters and numbers, no I, O, Q)
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"
    return ''.join(random.choices(chars, k=17))

def generate_track_invoice_data(num_invoices=1):
    return {
        "company": {
            "company_name": fake.company(),
            "address": fake.street_address().replace("\n", " "),
            "city": fake.city(),
            "state": random.choice(US_STATES),
            "zip": fake.zipcode()
        },
        "invoices": [
            {
                "description": random.choice(DESCRIPTION_CHOICES),
                "make": fake.company(),
                "model": fake.word().upper(),
                "VIN": generate_random_vin(),
                "year": str(random.randint(1990, datetime.now().year)),
                "mileage": random.randint(0, 500_000),
                "total_sum": round(random.uniform(1000, 100000), 2),
                "fee": round(random.uniform(100, 1000), 2)
            } for _ in range(num_invoices)
        ]
    }

coordinates = {
    "default_invoice": {
        0: {
            # company info
            "invoice_number": (70, 100),
            "company_name": (43, 160),
            "address": (43, 175),
            "city_state_zip": (43, 190),
            "date": (425, 160),
            # invoice_info
            "description_1": (13, 368),
            "make_1": (110, 368),
            "model_1": (192, 368),
            "VIN_1": (262, 368),
            "year_1": (410, 368),
            "mileage_1": (453, 368),
            "total_sum_1": (530, 368),

            "description_2": (13, 394),
            "make_2": (110, 394),
            "model_2": (192, 394),
            "VIN_2": (262, 394),
            "year_2": (410, 394),
            "mileage_2": (453, 394),
            "total_sum_2": (530, 394),

            "description_3": (13, 418),
            "make_3": (110, 418),
            "model_3": (192, 418),
            "VIN_3": (262, 418),
            "year_3": (410, 418),
            "mileage_3": (453, 418),
            "total_sum_3": (530, 418),

            "description_4": (13, 442),
            "make_4": (110, 442),
            "model_4": (192, 442),
            "VIN_4": (262, 442),
            "year_4": (410, 442),
            "mileage_4": (453, 442),
            "total_sum_4": (530, 442),

            "description_5": (13, 466),
            "make_5": (110, 466),
            "model_5": (192, 466),
            "VIN_5": (262, 466),
            "year_5": (410, 466),
            "mileage_5": (453, 466),
            "total_sum_5": (530, 466),

            "total_fee": (515, 520),
            "total_result": (510, 550),
        }
    }
}


def aggregate_invoices(data):
    aggregated = {}

    company_info = data["company"]
    invoices = data["invoices"]

    aggregated = company_info
    total_fee = 0
    total_result = 0

    for i, invoice in enumerate(invoices, start=1):
        for key, value in invoice.items():
            if key == "fee":
                total_fee += value
            elif key == "total_sum":
                total_result += value
                value = f"{value:,.2f}"

            aggregated[f"{key}_{i}"] = value

    aggregated["total_fee"] = f"{total_fee:,.2f}"
    aggregated["total_result"] = f"{total_result:,.2f}"

    return aggregated

def fill_pdf_by_coordinates(
    template_path: Path,
    save_file_path: Path,
    data: Dict,
    coordinates: Dict,
    font_size: int = 12,
) -> None:
    pdf_document = fitz.open(template_path)

    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]

        page_coordinates = coordinates.get(page_num, None)
        if not page_coordinates:
            break

        full_data = aggregate_invoices(data)
        full_data["invoice_number"] = f"{datetime.now().strftime("%Y%d%m")}001"
        full_data["city_state_zip"] = f"{full_data.get("city", "")}, {full_data.get("state", "")} {full_data.get("zip", "")}"
        full_data["date"] = datetime.now().strftime("%m.%d.%Y")

        index = 0
        for key, value in full_data.items():
            if key == "invoice_number":
                font_size = 19
                font_color = (1, 1, 1)
            elif key == "company_name" or key == "address" or key == "city_state_zip" or key == "date":
                font_size = 12
                font_color = (1, 1, 1)
            else:
                font_size = 8
                font_color = (0.1804, 0.1843, 0.3725)

            value = str(value)
            field_coordinates = page_coordinates.get(key, None)
            if len(data["invoices"]) == 1:
                if key in ["description_1", "make_1","model_1", "VIN_1","year_1","mileage_1", "total_sum_1"]:
                    field_coordinates = (field_coordinates[0], 385)
                elif key in ["total_fee", "total_result"]:
                    field_coordinates = (field_coordinates[0] + 10, field_coordinates[1])


            if not field_coordinates:
                continue

            if isinstance(field_coordinates, list):
                for fc in field_coordinates:
                    page.insert_text(fc, value.strip(), fontsize=font_size, color=font_color) # type: ignore
            else:
                page.insert_text(field_coordinates, value.strip(), fontsize=font_size, color=font_color) # type: ignore

            index += 1

    pdf_document.save(save_file_path)


if __name__ == "__main__":
    for num in range(1, 6):
        data = generate_track_invoice_data(num)
        fill_pdf_by_coordinates(
            Path(__file__).resolve().parent.parent / "applications" / name_pdf_template_map[num],
            Path(f"basa_{num}.pdf"),
            data,
            coordinates["default_invoice"],
        )
