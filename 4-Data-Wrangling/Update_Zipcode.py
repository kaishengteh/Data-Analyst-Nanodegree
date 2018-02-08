'''
This code will update non 5-digit zipcode.
If it is 8/9-digit, only the first 5 digits are kept.
If it has the state name in front, only the 5 digits are kept.
If it is something else, will not change anything as it might result in error when validating the csv file.
'''
def update_zipcode(zipcode):
    """Clean postcode to a uniform format of 5 digit; Return updated postcode"""
    if re.findall(r'^\d{5}$', zipcode): # 5 digits 02118
        valid_zipcode = zipcode
        return valid_zipcode
    elif re.findall(r'(^\d{5})-\d{3}$', zipcode): # 8 digits 02118-029
        valid_zipcode = re.findall(r'(^\d{5})-\d{3}$', zipcode)[0]
        return valid_zipcode
    elif re.findall(r'(^\d{5})-\d{4}$', zipcode): # 9 digits 02118-0239
        valid_zipcode = re.findall(r'(^\d{5})-\d{4}$', zipcode)[0]
        return valid_zipcode
    elif re.findall(r'CA\s*\d{5}', zipcode): # with state code CA 02118
        valid_zipcode =re.findall(r'\d{5}', zipcode)[0]  
        return valid_zipcode  
    else: #return default zipcode to avoid overwriting
        return zipcode
    
def test_zip():
    for zips, ways in zip_print.iteritems():
        for name in ways:
            better_name = update_zipcode(name)
            print name, "=>", better_name

if __name__ == '__main__':
    test_zip()
