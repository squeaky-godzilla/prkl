# record_format = {
#                     "artist": "unicode",
#                     "title": "unicode",
#                     "difficulty": "float",
#                     "level": "int",
#                     "released": "unicode"
#                 }
#
# bad_record = {
#                     "artist": "The Yousicians",
#                     "title": "Lycanthropic Metamorphosis",
#                     "difficulty": 14.6,
#                     "level": "13",
#                     "released": "1999-12-31"
#                 }

def format_chk(tested_obj,example_obj,date_format):
    import datetime
    failed_keys = []
    # print example_obj
    # print tested_obj
    for key, value in tested_obj.items():
        if key.replace("u'","'") in example_obj:
            # print type(value).__name__ + " | should be " + example_obj[key]
            if type(value).__name__ == example_obj[key]:
                pass
            elif type(value).__name__ == "int" and example_obj[key] == 'float':
                pass
            elif type(value).__name__ == "unicode":
                try:
                    datetime.datetime.strptime(value,date_format)
                except ValueError:
                    failed_keys.append(key)
            else:
                failed_keys.append(key)
        else:
            failed_keys.append(key)
    return failed_keys

# print format_chk(bad_record, record_format, "released", '%Y-%m-%d')
