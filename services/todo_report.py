import io
from typing import AsyncGenerator, List
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

from models.todo_task import ToDoTask


class TodoReportService:
    CHUNK_SIZE = 8192
    
    def _create_excel_report_buffer(self, todos: List[ToDoTask]) -> io.BytesIO:
        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Todo Tasks"

        headers = ["ID", "Название", "Описание", "Дата создания", "Дата изменения"]

        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")

        for col_num, header in enumerate(headers, 1):
            cell = worksheet.cell(row=1, column=col_num)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment

        for row_num, todo in enumerate(todos, 2):
            worksheet.cell(row=row_num, column=1, value=str(todo.id))
            worksheet.cell(row=row_num, column=2, value=todo.title)
            worksheet.cell(row=row_num, column=3, value=todo.description or "")
            worksheet.cell(
                row=row_num, column=4,
                value=todo.created_at.strftime("%d.%m.%Y %H:%M") if todo.created_at else "",
            )
            worksheet.cell(
                row=row_num, column=5,
                value=todo.updated_at.strftime("%d.%m.%Y %H:%M") if todo.updated_at else "",
            )

        buf = io.BytesIO()
        workbook.save(buf)
        buf.seek(0)
        return buf

    async def get_report_chunks(
        self,
        todos: List[ToDoTask],
        chunk_size: int = CHUNK_SIZE,
    ) -> AsyncGenerator[bytes, None]:
        buf: io.BytesIO = self._create_excel_report_buffer(todos=todos)

        while chunk := buf.read(chunk_size):
            yield chunk

        buf.close()