GAME_JOBS = {
    1: {
        'name': 'Расклейщик листовок',
        'requirements': {
            'experience': 0,
        },
        # 0% profit-effect from previous job
        # profits after 20 energy = 1000$ - 2000$ - 3000$
        'earnings_money': {
            'min': 50,
            'max': 150+1,
            'step': 30
        }
    },
    2: {
        'name': 'Автомеханик СТО',
        'requirements': {
            'experience': 5000,
        },
        # ~12% profit-effect from previous job
        'earnings_money': {
            'min': 60,
            'max': 180+1,
            'step': 30
        }
    },
    3: {
        'name': 'Официант в ресторане',
        'requirements': {
            'experience': 10000,
        },
        # 24% profit-effect from previous job
        'earnings_money': {
            'min': 70,
            'max': 220+1,
            'step': 50,
        }
    },
    4: {
        'name': 'Директор ночного клуба',
        'requirements': {
            'experience': 15000,
        },
        # 36% profit-effect from previous job
        'earnings_money': {
            'min': 100,
            'max': 300+1,
            'step': 50,
        }
    },
    5: {
        'name': 'Веб-дизайнер',
        'requirements': {
            'gameLevel': 20000,
        },
        # 48% profit-effect from previous job
        'earnings_money': {
            'min': 150,
            'max': 450+1,
            'step': 60,
        }
    },
    6: {
        'name': 'Разработчик',
        'requirements': {
            'experience': 25000,
        },
        # 60% profit-effect from previous job
        'earnings_money': {
            'min': 240,
            'max': 720+1,
            'step': 80,
        }
    },
    7: {
        'name': 'Кибербезопасник',
        'requirements': {
            'experience': 30000,
        },
        # 72% profit-effect from previous job
        'earnings_money': {
            'min': 430,
            'max': 1240+1,
            'step': 90,
        }
    },
    8: {
        'name': 'Космический инженер',
        'requirements': {
            'experience': 35000,
        },
        # 84% profit-effect from previous job
        'earnings_money': {
            'min': 780,
            'max': 2280+1,
            'step': 500,
        }
    },
}