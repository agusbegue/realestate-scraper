from utils.business_rules import AREA_DELTA


QUERY = '?'
AND = '&'
SECOND_PARAM = '%2C+'


def parse_url(url, parameters):
    if len(parameters) > 0:
        url += QUERY
    for i, param in enumerate(parameters):
        if len(param) == 2:
            url += '{}={}'.format(param[0], param[1])
        elif len(param) == 3:
            url += '{}={}{}{}'.format(param[0], param[1], SECOND_PARAM, param[2])
        else:
            raise ValueError('Too many arguments to unpack')
        if i < len(parameters) - 1:
            url += AND
    return url


BASE_PARAMS = ('adfilter_area', 'adfilter_areamax', 'adfilter_lift', 'adfilter_parkingspace')


def get_extra_params(prop):
    query = ()
    area = prop.get('area', None)
    if area:
        query += (('adfilter_area', str(int(area * (1 - AREA_DELTA)))),
                  ('adfilter_areamax', str(int(area * (1 + AREA_DELTA)))))
    # incluye caso negativo tambien
    if prop.get('lift', None):
        query += (('adfilter_lift', '1'),)
    if prop.get('parking', None):
        query += (('adfilter_parkingspace', '1'),)
    for param in BASE_PARAMS:
        if not any(param in code for code in query):
            query += ((param, ''),)
    return query


headers = {
    'authority': 'www.idealista.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.idealista.com/point/venta-viviendas/41.43616/1.40921/15/mapa-google',
    'accept-language': 'en,es-US;q=0.9,es;q=0.8,es-419;q=0.7',
}

params = (
    ('locationUri', ''),
    ('typology', '1'),
    ('operation', '1'),
    ('freeText', ''),
    ('liveSearch', 'true'),
    ('zoom', '17'),
    ('uid', 'xdtzivth8hnwhzdwuqmlrnzba2gclpccpsvojp235tto'),
    ('adfilter_pricemin', 'default'),
    ('adfilter_price', 'default'),
    #('adfilter_area', 'default'),
    #('adfilter_areamax', 'default'),
    ('adfilter_homes', ''),
    ('adfilter_chalets', ''),
    ('adfilter_countryhouses', ''),
    ('adfilter_duplex', ''),
    ('adfilter_penthouse', ''),
    ('adfilter_rooms_0', ''),
    ('adfilter_rooms_1', ''),
    ('adfilter_rooms_2', ''),
    ('adfilter_rooms_3', ''),
    ('adfilter_rooms_4_more', ''),
    ('adfilter_baths_1', ''),
    ('adfilter_baths_2', ''),
    ('adfilter_baths_3', ''),
    ('adfilter_newconstruction', ''),
    ('adfilter_goodcondition', ''),
    ('adfilter_toberestored', ''),
    ('adfilter_hasairconditioning', ''),
    ('adfilter_wardrobes', ''),
    #('adfilter_lift', ''),
    ('adfilter_flatlocation', ''),
    #('adfilter_parkingspace', ''),
    ('adfilter_garden', ''),
    ('adfilter_swimmingpool', ''),
    ('adfilter_hasterrace', ''),
    ('adfilter_boxroom', ''),
    ('adfilter_top_floor', ''),
    ('adfilter_intermediate_floor', ''),
    ('adfilter_ground_floor', ''),
    ('adfilter_digitalvisit', ''),
    ('adfilter_agencyisabank', ''),
    ('adfilter_published', 'default'),
    ('solo-favoritos', 'false'),
)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0", "system": "Firefox 67.0 Linux',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "system": "Chrome 75.0 Win7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
]
