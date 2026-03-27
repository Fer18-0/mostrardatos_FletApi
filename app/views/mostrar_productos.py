import flet as ft 
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos, Card

def products_view(page:ft.Page) -> ft.Control: 
    rows_data:list[dict[str,Any]]=[]
    total_items=0 
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos.H3) 
    #Encabezados 
    columnas=[ ft.DataColumn(label=ft.Text("Nombre", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Min", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Max", style=Textos.H3)),
    ]

    #Se definen las filas de la tabla 
    # Cada data.append agrega 
    data=[] 
    data.append( 
        ft.DataRow( 
            cells=[ 
                ft.DataCell(ft.Text("nombre1...")), 
                ft.DataCell(ft.Text("cantidad1...")),
                ft.DataCell(ft.Text("ingreso1...")), 
                ft.DataCell(ft.Text("min1...")), 
                ft.DataCell(ft.Text("max1...")), ]))

    #Se crea la tabla con los encabezados(columnas) y los datos de prueba(data) 
    tabla=ft.DataTable( 
        columns=columnas, 
        rows=data, 
        width=900, 
        heading_row_height=60, 
        heading_row_color=Colors.BG, 
        data_row_max_height=60, 
        data_row_min_height=48
        )
    #return tabla

    async def actualizar_data():
        nonlocal rows_data, total_items
        try:
            data=list_products(limit=200, offset=0) # se conecta a transaccines_api_productos para obtener los product
            total_items=int(data.get("total", 0)) 
            #print(total_items)
            total_text.value="Total de productos: "+str(total_items)
            rows_data=data.get("items", []) or []
            actualizar_filas()
        except Exception as ex:
            await show_snackbar(
                page=page,
                title="Error",
                message="Error al cargar productos: " + str(ex),
                bgcolor=Colors.DANGER
            )
    
    def actualizar_filas():
        nuevas_filas=[]
        for p in rows_data: 
            nuevas_filas.append( 
                ft.DataRow( 
                    cells=[ 
                        ft.DataCell(ft.Text(p.get("name", ""))), 
                        ft.DataCell(ft.Text(str(p.get("quantity", "")))),
                        ft.DataCell(ft.Text(p.get("ingreso_date", ""))), 
                        ft.DataCell(ft.Text(str(p.get("min_stock", "")))), 
                        ft.DataCell(ft.Text(str(p.get("max", "")))), ])) 
        tabla.rows=nuevas_filas
        page.update()
    page.run_task(actualizar_data)
    #return tabla
    #se prepara un sistema de columnas para mostrar tanto el total de registros y
    #la tabla y con un mejor formato
    #Cuando se necesita el scroll también se muestra
    btn_nuevo = ft.ElevatedButton(
    "Nuevo producto",
    icon=ft.Icons.ADD,
    on_click=lambda e: print("Click"))
    contenido = ft.Column(
    #Se crea un espacio entra cada elemento 
        spacing=30, 
        #Cuando no caben los elementos se genera el scroll 
        scroll=ft.ScrollMode.AUTO, 
        #Se establecen tanto el total como la tabla para mostrar 
        ######## Se agrega el botón de nuevo registro ######### 
        controls=[btn_nuevo,total_text,ft.Container(content=tabla)]
    )
#Se muestra esa columna
    return contenido



