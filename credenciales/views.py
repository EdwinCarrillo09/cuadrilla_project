from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Credencial
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

def registro_credenciales(request):
    """Maneja el formulario de registro y el listado en la página web."""
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        apellidos_nombres = request.POST.get('apellidos_nombres').upper()
        turno = request.POST.get('turno')
        
        # Guardar permanentemente en la base de datos
        Credencial.objects.create(
            cedula=cedula,
            apellidos_nombres=apellidos_nombres,
            turno=turno
        )
        return redirect('registro_credenciales')

    registros = Credencial.objects.all()
    return render(request, 'credenciales/registro.html', {'registros': registros})

def exportar_excel(request):
    """Genera el archivo binario Excel replicando el formato de la captura."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Hoja2 (2)"
    ws.views.sheetView[0].showGridLines = True # Asegura que se vean las líneas de las celdas

    # Definir tipografía y estilos
    font_titulo = Font(name='Aptos Narrow', size=16, bold=True)
    font_cabecera = Font(name='Aptos Narrow', size=11, bold=True, color="000000")
    font_celda = Font(name='Aptos Narrow', size=11)
    
    # Color verde oliva de la captura (#76933C)
    fill_cabecera = PatternFill(start_color="76933C", end_color="76933C", fill_type="solid")
    
    border_fino = Border(
        left=Side(style='thin', color='B0B0B0'), right=Side(style='thin', color='B0B0B0'),
        top=Side(style='thin', color='B0B0B0'), bottom=Side(style='thin', color='B0B0B0')
    )

    # Escribir títulos en las filas correspondientes
    ws['B2'] = "LISTADO CUADRILLA CINDY"
    ws['B2'].font = font_titulo
    ws['B4'] = "ANCHUNDIA"
    ws['B4'].font = font_titulo

    # Cabeceras de la tabla en la Fila 7
    cabeceras = ["", "Cédula", "APELLIDOS Y NOMBRES", "Turno"]
    for col_num, cabecera in enumerate(cabeceras, start=1):
        cell = ws.cell(row=7, column=col_num, value="" if col_num == 1 else cabecera)
        cell.font = font_cabecera
        cell.fill = fill_cabecera
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border_fino

    # Llenar la información desde la base de datos desde la Fila 8 en adelante
    registros = Credencial.objects.all()
    for index, reg in enumerate(registros, start=1):
        row_num = 7 + index
        c_num = ws.cell(row=row_num, column=1, value=index)
        c_ced = ws.cell(row=row_num, column=2, value=reg.cedula)
        c_nom = ws.cell(row=row_num, column=3, value=reg.apellidos_nombres)
        c_tur = ws.cell(row=row_num, column=4, value=reg.turno)

        for cell in [c_num, c_ced, c_nom, c_tur]:
            cell.font = font_celda
            cell.border = border_fino
            cell.alignment = Alignment(horizontal="center" if cell in [c_num, c_ced] else "left")

    # Anchos de columna perfectos
    ws.column_dimensions['A'].width = 6
    ws.column_dimensions['B'].width = 18
    ws.column_dimensions['C'].width = 45
    ws.column_dimensions['D'].width = 25

    # Preparar descarga del archivo
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="LISTADO_CUADRILLA_CINDY_ANCHUNDIA.xlsx"'
    wb.save(response)
    return response

    # Agregar esto al final de credenciales/views.py

def limpiar_registros(request):
    """Elimina todos los registros de la base de datos para empezar una nueva lista."""
    if request.method == 'POST':
        Credencial.objects.all().delete() # Borra de golpe todos los registros
    return redirect('registro_credenciales')