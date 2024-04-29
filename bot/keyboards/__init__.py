from . import jobs, start, general, bank, business

keyboards = {
    'start': start.keyboard,
    'general': general.keyboard,
    
    'bank': bank.keyboard,
    'bank_cancel': bank.keyboard_cancel,

    'business': business.keyboard,
    'my_business': business.keyboard_my_business,

    'jobs': jobs.keyboard
}