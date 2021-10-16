#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'grib',
        'variable': 'ocean_surface_stress_equivalent_10m_neutral_wind_speed',
        'year': '2021',
        'month': [
            '03', '04', '05',
            '06', '07', '08',
            '09', '10',
        ],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
            '31',
        ],
        'time': '08:00',
        'area': [
            55.58, 15.98, 55.25,
            16.44,
        ],
    },
    'Data/windspeed.grib')
