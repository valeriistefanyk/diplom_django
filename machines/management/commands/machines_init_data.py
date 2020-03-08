def read_data_xls(*argv):
    import xlrd
    import datetime
    loc = ("static_files/other_data/machines_bd.xls") 
  
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    
    row_array = []
    for i in range(5, sheet.nrows - 1):
        row_array.append(sheet.row_values(i))
    for i in range(len(row_array)):
        for j in (3, 26, 29):
            if isinstance(row_array[i][j], float):
                row_array[i][j] = datetime.datetime(*xlrd.xldate_as_tuple(row_array[i][j], wb.datemode)) 
    for i in row_array:
        i.pop()

    return row_array


from django.core.management.base import BaseCommand
from machines.models import Machine


class Command(BaseCommand):
    
    def init_data(self): 
        # fields = [
        #     inventory_number, name, number_machine, year_of_commissioning, engine_brand, engine_number,
        #     capacity, costs_at_rate, dizmaslo, turbocharger_mark, turbocharger_count, filtr_air,
        #     filtr_fuel, filtr_dizmaslo, filtr_gidravlichni, lining_blocks_mark, lining_blocks_count,
        #     lining_pidpiiki_mark, lining_pidpiiki_count, compressor_mark, compressor_count, diametr_wheel_pairs,
        #     battery_kind, battery_count, battery_last_replacement, battery_count_need, date_ost_kr,
        #     initial_value, residual_value, depreciation_end_date, dizmaslo_mark, dizmaslo_volume,
        #     transmission_fluid_mark, transmission_fluid_volume, hydraulic_fluid_mark, hydraulic_fluid_volume
        # ]
        
        for element in read_data_xls():
            Machine.objects.create(
                inventory_number = element[0], 
                name = element[1], 
                number_machine = element[2], 
                year_of_commissioning = element[3] if element[3] else None, 
                engine_brand = element[4], 
                engine_number = element[5],
                capacity = element[6] if element[6] else 0, 
                costs_at_rate = element[7] if element[7] else 0, 
                dizmaslo = element[8] if element[8] else 0, 
                turbocharger_mark = element[9], 
                turbocharger_count = element[10] if element[10] else 0, 
                filtr_air = element[11],
                filtr_fuel = element[12], 
                filtr_dizmaslo = element[13], 
                filtr_gidravlichni = element[14], 
                lining_blocks_mark = element[15], 
                lining_blocks_count = element[16] if element[16] else 0,
                lining_pidpiiki_mark = element[17], 
                lining_pidpiiki_count = element[18] if element[18] else 0, 
                compressor_mark = element[19], 
                compressor_count = element[20] if element[20] else 0, 
                diametr_wheel_pairs = element[21],
                battery_kind = element[22], 
                battery_count = element[23], 
                battery_last_replacement = element[24], 
                battery_count_need = element[25], 
                date_ost_kr = element[26] if element[26] else None,
                initial_value = element[27], 
                residual_value = element[28], 
                depreciation_end_date = element[29] if element[29] else None, 
                dizmaslo_mark = element[30], 
                dizmaslo_volume = element[31] if element[31] else 0,
                transmission_fluid_mark = element[32], 
                transmission_fluid_volume = element[33] if element[33] else 0, 
                hydraulic_fluid_mark = element[34], 
                hydraulic_fluid_volume = element[35] if element[35] else 0
            )


    def handle(self, *args, **kwargs):
        print("Initializes data for machine model")
        self.init_data()