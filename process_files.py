from typing import TypedDict

import polars as pl

STREET_TYPES = [
    "ул",
    "пер",
    "проезд",
    "мкр",
    "тер",
    "СНТ",
    "линия",
]


class ImportData(TypedDict):
    consumer_code: str
    serial_number: int
    address: str
    consumer_name: str
    device_type: str
    tp_number: str


def process_files(sims_file: str, meters_file: str) -> list[ImportData]:
    df_sims = pl.read_excel(sims_file, read_options={"header_row": 1}).slice(0, -1)
    df_meters = pl.read_excel(meters_file, read_options={"header_row": None})

    serial_numbers = df_meters.select(pl.col("column_1")).to_series()

    df_sims = df_sims.with_columns(pl.col("Серийный №").str.to_integer()).filter(
        pl.col("Серийный №").is_in(serial_numbers)
    )

    region_address = "Краснодарский край, Тимашевский р-н, г Тимашевск"
    pattern = r"^(ТП-\d+[А-Яа-я]?)"

    df_sims = df_sims.with_columns(
        [
            pl.col("Адрес").str.extract(pattern, 1).alias("tp_number"),
            pl.col("Адрес")
            .str.replace_all(".", "", literal=True)
            .map_elements(add_house_prefix)
            .str.replace(pattern, region_address),
        ]
    )

    return (
        df_sims.select(
            pl.col(
                [
                    "Код потребителя",
                    "Серийный №",
                    "Адрес",
                    "Наименование точки учета",
                    "Тип устройства",
                    "tp_number",
                ]
            )
        )
        .rename(
            {
                "Код потребителя": "consumer_code",
                "Серийный №": "serial_number",
                "Адрес": "address",
                "Наименование точки учета": "consumer_name",
                "Тип устройства": "device_type",
            }
        )
        .to_dicts()
    )


def add_house_prefix(address: str) -> str:
    addr_parts = [p.strip() for p in address.split(",")]

    numeric_tail = []
    street_index = None
    for i in range(len(addr_parts) - 1, -1, -1):
        addr_part = addr_parts[i]

        if addr_part and addr_part[0].isdigit():
            numeric_tail.append(addr_part)
        else:
            if any(t in addr_part.lower() for t in STREET_TYPES):
                street_index = i
                break
            else:
                break

    if street_index is not None and numeric_tail:
        numeric_tail.reverse()
        combined = "/".join(numeric_tail)
        new_parts = addr_parts[: street_index + 1] + [f"д {combined}"]
        return ", ".join(new_parts)

    if street_index is not None and not numeric_tail:
        return address + ", д Строение"

    return address
