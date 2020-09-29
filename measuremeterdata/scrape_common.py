#!/usr/bin/env python3

# Various small utilities used by scrapers.

import datetime
import os
import subprocess
import re
import sys
import requests
import certifi
import xlrd
from .scrape_dates import parse_date


__location__ = os.path.realpath(
    os.path.join(
        os.getcwd(),
        os.path.dirname(__file__)
    )
)


class DayData(object):
    __isfrozen = False
    def __init__(self, canton, url):
        self.canton = canton
        self.url = url
        self.timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone().isoformat()
        self.datetime = None
        self.tested = None
        self.cases = None
        self.hospitalized = None
        self.new_hosp = None
        self.icu = None
        self.vent = None
        self.deaths = None
        self.recovered = None
        self.isolated = None
        self.quarantined = None
        # canton-specific fields
        self.icf = None
        self.confirmed_non_resident = None
        self.hosp_non_resident = None
        self.quarantine_riskareatravel = None
        self.quarantine_total = None

        # freeze class, so that no new attributes can be created
        self.__isfrozen = True

    def __setattr__(self, key, value):
        if self.__isfrozen and not hasattr(self, key):
            raise TypeError( "%r is a frozen class" % self )
        object.__setattr__(self, key, value)

    def __bool__(self):
        attributes = [
            self.tested,
            self.cases,
            self.hospitalized,
            self.new_hosp,
            self.icu,
            self.vent,
            self.deaths,
            self.recovered,
            self.isolated,
            self.quarantined,
            self.icf,
            self.confirmed_non_resident,
            self.hosp_non_resident,
            self.quarantine_riskareatravel,
            self.quarantine_total
        ]
        return any(v is not None for v in attributes)

    def __str__(self):
        str_rep = [
            self.canton,
            f'Scraped at: {self.timestamp}',
            f'Downloading: {self.url}'
        ]
        if self.datetime is not None and self.datetime != '':
            str_rep += [f'Date and time: {self.datetime}']
        if self.tested is not None and self.tested != '':
            str_rep += [f'Tested: {self.tested}']
        if self.cases is not None and self.cases != '':
            str_rep += [f'Confirmed cases: {self.cases}']
        if self.hospitalized is not None and self.hospitalized != '':
            str_rep += [f'Hospitalized: {self.hospitalized}']
        if self.new_hosp is not None and self.new_hosp != '':
            str_rep += [f'New Hospitalized: {self.new_hosp}']
        if self.icu is not None and self.icu != '':
            str_rep += [f'ICU: {self.icu}']
        if self.vent is not None and self.vent != '':
            str_rep += [f'Vent: {self.vent}']
        if self.deaths is not None and self.deaths != '':
            str_rep += [f'Deaths: {self.deaths}']
        if self.recovered is not None and self.recovered != '':
            str_rep += [f'Recovered: {self.recovered}']
        if self.isolated is not None and self.isolated != '':
            str_rep += [f'Isolated: {self.isolated}']
        if self.quarantined is not None and self.quarantined != '':
            str_rep += [f'Quarantined: {self.quarantined}']
        if self.icf is not None and self.icf != '':
            str_rep += [f'ICF: {self.icf}']
        if self.confirmed_non_resident is not None and self.confirmed_non_resident != '':
            str_rep += [f'Confirmed non-resident: {self.confirmed_non_resident}']
        if self.hosp_non_resident is not None and self.hosp_non_resident != '':
            str_rep += [f'Hospitalized non-resident: {self.hosp_non_resident}']
        if self.quarantine_riskareatravel is not None and self.quarantine_riskareatravel != '':
            str_rep += [f'Quarantined risk area travel: {self.quarantine_riskareatravel}']
        if self.quarantine_total is not None and self.quarantine_total != '':
            str_rep += [f'Quarantined total: {self.quarantine_total}']
        return "\n".join(str_rep)


class DistrictData:
    __initialized = False
    SEPARATOR = ','

    def __init__(self, canton='', district=''):
        self.date = None
        self.week = None
        self.year = None
        self.canton = canton
        self.district = district
        self.district_id = None
        self.population = None
        self.total_cases = None
        self.new_cases = None
        self.total_deceased = None
        self.new_deceased = None
        self.url = None
        self.__initialized = True

    def __setattr__(self, key, value):
        if self.__initialized and not hasattr(self, key):
            raise TypeError('unknown key: {0}'.format(key))
        object.__setattr__(self, key, value)

    def __str__(self):
        res = []
        res.append('' if self.district_id is None else str(self.district_id))
        res.append(self.district)
        res.append(self.canton)
        res.append(self.date or '')
        res.append('' if self.week is None else str(self.week))
        res.append('' if self.year is None else str(self.year))
        res.append('' if self.population is None else str(self.population))
        res.append('' if self.total_cases is None else str(self.total_cases))
        res.append('' if self.new_cases is None else str(self.new_cases))
        res.append('' if self.total_deceased is None else str(self.total_deceased))
        res.append('' if self.new_deceased is None else str(self.new_deceased))
        res.append(self.url)
        return DistrictData.SEPARATOR.join(res)

    @staticmethod
    def __get_int_item(item):
        return None if item is None or item == '' else int(item)

    def parse(self, data):
        items = data.split(DistrictData.SEPARATOR)
        if len(items) == 12:
            self.district_id = self.__get_int_item(items[0])
            self.district = items[1]
            self.canton = items[2]
            self.date = items[3]
            self.week = self.__get_int_item(items[4])
            self.year = self.__get_int_item(items[5])
            self.population = self.__get_int_item(items[6])
            self.total_cases = self.__get_int_item(items[7])
            self.new_cases = self.__get_int_item(items[8])
            self.total_deceased = self.__get_int_item(items[9])
            self.new_deceased = self.__get_int_item(items[10])
            self.url = items[11]
            return True
        return False

    @staticmethod
    def header():
        return 'DistrictId,District,Canton,Date,Week,Year,Population,TotalConfCases,NewConfCases,TotalDeaths,NewDeaths,SourceUrl'


spelledOutNumbersMap = {
    'eins': 1,
    'einen': 1,
    'einem': 1,
    'ein': 1,
    'zwei': 2,
    'drei': 3,
    'vier': 4,
    'fünf': 5,
    'f&uuml;nf': 5,
    'sechs': 6,
    'sieben': 7,
    'acht': 8,
    'neun': 9,
    'zehn': 10,
    'elf': 11,
    'zwölf': 12,
    'zw&ouml;lf': 12
}


class StripKeyDict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, key.strip())

    def __setitem__(self, key, val):
        dict.__setitem__(self, key.strip(), val)

    # method to search for keys with regex
    def search(self, key):
        reg = re.compile(key, flags=re.I|re.DOTALL)
        for k, v in self.items():
            if reg.match(k):
                return v
        raise KeyError


def add_cert_to_bundle():
    try:
        test = requests.get('https://www.infosan.vd.ch')
    except requests.exceptions.SSLError as err:
        print('SSL Error. Adding custom certs to Certifi store...', file=sys.stderr)
        cafile = certifi.where()
        with open(os.path.join(__location__, 'certificate.pem'), 'rb') as infile:
            customca = infile.read()
        with open(cafile, 'ab') as outfile:
            outfile.write(customca)

def download(url, encoding='utf-8', silent=False):
    if not silent:
        print("Downloading:", url)
    headers = {'user-agent': 'Mozilla Firefox Mozilla/5.0; openZH covid_19 at github'}
    r = requests.get(url, headers=headers, verify=certifi.where())
    r.raise_for_status()
    if encoding:
        r.encoding = encoding
    return r.text


def jsondownload(url, silent=False):
    if not silent:
        print("Downloading:", url)
    r = requests.get(url, verify=certifi.where())
    r.raise_for_status()
    return r.json()

def xlsdownload(url, silent=False):
    if not silent:
        print("Downloading:", url)
    r = requests.get(url, verify=certifi.where())
    r.raise_for_status()
    xls = xlrd.open_workbook(file_contents=r.content)
    return xls

def parse_xls(book, header_row=1, sheet_index=0, sheet_name=None, skip_rows=1):
    rows = []
    if sheet_name:
        sheet = book.sheet_by_name(sheet_name)
    else:
        sheet = book.sheet_by_index(sheet_index)
    # if a header cell is empty, the name of the column (e.g. "A") is used instead
    headers = {c: str(sheet.cell_value(header_row, c) or xlrd.formula.colname(c)) for c in range(sheet.ncols)}
    for r in range(header_row + skip_rows, sheet.nrows):
        entry = StripKeyDict()
        for c, h in headers.items():
            if h.strip() in entry:
                h = f"{h.strip()}{str(c)}"
            cell_type = sheet.cell_type(r, c)
            value = sheet.cell_value(r, c)
            if cell_type == xlrd.XL_CELL_DATE:
                entry[h] = xlrd.xldate.xldate_as_datetime(value, book.datemode)
            elif cell_type == xlrd.XL_CELL_EMPTY:
                entry[h] = None
            elif represents_int(value):
                entry[h] = int(value)
            else:
                entry[h] = value

        rows.append(entry)
    return rows

def pdfdownload(url, encoding='utf-8', raw=False, layout=False, silent=False):
    """Download a PDF and convert it to text"""
    if not silent:
        print("Downloading:", url)
    downloader = os.path.join(os.path.dirname(__file__), 'download.sh')
    with subprocess.Popen([downloader, url], stdout=subprocess.PIPE) as pdf:
        pdf_command = ['pdftotext']
        if raw:
            pdf_command += ['-raw']
        if layout:
            pdf_command += ['-layout']
        pdf_command += ['-', '-']
        with subprocess.Popen(pdf_command, stdin=pdf.stdout, stdout=subprocess.PIPE) as text:
            t = text.stdout.read()
            text.wait()
            return t.decode(encoding)


def filter(pattern, d, flags=re.I):
    """grep like"""
    return "\n".join(l for l in d.split('\n') if re.search(pattern, l, flags=flags))


def find(pattern, d, group=1, flags=re.I):
    """sed like. Ignore character case by default"""
    m = re.search(pattern, d, flags=flags)
    if m:
        return m[group]
    return None


def timestamp():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).astimezone()
    print("Scraped at:", now.isoformat())


def represents_int(s):
    try:
        int(s)
        return True
    except (ValueError, TypeError):
        return False

def safeint(s):
    if not s:
        return s
    f = float(s)
    r = round(f)
    if f == r:
        return int(f)
    else:
        raise ValueError(f"Can't parse {s} as int without losing precision")

def int_or_word(x):
    if x in spelledOutNumbersMap:
        return spelledOutNumbersMap[x]
    elif represents_int(x):
        return int(x)
    return None


def date_from_text(date_str):
    new_date = parse_date(date_str)
    day = new_date.split("T", 1)[0].split('-', 2)
    day = datetime.date(int(day[0]), int(day[1]), int(day[2]))
    return day
