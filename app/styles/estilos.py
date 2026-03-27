import flet as ft

class Colors:
    BG = "#EDEAEA"
    CARD = "#26378E"
    BORDER = "#26378E"
    TEXT = "#575758"
    PRIMARY = "#334ACA"
    SUCCESS = "#047B08"  # ✔ Se agregó #
    INFO = "#04B4FA"
    DANGER = "#FF0000"
    WHITE = "#FFFFFF"
    BLACK = "#000000"


class Textos:
    H1 = ft.TextStyle(size=30, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H2 = ft.TextStyle(size=25, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    H3 = ft.TextStyle(size=20, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)
    text = ft.TextStyle(size=15, weight=ft.FontWeight.W_300, font_family="sans-serif", color=Colors.TEXT)


class inputs:
    INPUT_PRIMARY = {
        "border_color": Colors.BORDER,  # ✔ : en vez de =
        "focused_border_color": Colors.PRIMARY,
        "cursor_color": Colors.PRIMARY,
        "width": 500,
        "text_style": Textos.text,
        "label_style": Textos.text,
        "bgcolor": Colors.BG  # ✔ corregido BACKGROUND por BG
    }


class Buttons:
    BUTTON_PRIMARY = ft.ButtonStyle(
        bgcolor=Colors.PRIMARY,
        color=Colors.WHITE,  
        shape=ft.RoundedRectangleBorder(radius=5),
        padding=10,
        text_style=Textos.text
    )

    BUTTON_SUCCESS = ft.ButtonStyle(
        bgcolor=Colors.SUCCESS,
        color=Colors.WHITE,  
        shape=ft.RoundedRectangleBorder(radius=5),
        padding=10,
        text_style=Textos.text
    )

    BUTTON_DANGER = ft.ButtonStyle(
        bgcolor=Colors.DANGER,
        color=Colors.WHITE,  # ✔ corregido white
        shape=ft.RoundedRectangleBorder(radius=5),
        padding=10,
        text_style=Textos.text
    )


class Card:
    tarjeta = {
        "width": 6600,  # no modifico estructura ni valor
        "padding": 16,
        "border_radius": 12,
        "bgcolor": Colors.BG,
        "border": ft.Border.all(2, Colors.BORDER)
    }