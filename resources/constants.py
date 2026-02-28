DATETIME_FMT = "%Y-%m-%dT%H:%M:%S"

OFFSET_FROM_DEFAULT = 0
LIMIT_FROM_DEFAULT = 1
LIMIT_TO_DEFAULT = 1000

"""
Константы для выгрузки отчёта
"""
FILENAME_TEMPLATE = "todos_{id}.xlsx"
REPORT_CHUNK_SIZE: int = 1024
REPORT_EXPORT_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
CONTENT_DISPOSITION_TEMPLATE = 'attachment; filename="{filename}"'
CONTENT_DISPOSITION_HEADER = "Content-Disposition"
REPORT_TITLE = "Todo Tasks"
REPORT_HEADERS = ("ID", "Название", "Описание", "Дата создания", "Дата изменения")
HEADER_FILL_KWARGS = {
    "start_color": "366092",
    "end_color": "366092",
    "fill_type": "solid",
}
HEADER_ALIGNMENT = {
    "horizontal": "center",
    "vertical": "center",
}
HEADER_FONT = {
    "bold": True,
    "color": "FFFFFF",
}
HEADERS_ROW_NUM: int = 1
HEADERS_COL_NUM: int = 1
COLUMNS_WIDTH: int = 40
BODY_ROW_NUM: int = 2
REPORT_DATETIME_FORMAT = "%d.%m.%Y %H:%M"

"""
Настройки Security
"""
TOKEN_ENCODING = "utf-8"
TOKEN_TYPE = "bearer"
