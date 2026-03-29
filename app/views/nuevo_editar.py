#app/views/nuevo_editar.py 
import flet as ft 
from app.components.popup import show_popup, close_popup 
def formulario_nuevo_editar_producto(page: ft.Page, on_submit, initial: dict | None = None):
    initial = initial or {}

    titulo = ft.Text("Editar producto" if initial.get("id") else "Nuevo producto")

    name = ft.TextField(label="Nombre", value=initial.get("name", ""))
    quantity = ft.TextField(label="Cantidad", value=str(initial.get("quantity", 0)))
    ingreso_date = ft.TextField(label="Ingreso (YYYY-MM-DD)", value=initial.get("ingreso_date", ""))
    min_stock = ft.TextField(label="Stock mínimo", value=str(initial.get("min_stock", 0)))
    max_stock = ft.TextField(label="Stock máximo", value=str(initial.get("max_stock", 0)))

    def close():
        close_popup(page)

    async def save(_e):
        if not name.value.strip():
            await show_popup(page, "Validación", "El nombre es obligatorio.")
            return
        try:
            data = {
                "name": name.value.strip(),
                "quantity": int(quantity.value),
                "ingreso_date": ingreso_date.value.strip(),
                "min_stock": int(min_stock.value),
                "max_stock": int(max_stock.value),
            }
        except ValueError:
            await show_popup(page, "Validación", "Cantidad y stocks deben ser números enteros.")
            return

        await on_submit(data)
        close()

    btn_cancelar = ft.TextButton("Cancelar", on_click=lambda e: close())
    btn_guardar = ft.Button("Guardar", on_click=lambda e: page.run_task(save, e))

    dlg = ft.AlertDialog(
        modal=False,
        title=titulo,
        content=ft.Container(
            width=420,
            content=ft.Column(
                tight=True,
                controls=[name, quantity, ingreso_date, min_stock, max_stock],
            ),
        ),
        actions=[btn_cancelar, btn_guardar],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_():
        page.show_dialog(dlg)

    return dlg, open_, close