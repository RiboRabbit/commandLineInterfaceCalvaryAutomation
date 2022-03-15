# Get new Sponsors Search
get_new_sponsors_url = "http://202.153.33.67/sponsors/sponsor/getNewSponsors"

def get_new_sponsors_payload(keyword):
    return {"keywords": keyword}

# Recipt Submit
add_receipt_submit = "http://202.153.33.67/sponsors/Receipts/receiptAddSubmit"

add_receipt_submit_payload = {
    "id": "107761",
    "sp_code": "AA3087",
    "receipt_book_no": "0000",
    "amount": "0",
    "paid_date": "28-01-2022",
    "tv":"" ,
    "status": "2",
    "mode" : "1",
    "remark_id": "" ,
    "premarks": "" ,
    "send_sms": "1"
}

#Search Receipt
add_receipt_data_url = "http://202.153.33.67/sponsors/sponsor/addReceipt"

def add_receipt_data_payload(rec_id):
    return  {"id": rec_id}

# Searching for sponsors
get_sponsers_url = "http://202.153.33.67/sponsors/sponsor/getSponsors"

get_sponsers_payload = {
    "keywords": "as"
}


# Login for Ongole
login_url = "http://202.153.33.67/sponsors/Login"

login_url_payload = {
    "user_name": "ongole",
    "password": "Ogl#Spnr",
    "location": "6"
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
        }