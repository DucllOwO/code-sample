from databases.interfaces import Record


def convert_record_to_dict(
    record: list[Record] | Record | None,
) -> list[dict] | dict | None:
    def convert(record: Record | None) -> dict | None:
        if not record:
            return None
        return dict(record._mapping)

    if isinstance(record, list):
        return [convert(row) for row in record]
    return convert(record)
