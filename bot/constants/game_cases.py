GAME_CASES = {
    1: {
        'name': 'Стандартный',
        'desc': 'Деньги • Опыт',
        'price': {
            'currency': 'money',
            'amount': 50000
        },
        'items': [
            {
                'item_type': 'money',
                'amount': {'min': 30000, 'max': 120000+1, 'step': 10000},
                'chance': 35
            },
            {
                'item_type': 'experience',
                'amount': {'min': 15, 'max': 45+1, 'step': 15},
                'chance': 20
            },
        ]
    },
    2: {
        'name': 'Денежный',
        'desc': '• Деньги',
        'price': {
            'currency': 'special_currency',
            'amount': 2500
        },
        'items': [
            {
                'item_type': 'money',
                'amount': {'min': 750000, 'max': 1750000+1, 'step': 250000},
                'chance': 1
            },
        ]
    },
    3: {
        'name': 'Ультра',
        'desc': 'Деньги • Опыт',
        'price': {
            'currency': 'money',
            'amount': 100000
        },
        'items': [
            {
                'item_type': 'money',
                'amount': {'min': 750000, 'max': 1750000+1, 'step': 250000},
                'chance': 1
            },
            {
                'item_type': 'experience',
                'amount': {'min': 50, 'max': 150+1, 'step': 30},
                'chance': 30
            },
        ]
    },
    4: {
        'name': 'Особый',
        'desc': 'Спец.валюта',
        'price': {
            'currency': 'money',
            'amount': 500000
        },
        'items': [
            {
                'item_type': 'special_currency',
                'amount': {'min': 10000, 'max': 10000+1, 'step': 1},
                'chance': 1
            },
        ]
    },
}