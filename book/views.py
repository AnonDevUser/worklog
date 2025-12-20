from django.shortcuts import render, redirect

# ISO 4217 Currency Mapping
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
    return render(request, 'book/main.html')

def user_login(request):
    return render(request, 'book/login.html')

def user_signup(request):
    return render(request, 'book/signup.html', {'currencies': GLOBAL_CURRENCIES})