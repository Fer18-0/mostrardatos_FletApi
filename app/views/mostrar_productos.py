import flet as ft 
from typing import Any
from app.services.transacciones_api_productos import list_products, get_product, create_product, update_product, delete_product
from app.components.popup import show_popup, show_popup_auto_close, show_snackbar, confirm_dialog
from app.components.error import ApiError, api_error_to_text
from app.styles.estilos import Colors, Textos, Card
from app.views.nuevo_editar import formulario_nuevo_editar_producto

def products_view(page:ft.Page) -> ft.Control: 
    def inicio_nuevo_producto(_e):
        async def crear_nuevo_producto(data:dict):
            try:
                await create_product(data) 
                await show_snackbar(page, "Éxito", "Producto creado.", bgcolor=Colors.SUCCESS) 
                await actualizar_data() 
            except ApiError as ex: 
                await show_popup(page, "Error", api_error_to_text(ex)) 
            except Exception as ex: 
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(page, on_submit=crear_nuevo_producto, initial=None) 
        open_() 
    def inicio_editar_producto(p: dict[str, Any]):
        async def editar_producto(data: dict):
            try:
                await update_product(p["id"], data)
                close()
                await show_snackbar(page, "Éxito", "Producto actualizado", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

        dlg, open_, close = formulario_nuevo_editar_producto(
            page, on_submit=editar_producto, initial=p
        )
        open_()
    async def borrar_producto(p: dict[str, Any]):
            try:
                await delete_product(p["id"])
                await show_snackbar(page, "Éxito", "Producto eliminado", bgcolor=Colors.SUCCESS)
                await actualizar_data()
            except ApiError as ex:
                await show_popup(page, "Error", api_error_to_text(ex))
            except Exception as ex:
                await show_snackbar(page, "Error", str(ex), bgcolor=Colors.DANGER)

    def inicio_eliminar_producto(p: dict[str, Any]):
            async def tarea():
                await borrar_producto(p)
            page.run_task(tarea)


    btn_nuevo = ft.Button("Nuevo producto",icon=ft.Icons.ADD,on_click=inicio_nuevo_producto)
    rows_data:list[dict[str,Any]]=[]
    total_items=0 
    total_text = ft.Text("Total de productos: (cargando...)", style=Textos.H3) 
    #Encabezados 
    columnas=[ ft.DataColumn(label=ft.Text("Nombre", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Cantidad", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Ingreso", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Min", style=Textos.H3)), 
        ft.DataColumn(label=ft.Text("Max", style=Textos.H3)),
        ft.DataColumn(label=ft.Text("Acciones", style=Textos.H3)), 
        
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
                ft.DataCell(ft.Text("max1...")),
                ft.DataCell(ft.Text("...")), ]))

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
                        ft.DataCell(ft.Text(str(p.get("max_stock", "")))), 
                        ft.DataCell(
                            ft.Row(
                                spacing=10,
                                controls=[
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        on_click=lambda e, p=p: inicio_editar_producto(p)
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        tooltip="Eliminar",
                                        on_click=lambda e, p=p: inicio_eliminar_producto(p)
                                    )
                                ]
                            )
                        ), ])) 
        tabla.rows=nuevas_filas
        page.update()
    page.run_task(actualizar_data)
    #return tabla
    #se prepara un sistema de columnas para mostrar tanto el total de registros y
    #la tabla y con un mejor formato
    #Cuando se necesita el scroll también se muestra

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
    #return contenido
    # Tarjeta
    tarjeta = ft.Container(
        content=contenido,
        **Card.tarjeta
    )
    final = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, -1),
        content=tarjeta
    )
    return final






