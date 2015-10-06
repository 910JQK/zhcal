#!/usr/bin/env python3


import argparse
import datetime
from calendar import Calendar


# 每年元旦的農曆日期 (1900-2049)
# 8 位整數，高 2 位表示月，低 6 位表示日
# 月份： 0: 冬月, 1: 臘月, 2: 閏冬月
LUNAR_DATE_OF_INITIAL_DAYS = [0x41, 0xb, 0x16, 0x43, 0xe, 0x1a, 0x47, 0x11, 0x1c, 0x4a, 0x14, 0x41, 0xd, 0x18, 0x46, 0x10, 0x1a, 0x48, 0x13, 0x1e, 0xb, 0x17, 0x44, 0xf, 0x19, 0x47, 0x11, 0x1c, 0x49, 0x15, 0x42, 0xd, 0x18, 0x46, 0x10, 0x1a, 0x47, 0x13, 0x1e, 0xb, 0x16, 0x44, 0xf, 0x19, 0x46, 0x12, 0x1c, 0x4a, 0x15, 0x43, 0xd, 0x18, 0x45, 0x10, 0x1b, 0x48, 0x13, 0x41, 0xc, 0x16, 0x43, 0xf, 0x19, 0x46, 0x11, 0x1d, 0x4a, 0x15, 0x42, 0xd, 0x18, 0x45, 0xf, 0x1b, 0x49, 0x13, 0x41, 0xc, 0x16, 0x43, 0xe, 0x1a, 0x47, 0x12, 0x1d, 0xb, 0x15, 0x42, 0xc, 0x18, 0x45, 0x10, 0x1b, 0x49, 0x14, 0x41, 0xb, 0x16, 0x43, 0xe, 0x19, 0x47, 0x12, 0x1d, 0x4a, 0x15, 0x42, 0xd, 0x17, 0x46, 0x11, 0x1b, 0x48, 0x14, 0x41, 0xb, 0x16, 0x44, 0xf, 0x1a, 0x47, 0x12, 0x1d, 0x4a, 0x14, 0x42, 0xd, 0x18, 0x45, 0x11, 0x1c, 0x48, 0x13, 0x41, 0x8b, 0x16, 0x44, 0x10, 0x1a, 0x47, 0x11, 0x1d, 0x4a, 0x15, 0x42, 0xe, 0x19, 0x46, 0x10, 0x1c]
# Data from Sean Lin (sean.o4u.com)
# 每年的月長和閏月數據 (1900-2049)
# 16 位整數，高 12 位表示月長，低 4 位表示閏月
# 月長： 0: 小月, 1: 大月
LUNAR_MONTH_LENGTH = [0x4bd8, 0x4ae0, 0xa570, 0x54d5, 0xd260, 0xd950, 0x5554, 0x56af, 0x9ad0, 0x55d2, 0x4ae0, 0xa5b6, 0xa4d0, 0xd250, 0xd295, 0xb54f, 0xd6a0, 0xada2, 0x95b0, 0x4977, 0x497f, 0xa4b0, 0xb4b5, 0x6a50, 0x6d40, 0xab54, 0x2b6f, 0x9570, 0x52f2, 0x4970, 0x6566, 0xd4a0, 0xea50, 0x6a95, 0x5adf, 0x2b60, 0x86e3, 0x92ef, 0xc8d7, 0xc95f, 0xd4a0, 0xd8a6, 0xb55f, 0x56a0, 0xa5b4, 0x25df, 0x92d0, 0xd2b2, 0xa950, 0xb557, 0x6ca0, 0xb550, 0x5355, 0x4daf, 0xa5b0, 0x4573, 0x52bf, 0xa9a8, 0xe950, 0x6aa0, 0xaea6, 0xab50, 0x4b60, 0xaae4, 0xa570, 0x5260, 0xf263, 0xd950, 0x5b57, 0x56a0, 0x96d0, 0x4dd5, 0x4ad0, 0xa4d0, 0xd4d4, 0xd250, 0xd558, 0xb540, 0xb6a0, 0x95a6, 0x95bf, 0x49b0, 0xa974, 0xa4b0, 0xb27a, 0x6a50, 0x6d40, 0xaf46, 0xab60, 0x9570, 0x4af5, 0x4970, 0x64b0, 0x74a3, 0xea50, 0x6b58, 0x5ac0, 0xab60, 0x96d5, 0x92e0, 0xc960, 0xd954, 0xd4a0, 0xda50, 0x7552, 0x56a0, 0xabb7, 0x25d0, 0x92d0, 0xcab5, 0xa950, 0xb4a0, 0xbaa4, 0xad50, 0x55d9, 0x4ba0, 0xa5b0, 0x5176, 0x52bf, 0xa930, 0x7954, 0x6aa0, 0xad50, 0x5b52, 0x4b60, 0xa6e6, 0xa4e0, 0xd260, 0xea65, 0xd530, 0x5aa0, 0x76a3, 0x96d0, 0x4afb, 0x4ad0, 0xa4d0, 0xd0b6, 0xd25f, 0xd520, 0xdd45, 0xb5a0, 0x56d0, 0x55b2, 0x49b0, 0xa577, 0xa4b0, 0xaa50, 0xb255, 0x6d2f, 0xada0, 0x4b63, 0x937f, 0x49f8, 0x4970, 0x64b0, 0x68a6, 0xea5f, 0x6b20, 0xa6c4, 0xaaef, 0x92e0, 0xd2e3, 0xc960, 0xd557, 0xd4a0, 0xda50, 0x5d55, 0x56a0, 0xa6d0, 0x55d4, 0x52d0, 0xa9b8, 0xa950, 0xb4a0, 0xb6a6, 0xad50, 0x55a0, 0xaba4, 0xa5b0, 0x52b0, 0xb273, 0x6930, 0x7337, 0x6aa0, 0xad50, 0x4b55, 0x4b6f, 0xa570, 0x54e4, 0xd260, 0xe968, 0xd520, 0xdaa0, 0x6aa6, 0x56df, 0x4ae0, 0xa9d4, 0xa4d0, 0xd150, 0xf252, 0xd520]

# Data from Sean Lin (sean.o4u.com)
# 二十四節氣時間 (1900-2049)
SOLAR_TERM_BASE = [4, 19, 3, 18, 4, 19, 4, 19, 4, 20, 4, 20, 6, 22, 6, 22, 6, 22, 7, 22, 6, 21, 6, 21]
SOLAR_TERM_INDEX = '0123415341536789:;<9:=<>:=1>?012@015@015@015AB78CDE8CD=1FD01GH01GH01IH01IJ0KLMN;LMBEOPDQRST0RUH0RVH0RWH0RWM0XYMNZ[MB\\]PT^_ST`_WH`_WH`_WM`_WM`aYMbc[Mde]Sfe]gfh_gih_Wih_WjhaWjka[jkl[jmn]ope]qph_qrh_sth_W'
SOLAR_TERM_OFFSET = '211122112122112121222211221122122222212222222221222122222232222222222222222233223232223232222222322222112122112121222211222122222222222222222222322222112122112121222111211122122222212221222221221122122222222222222222222223222232222232222222222222112122112121122111211122122122212221222221221122122222222222222221211122112122212221222211222122222232222232222222222222112122112121111111222222112121112121111111222222111121112121111111211122112122112121122111222212111121111121111111111122112122112121122111211122112122212221222221222211111121111121111111222111111121111111111111111122112121112121111111222111111111111111111111111122111121112121111111221122122222212221222221222111011111111111111111111122111121111121111111211122112122112121122211221111011111101111111111111112111121111121111111211122112122112221222211221111011111101111111110111111111121111111111111111122112121112121122111111011111121111111111111111011111111112111111111111011111111111111111111221111011111101110111110111011011111111111111111221111011011101110111110111011011111101111111111211111001011101110111110110011011111101111111111211111001011001010111110110011011111101111111110211111001011001010111100110011011011101110111110211111001011001010011100110011001011101110111110211111001010001010011000100011001011001010111110111111001010001010011000111111111111111111111111100011001011001010111100111111001010001010000000111111000010000010000000100011001011001010011100110011001011001110111110100011001010001010011000110011001011001010111110111100000010000000000000000011001010001010011000111100000000000000000000000011001010001010000000111000000000000000000000000011001010000010000000'

CYCLE_10 = '甲乙丙丁戊己庚辛壬癸'
CYCLE_12 = '子丑寅卯辰巳午未申酉戌亥'
CYCLE_60 = ['甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未', '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳', '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯', '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑', '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥']
ZODIAC = '鼠牛虎兔龍蛇馬羊猴雞狗豬'
LUNAR_MONTHS = '#正二三四五六七八九十冬臘'
NUM = '#一二三四五六七八九十'
QUARTERS = ['初初', '初一', '初二', '初三', '正初', '正一', '正二', '正三']

SOLAR_TERMS = ['小寒', '大寒', '立春', '雨水', '驚蟄', '春分', '清明', '穀雨', '立夏', '小滿', '芒種', '夏至', '小暑', '大暑', '立秋', '處暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪', '冬至']

FESTIVALS = [
    {
        'date': (1, 0),
        'name': '除夕'
    },
    {
        'date': (1, 1),
        'name': '春節'
    },
    {
        'date': (1, 15),
        'name': '元宵'
    },
    {
        'date': (5, 5),
        'name': '端午'
    },
    {
        'date': (7, 7),
        'name': '七夕'
    },
    {
        'date': (7, 15),
        'name': '中元'
    },
    {
        'date': (8, 15),
        'name': '中秋'
    },
    {
        'date': (9, 9),
        'name': '重陽'
    },
    {
        'date': (12, 8),
        'name': '臘八'
    },
    {
        'date': (12, 23),
        'name': '小年'
    }
]

WEEKDAYS = '一二三四五六日'
MONTHS = ['#', '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二']

DAY_SEC = 86400
TS_ZERO = datetime.date(1970, 1, 1)
# 1970 年：庚戌年
TS_ZERO_YEAR_CYCLE_INDEX = 46
# 1970 年小寒之前：丙子月
TS_ZERO_MONTH_CYCLE_INDEX = 12
# 1970 年元旦：辛巳日
TS_ZERO_DAY_CYCLE_INDEX = 17


class TZ(datetime.tzinfo):
    '''UTC+8'''

    def utcoffset(self, dt):
        return datetime.timedelta(hours=8)

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return 'UTC+8'


tz = TZ()


def check_year_range(year):
    if year not in range(1901, 2050):
        raise NotImplementedError('Out of data range')


def check_datetime_range(date_time):
    if (date_time < datetime.datetime(1901, 1, 1, tzinfo=tz)
            or date_time > datetime.datetime(2049, 12, 31, tzinfo=tz)):
        raise NotImplementedError('Out of data range')


def get_cycle_60(cycle_10, cycle_12):
    '''將一對天干索引和地支索引轉換為六十甲子索引

    @param int cycle_10 in range(0, 10)
    @param int cycle_12 in range(0, 12)
    @return int in range(0, 60)
    '''
    result = 0
    i = 0
    j = 0
    for k in range(0, 60):
        if i == cycle_10 and j == cycle_12:
            result = k
            break
        i = (i + 1) % 10
        j = (j + 1) % 12
    return result


def get_lunar_date_str(index):
    '''從索引生成農曆日期字符串

    @param int index in range(1, 31)
    @return str
    '''
    h = index // 10
    l = index % 10
    if h == 0:
        return '初' + NUM[l]
    elif h == 1:
        if l == 0:
            return '初十'
        else:
            return '十' + NUM[l]
    elif h == 2:
        if l == 0:
            return '二十'
        else:
            return '廿' + NUM[l]
    elif h == 3:
        return '三十'


def date2ts(date):
    '''將 date object 轉換為 UNIX 時間戳

    @param datetime.date date
    @return int
    '''
    return int((date - TS_ZERO).total_seconds())


def is_leap_year(year):
    '''判斷閏年

    @param int year > 1582
    @return bool
    '''
    if(year % 100 == 0):
        return (year % 400 == 0)
    else:
        return (year % 4 == 0)


def get_solar_term_date(index, year):
    '''計算節氣日期

    Algorithm from Sean Lin (sean.o4u.com)

    @param int index in range(0, 24)
    @param int year in range(1901, 2050)
    @return datetime.date
    '''
    return datetime.date(year, index//2 + 1, SOLAR_TERM_BASE[index] + int(
       SOLAR_TERM_OFFSET[(ord(SOLAR_TERM_INDEX[year-1900]) - 48) * 24 + index]
    ))


def get_leap_month(year):
    '''返回當年閏月，0 代表沒有閏月

    @param int year in range(1901, 2050)
    @return int in range(0, 13)
    '''
    month = LUNAR_MONTH_LENGTH[year-1900] & 0xf
    if month == 0xf:
        return 0
    else:
        return month


def get_month_day_count(month, year):
    '''返回當年當月的天數

    @param int month in range(0, 13)
    @param int year in range(1901, 2050)
    @return int in range(29, 31)
    '''
    if month:
        if LUNAR_MONTH_LENGTH[year-1900] & (0x10000 >> month):
            return 30
        else:
            return 29
    else:
        if get_leap_month(year+1):
            return 30
        else:
            return 29


def build_calendar(year):
    '''生成農曆年曆數據

    @param int year in range(1901, 2050)
    @return list<
        dict { lunar_month, lunar_date, is_leap_month, timestamp }
    >
    '''
    initial_month = (
        LUNAR_DATE_OF_INITIAL_DAYS[year-1900] & (0x3 << 6)
    ) >> 6
    initial_date = LUNAR_DATE_OF_INITIAL_DAYS[year-1900] & 0x3f
    leap_prev = get_leap_month(year-1)
    leap = get_leap_month(year)
    year_day_count = 365 + is_leap_year(year)

    data = []
    result = []

    if initial_month == 0:
        # 冬月
        data.append({
            'index': 11,
            'day_count': get_month_day_count(11, year-1),
            'is_leap': False
        })
        # 千年難尋閏臘月，因此不判定閏臘月
    elif initial_month == 1:
        # 臘月
        pass
    elif initial_month == 2:
        # 閏冬月
        data.append({
            'index': 11,
            'day_count': get_month_day_count(0, year-1),
            'is_leap': True
        })
    data.append({
        'index': 12,
        'day_count': get_month_day_count(12, year-1),
        'is_leap': False
    })

    for i in range(1, 13):
        data.append({
            'index': i,
            'day_count': get_month_day_count(i, year),
            'is_leap': False
        })
        if leap == i:
            data.append({
                'index': i,
                'day_count': get_month_day_count(0, year),
                'is_leap': True
            })

    ts = date2ts(datetime.date(year, 1, 1))
    lunar_date = initial_date
    j = 0
    for i in range(0, year_day_count):
        if lunar_date > data[j]['day_count']:
            lunar_date = 1
            j += 1
        result.append({
            'timestamp': ts,
            'lunar_date': lunar_date,
            'lunar_month': data[j]['index'],
            'is_leap_month': data[j]['is_leap']
        })
        lunar_date += 1
        ts += DAY_SEC

    return result


def get_year_cycle_index_approx(year):
    '''干支紀年：返回當年立春以後的年柱六十甲子索引

    @param int year
    @return int in range(0, 60)
    '''
    index = (TS_ZERO_YEAR_CYCLE_INDEX + (year - 1970)) % 60
    if index < 0:
        index += 60
    return index


def get_year_cycle_index(date):
    '''干支紀年（返回六十甲子索引）

    @param datetime.date date (1901/1/1 - 2049/12/31)
    @return int in range(0, 60)
    '''
    index = get_year_cycle_index_approx(date.year)
    if(date < get_solar_term_date(2, date.year)):
        index = (index - 1) % 60
    return index


def get_month_cycle_index(date):
    '''干支紀月（返回六十甲子索引）

    @param datetime.date date (1901/1/1 - 2049/12/31)
    @return int in range(0, 60)
    '''
    start_index = (TS_ZERO_MONTH_CYCLE_INDEX + (date.year - 1970) * 12) % 60
    add = 12
    for i in range(0, 12):
        if date < get_solar_term_date(i*2, date.year):
            add = i
            break
    return (start_index + add) % 60


def get_day_cycle_index(date):
    '''干支紀日（返回六十甲子索引）

    @param datetime.date date
    @return int in range(0, 60)
    '''
    return (TS_ZERO_DAY_CYCLE_INDEX + date2ts(date) // DAY_SEC) % 60


def get_hour_cycle_index(date_time):
    '''干支紀時（返回六十甲子索引）

    Algorithm from Wikipedia (zh)
    %E5%B9%B2%E6%94%AF#.E5.B9.B2.E6.94.AF.E7.B4.80.E6.99.82

    @param datetime.datetime date_time
    @return int in range(0, 60)
    '''
    day_cycle_index = get_day_cycle_index(date_time.date())
    cycle_12 = get_hour(date_time.time())
    cycle_10 = (cycle_12 + (day_cycle_index % 10 % 5) * 2) % 10
    return get_cycle_60(cycle_10, cycle_12)


def get_hour(time):
    '''返回時辰（地支索引）

    @param datetime.time time
    @return int in range(0, 12)
    '''
    return (time.hour + 1) // 2 % 12


def get_quarter(time):
    '''返回刻（九十六刻制）

    @param datetime.time time
    @return int in range(0, 8)
    '''
    return 4 * ((time.hour + 1) % 2) + time.minute // 15


def get_zodiac(date):
    '''返回生肖索引（以正月初一為轉換點）

    @param datetime.date date (1901/1/1 - 2049/12/31)
    @return int in range(0, 12)
    '''
    boundary = zh_to_gregorian(date.year, 1, 1, False)
    index = get_year_cycle_index_approx(date.year) % 12
    if date < boundary:
        index = (index - 1) % 12
    return index


def get_festivals_date(year):
    '''返回當年農曆節日的格里曆日期

    @param int year in range(1901, 2050)
    @return list<
        dict { date, name }
    >
    '''
    result = []
    days = build_calendar(year)
    prev_day_lunar_date = -1
    for day in days:
        for festival in FESTIVALS:
            if festival['date'][0] == day['lunar_month']:
                if festival['date'][1] == day['lunar_date']:
                    result.append({
                        'date': datetime.datetime.utcfromtimestamp(
                            day['timestamp']
                        ).date(),
                        'lunar_date': festival['date'],
                        'name': festival['name']
                    })
                elif (festival['date'][1] == 0 and day['lunar_date'] == 1
                      and prev_day_lunar_date != -1):
                    result.append({
                        'date': datetime.datetime.utcfromtimestamp(
                            day['timestamp'] - DAY_SEC
                        ).date(),
                        'lunar_date': (
                            (festival['date'][0] - 1 - 1) % 12 + 1,
                            prev_day_lunar_date
                        ),
                        'name': festival['name']
                    })
        prev_day_lunar_date = day['lunar_date']
    return result


def gregorian_to_zh(date):
    '''格里曆轉農曆

    @param datetime.date date (1900/1/1 - 2049/12/31)
    @return dict { lunar_month, lunar_date, is_leap_month, timestamp }
    '''
    ts = date2ts(date)
    days = build_calendar(date.year)
    for day in days:
        if day['timestamp'] == ts:
            return day


def zh_to_gregorian(year, lunar_month, lunar_date, is_leap_month):
    '''農曆轉格里曆

    @param int year in range(1901, 2050)
    @param int lunar_month in range(1, 13)
    @param int lunar_date in range(1, 31)
    @param bool is_leap_month
    @return datetime.date
    '''
    target = {
        'lunar_month': lunar_month,
        'lunar_date': lunar_date,
        'is_leap_month': is_leap_month
    }
    days = build_calendar(year)
    for day in days:
        ts = day['timestamp']
        del day['timestamp']
        if day == target:
            return datetime.datetime.utcfromtimestamp(ts).date()


def inverse_color(string):
    return '\033[7m' + string + '\033[0m'


def num_prepend_blank(num):
    result = str(num)
    if len(result) < 2:
        result = ' ' + result
    return result


def print_datetime(date_time):
    check_datetime_range(date_time)
    date = date_time.date()
    time = date_time.time()
    zh = gregorian_to_zh(date_time.date())
    lunar_month_prefix = ''
    if zh['is_leap_month']:
        lunar_month_prefix = '閏'
    print(
'''
西元 %(year)d 年 %(month)d 月 %(day)d 日  週%(weekday)s
農曆 %(lunar_month)s月%(lunar_date)s  生肖：%(zodiac)s
四柱 %(year_cycle)s年  %(month_cycle)s月  %(day_cycle)s日  %(hour_cycle)s時
時間 東八區 %(hour)d 時 %(minute)d 分 %(second)d 秒  %(c_quarter)s刻
''' % {
    'year': date.year,
    'month': date.month,
    'day': date.day,
    'weekday': WEEKDAYS[date.weekday()],
    'lunar_month': lunar_month_prefix + LUNAR_MONTHS[zh['lunar_month']],
    'lunar_date': get_lunar_date_str(zh['lunar_date']),
    'zodiac': ZODIAC[get_zodiac(date)],
    'year_cycle': CYCLE_60[get_year_cycle_index(date)],
    'month_cycle': CYCLE_60[get_month_cycle_index(date)],
    'day_cycle': CYCLE_60[get_day_cycle_index(date)],
    'hour_cycle': CYCLE_60[get_hour_cycle_index(date_time)],
    'hour': date_time.hour,
    'minute': date_time.minute,
    'second': date_time.second,
    'c_quarter': QUARTERS[get_quarter(time)]
      }
    )


def print_info(args):
    print_datetime(datetime.datetime(args.year, args.month, args.day,
                                     args.hour, args.m, 0, tzinfo=tz))


def print_now(args):
    print_datetime(datetime.datetime.now(tz))


def print_festivals(year):
    check_year_range(year)
    festivals = get_festivals_date(year)
    for festival in festivals:
        print('{0} {1}月{2}  {3} 月 {4} 日  週{5}'.format(
            festival['name'],
            LUNAR_MONTHS[festival['lunar_date'][0]],
            get_lunar_date_str(festival['lunar_date'][1]),
            num_prepend_blank(festival['date'].month),
            num_prepend_blank(festival['date'].day),
            WEEKDAYS[festival['date'].weekday()]
        ))


def print_calendar(year, month, first_weekday):
    check_year_range(year)
    # Print header
    print('{:^63}'.format(MONTHS[month] + '月 ' + str(year)))
    line = ''
    print('')
    for i in range(0, 7):
        line += '   週{0}  '.format(WEEKDAYS[(i+first_weekday) % 7])
    print(line)

    # Initialize
    first = True
    days = build_calendar(year)
    festivals = get_festivals_date(year)
    st1 = get_solar_term_date((month - 1)*2, year)
    st2 = get_solar_term_date((month - 1)*2 + 1, year)
    now = datetime.datetime.now(tz)
    today = now.date()
    index = 0
    line = ''
    for date in Calendar(first_weekday).itermonthdates(year, month):
        if date.month > month and date.year == year:
            break
        if date.weekday() == first_weekday:
            print(line)
            line = ''
        if first and date.year == year:
            ts = date2ts(date)
            for i in range(0, len(days)):
                if days[i]['timestamp'] == ts:
                    index = i
                    break
            first = False
        day = num_prepend_blank(date.day)
        if date.month == month:
            lunar_str = ''
            lunar_date = days[index]['lunar_date']
            for festival in festivals:
                if date == festival['date']:
                    lunar_str = festival['name']
                    break
            if lunar_str:
                pass
            elif date == st1:
                lunar_str = SOLAR_TERMS[(month - 1)*2]
            elif date == st2:
                lunar_str = SOLAR_TERMS[(month - 1)*2 + 1]
            elif lunar_date == 1:
                month_str = LUNAR_MONTHS[days[index]['lunar_month']]
                if days[index]['is_leap_month']:
                    lunar_str = '閏' + month_str
                else:
                    lunar_str = month_str + '月'
            else:
                lunar_str = get_lunar_date_str(lunar_date)
            if date == today:
                line += inverse_color('{0} {1}'.format(day, lunar_str))
                line += '  '
            else:
                line += '{0} {1}  '.format(day, lunar_str)
        else:
            line += '         '
        index += 1
    if line != '':
        print(line)


def print_full_year(year, first_weekday):
    check_year_range(year)
    for i in range(1, 13):
        print_calendar(year, i, first_weekday)
        print('')


def main():
    parser = argparse.ArgumentParser(
        description=
        'Chinese Calendar Toolkit (All the time involved is UTC+8 time)'
    )
    subparsers = parser.add_subparsers()

    cal = subparsers.add_parser('calendar', help='Print calendar of a month')
    cal.add_argument('year', type=int)
    cal.add_argument('month', type=int)
    cal.add_argument('-f', type=int, default=0, metavar='first_weekday',
                     help='The first weekday (0=Monday)')
    cal.set_defaults(func=lambda args: print_calendar(args.year, args.month,
                                                        args.f))

    full = subparsers.add_parser('full',
                                 help='Print calendar of the whole year')
    full.add_argument('year', type=int)
    full.add_argument('-f', type=int, default=0, metavar='first_weekday',
                      help='The first weekday (0=Monday)')
    full.set_defaults(func=lambda args: print_full_year(args.year, args.f))

    festival = subparsers.add_parser('festivals',
                                     help='Print gregorian date of festivals')
    festival.add_argument('year', type=int)
    festival.set_defaults(func=lambda args: print_festivals(args.year))

    info = subparsers.add_parser('info',
        help='Print information of specified time, including the Four Pillars'
    )
    info.add_argument('year', type=int)
    info.add_argument('month', type=int)
    info.add_argument('day', type=int)
    info.add_argument('hour', type=int)
    info.add_argument('-m', type=int, default=0, help='Minute')
    info.set_defaults(func=print_info)

    now = subparsers.add_parser('now', help='Print information of now')
    now.set_defaults(func=print_now)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        datetime_now = datetime.datetime.now(tz)
        print_calendar(datetime_now.year, datetime_now.month, 0)


if __name__ == '__main__':
    main()
