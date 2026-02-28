HTTP_QUERY_DT_PATTERN = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$"
UNIQUE_DETAIL_PATTERN = (
    r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+already exists"
)
FK_DETAIL_PATTERN = (
    r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+"
    r"is not present in table\s+\"(?P<table>[^\"]+)\""
)

NOT_NULL_PATTERN = (
    r"null value in column\s+\"(?P<column>[^\"]+)\"\s+"
    r"(?:of relation\s+\"(?P<relation>[^\"]+)\"\s+)?"
    r"violates not-null constraint"
)

NOT_FOUND_DETAIL_PATTERN = r"Key\s+\((?P<columns>[^)]+)\)=\((?P<values>[^)]+)\)\s+is not present in table\s+\"(?P<table>[^\"]+)\""