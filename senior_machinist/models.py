from django.db import models
from django.contrib.auth.models import User
from machines.models import Machine
from engineer.models import Engineer


class SeniorMachinist(models.Model):
    """ Старший машиніст """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    brigade_name = models.CharField(blank=True, max_length=50)
    telephone1 = models.CharField(max_length=30, blank=True, default='')
    telephone2 = models.CharField(max_length=30, blank=True, default='')
    avatar = models.ImageField(blank=True, upload_to="employees", default='no-image.png')
    
    date_of_birth = models.DateField(blank=True, null=True)
    date_start_work = models.DateField(blank=True, null=True)

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, blank=True, null=True)

    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def phones(self):
        phones = self.telephone1
        if self.telephone2:
            phones += ', ' + self.telephone2
        return phones

    def __str__(self):
        return f"{self.user.username}"


class BrigadeMembers(models.Model):
    """ Члени бригади (підконтрольні машиністу) """

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    telephone1 = models.CharField(max_length=30, blank=True, default='')
    telephone2 = models.CharField(max_length=30, blank=True, default='')
    
    HELPER = 'hlp'
    MACHINIST = 'mnst'
    JOB_TITLE_CHOICES = [
        (HELPER, 'допоможний персонал'),
        (MACHINIST, 'машиніст'),
    ]
    job_title = models.CharField(
        max_length=4,
        choices=JOB_TITLE_CHOICES,
        default=MACHINIST,
    )

    seniormachinist = models.ForeignKey(SeniorMachinist, on_delete=models.CASCADE)

    def phones(self):
        phones = self.telephone1
        if self.telephone2:
            phones += ', ' + self.telephone2
        return phones

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class TempReport(models.Model):
    """ Таблиця Report - звіти від старших машиністів """
    
    filled_up = models.ForeignKey(SeniorMachinist, on_delete=models.CASCADE)
    date_of_completion = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)
    date = models.DateField(unique=True)

    checked = models.BooleanField(blank=True, default=False)
    checked_by = models.ForeignKey(Engineer, on_delete=models.CASCADE, blank=True, null = True)

    NO = 'no'
    START = 'strt'
    PART = 'part'
    FULL = 'full'
    FORWARD_I = 'fwdi'
    CHECKED_I = 'chki'
    FORWARD_D = 'fwdd'
    CHECKED_D = 'chkd'
    STAGE_CHOICES = [
        (NO, 'Пустий звіт'),
        (START, 'Початок створення'),
        (PART, 'Частично заповнений'),
        (FULL, 'Заповнений'),
        (FORWARD_I, 'Відісланий інженеру'),
        (CHECKED_I, 'Звіт перевірений інженером'), 
        (FORWARD_D, 'Відісланий директору'),
        (CHECKED_D, 'Звіт перевірений директором'), 
    ]
    stage = models.CharField(
        max_length=4,
        choices=STAGE_CHOICES,
        default=NO,
    )

    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)

  
    motohour = models.FloatField(blank=True, null=True)
    km = models.FloatField(blank=True, null=True)
    fuel = models.FloatField(blank=True, null=True)
    maslo = models.FloatField(blank=True, null=True)

    breakage = models.BooleanField(default=False)
    breakage_info = models.TextField(blank=True, null=True)
    breakage_date_start = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.filled_up} - {self.date}"


class BrigadeInfoReport(models.Model):
    """ Інформація про бригаду у звіті """

    member = models.ForeignKey(BrigadeMembers, on_delete=models.CASCADE)
    report = models.ForeignKey(TempReport, on_delete=models.CASCADE)
    date_time_from = models.DateTimeField(blank=True, null=True)
    date_time_to = models.DateTimeField(blank=True, null=True)
    
    NOT_ALLOWED = 'na'
    UNKNOW = 'uk'
    ALLOWED = 'al'
    HEALTH = 'hl'
    PASSED = 'ps'
    MEDICAL_CHECK = [
        (NOT_ALLOWED, 'не допущенний'),
        (ALLOWED, 'допущений'),
        (HEALTH, 'здоровий'),
        (PASSED, 'пройдено'),
        (UNKNOW, 'невідомо'),
    ]
    medical_check_before = models.CharField(
        max_length=2,
        choices=MEDICAL_CHECK,
        default=UNKNOW,
    )
    medical_check_after = models.CharField(
        max_length=2,
        choices=MEDICAL_CHECK,
        default=UNKNOW,
    )

    def __str__(self):
        return f"{self.member}"


class MachineWorkingReport(models.Model):
    """ Таблиця MachineWorkingReport - де машина працювала в ході робочого дня """

    report = models.ForeignKey(TempReport, on_delete=models.CASCADE)

    client = models.CharField(max_length=20, blank=True, null=True)
    station_from = models.CharField(max_length=50, blank=True, null=True)
    station_to = models.CharField(max_length=50, blank=True, null=True)
    departure_time = models.DateTimeField(blank=True, null=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    
    latFld = models.FloatField(blank=True, null=True)
    lngFld = models.FloatField(blank=True, null=True)
    time_from = models.DateTimeField(blank=True, null=True)
    time_to = models.DateTimeField(blank=True, null=True)

    place_working = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    workday_production = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.report.date}"

class MasloInfoReport(models.Model):

    report = models.OneToOneField(TempReport, on_delete=models.CASCADE, blank=True, null=True)
    marka = models.CharField(max_length=30, blank=True, null=True)
    vidano = models.CharField(max_length=30, blank=True)
    maslo_before = models.FloatField(blank=True, null=True)
    maslo_after = models.FloatField(blank=True, null=True)
    info = models.CharField(max_length=200, blank=True, null=True)


class MotoAndFuelInfoReport(models.Model):
    
    report = models.OneToOneField(TempReport, on_delete=models.CASCADE, blank=True, null=True)
    motohour_before = models.FloatField(blank=True, null=True)
    motohour_after = models.FloatField(blank=True, null=True)
    km_before = models.FloatField(blank=True, null=True)
    km_after = models.FloatField(blank=True, null=True)
    info = models.CharField(max_length=200, blank=True, null=True)
