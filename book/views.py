from django.shortcuts import render, redirect
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from .models import Task, UserProfile
# ISO 4217 Currency Mapping
def set_session_time(request, remember_me=False):
    if remember_me:
        request.session.set_expiry(2592000) #30 weeks 
    else:
        request.session.set_expiry(7200) #2 hours 
    
GLOBAL_CURRENCIES = {
    'USD': 'US Dollar ($)', 'EUR': 'Euro (€)', 'GBP': 'British Pound (£)', 'JPY': 'Japanese Yen (¥)',
    'INR': 'Indian Rupee (₹)', 'AUD': 'Australian Dollar ($)', 'CAD': 'Canadian Dollar ($)',
    'CHF': 'Swiss Franc (CHF)', 'CNY': 'Chinese Yuan (¥)', 'NZD': 'New Zealand Dollar ($)',
    'SGD': 'Singapore Dollar ($)', 'HKD': 'Hong Kong Dollar ($)', 'SEK': 'Swedish Krona (kr)',
    'KRW': 'South Korean Won (₩)', 'NOK': 'Norwegian Krone (kr)', 'MXN': 'Mexican Peso ($)',
    'ZAR': 'South African Rand (R)', 'RUB': 'Russian Ruble (₽)', 'BRL': 'Brazilian Real (R$)',
    'TRY': 'Turkish Lira (₺)', 'MYR': 'Malaysian Ringgit (RM)', 'THB': 'Thai Baht (฿)',
    'IDR': 'Indonesian Rupiah (Rp)', 'AED': 'UAE Dirham (د.إ)', 'SAR': 'Saudi Riyal (ر.س)',
    'PHP': 'Philippine Peso (₱)', 'VND': 'Vietnamese Dong (₫)', 'TWD': 'New Taiwan Dollar ($)',
    'ILS': 'Israeli New Shekel (₪)', 'DKK': 'Danish Krone (kr)', 'PLN': 'Polish Zloty (zł)',
    'ARS': 'Argentine Peso ($)', 'CLP': 'Chilean Peso ($)', 'COP': 'Colombian Peso ($)',
    'EGP': 'Egyptian Pound (E£)', 'KWD': 'Kuwaiti Dinar (KD)', 'NGN': 'Nigerian Naira (₦)',
    'PKR': 'Pakistani Rupee (₨)', 'QAR': 'Qatari Rial (QR)', 'TND': 'Tunisian Dinar (DT)',
    'UAH': 'Ukrainian Hryvnia (₴)', 'VUV': 'Vanuatu Vatu (VT)', 'ZMW': 'Zambian Kwacha (ZK)',
    'AMD': 'Armenian Dram (֏)', 'AZN': 'Azerbaijani Manat (₼)', 'BDT': 'Bangladeshi Taka (৳)',
    'BHD': 'Bahraini Dinar (BD)', 'BIF': 'Burundian Franc (FBu)', 'BND': 'Brunei Dollar ($)',
    'BOB': 'Bolivian Boliviano (Bs)', 'BWP': 'Botswana Pula (P)', 'BYN': 'Belarusian Ruble (Br)',
    'CUP': 'Cuban Peso ($)', 'CVE': 'Cape Verdean Escudo ($)', 'CZK': 'Czech Koruna (Kč)',
    'DJF': 'Djiboutian Franc (Fdj)', 'DOP': 'Dominican Peso ($)', 'DZD': 'Algerian Dinar (DA)',
    'ETB': 'Ethiopian Birr (Br)', 'FJD': 'Fijian Dollar ($)', 'GEL': 'Georgian Lari (₾)',
    'GHS': 'Ghanaian Cedi (GH₵)', 'GMD': 'Gambian Dalasi (D)', 'GNF': 'Guinean Franc (FG)',
    'GTQ': 'Guatemalan Quetzal (Q)', 'GYD': 'Guyanese Dollar ($)', 'HNL': 'Honduran Lempira (L)',
    'HRK': 'Croatian Kuna (kn)', 'HTG': 'Haitian Gourde (G)', 'HUF': 'Hungarian Forint (Ft)',
    'IQD': 'Iraqi Dinar (ID)', 'IRR': 'Iranian Rial (﷼)', 'ISK': 'Icelandic Krona (kr)',
    'JMD': 'Jamaican Dollar ($)', 'JOD': 'Jordanian Dinar (JD)', 'KES': 'Kenyan Shilling (KSh)',
    'KGS': 'Kyrgyzstani Som (с)', 'KHR': 'Cambodian Riel (៛)', 'KMF': 'Comorian Franc (CF)',
    'KZT': 'Kazakhstani Tenge (₸)', 'LAK': 'Laotian Kip (₭)', 'LBP': 'Lebanese Pound (L£)',
    'LKR': 'Sri Lankan Rupee (Rs)', 'LRD': 'Liberian Dollar ($)', 'LSL': 'Lesotho Loti (L)',
    'LYD': 'Libyan Dinar (LD)', 'MAD': 'Moroccan Dirham (MAD)', 'MDL': 'Moldovan Leu (L)',
    'MGA': 'Malagasy Ariary (Ar)', 'MKD': 'Macedonian Denar (den)', 'MMK': 'Myanmar Kyat (K)',
    'MNT': 'Mongolian Tugrik (₮)', 'MOP': 'Macanese Pataca (P)', 'MRU': 'Mauritanian Ouguiya (UM)',
    'MUR': 'Mauritian Rupee (Rs)', 'MVR': 'Maldivian Rufiyaa (Rf)', 'MWK': 'Malawian Kwacha (MK)',
    'MZN': 'Mozambican Metical (MT)', 'NAD': 'Namibian Dollar ($)', 'NIO': 'Nicaraguan Cordoba (C$)',
    'NPR': 'Nepalese Rupee (Rs)', 'OMR': 'Omani Rial (RO)', 'PAB': 'Panamanian Balboa (B/.)',
    'PEN': 'Peruvian Sol (S/.)', 'PGK': 'Papua New Guinean Kina (K)', 'PYG': 'Paraguayan Guarani (₲)',
    'RON': 'Romanian Leu (lei)', 'RSD': 'Serbian Dinar (din)', 'RWF': 'Rwandan Franc (FRw)',
    'SBD': 'Solomon Islands Dollar ($)', 'SCR': 'Seychellois Rupee (Rs)', 'SDG': 'Sudanese Pound (S£)',
    'SHP': 'Saint Helena Pound (£)', 'SLL': 'Sierra Leonean Leone (Le)', 'SOS': 'Somali Shilling (Sh)',
    'SRD': 'Surinamese Dollar ($)', 'STN': 'Sao Tome and Principe Dobra (Db)', 'SYP': 'Syrian Pound (LS)',
    'SZL': 'Swazi Lilangeni (L)', 'TJS': 'Tajikistani Somoni (SM)', 'TMT': 'Turkmenistani Manat (m)',
    'TOP': 'Tongan Paʻanga (T$)', 'TTD': 'Trinidad and Tobago Dollar ($)', 'TZS': 'Tanzanian Shilling (x/y)',
    'UGX': 'Ugandan Shilling (USh)', 'UYU': 'Uruguayan Peso ($)', 'UZS': 'Uzbekistani Som (с)',
    'WST': 'Samoan Tala (WS$)', 'XAF': 'Central African CFA Franc (FCFA)', 'XCD': 'East Caribbean Dollar ($)',
    'XOF': 'West African CFA Franc (CFA)', 'XPF': 'CFP Franc (F)', 'YER': 'Yemeni Rial (﷼)',
}

def main(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'book/main.html')

def user_login(request):
    if request.user.is_authenticated: #if user is already logged in, show dashboard 
        return redirect('main')
    if request.method == "POST": #if method is POST 
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        remember = request.POST.get('remember', False)
        
        user = authenticate(request, username=username, password=password) #authenticate the user 

        if user is not None: #if user exists 
            login(request, user) #login 
            set_session_time(request, remember_me=remember) #set session_time baded on the rememberme checkbox 
            return redirect("main")
        else: 
            return render(request, "book/login.html", { #in case of no user to authenticate 
                "error":"invalid credentials"
            })
    else: 
        return render(request, 'book/login.html') #for GET method 

def user_signup(request): 
    context = {
            'currencies':GLOBAL_CURRENCIES
    }
    if request.method == "POST": #if method is post 
        username = request.POST.get("username").strip() #get all data from frontend 
        email = request.POST.get("email").strip()
        password = request.POST.get("confirm_password").strip()
        currency = request.POST.get("currency").strip()

        try:
            #create the user 
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            #add the user to UserProfile model 
            profile = UserProfile.objects.create(user=user, currency=currency)
            user = authenticate(request, username=username, password=password) #authenticate the user 
            
            if user:
                login(request, user) #login 
                set_session_time(request) #set default expiration 

            return render(request, 'book/main.html', context)
        except Exception as e:
            print(e) #remove when producing 
            return render(request, "book/signup.html", {
                "error": "user already exists with that email or username"
            }) 
    return render(request, 'book/signup.html', context)

def user_logout(request):
    if not request.user.is_authenticated:
        return redirect("main")
    if request.method == "POST":
        logout(request)
        return redirect("main")