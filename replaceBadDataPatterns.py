import logging
import pandas as pd

logging_file = 'C:\Users\Tony Chacon\OneDrive\Documents\__Software_Side_Projects\Python_File_Cleanup\Florida_RealEstateCommission_Python_Parsing_Log.log'

file_logger = logging.basicConfig(
    filename= logging_file, 
    format='%(asctime)s %(message)s', 
    datefmt='%m/%d/%Y %I:%M:%S %p', 
    level=logging.INFO)

logging_failure_text = ''
logging_failure_line_number = -1

input_file = "C:\Users\Tony Chacon\OneDrive\Documents\__Software_Side_Projects\Python_File_Cleanup\Florida_Agents.csv"

output_file = "C:\Users\Tony Chacon\OneDrive\Documents\__Software_Side_Projects\Python_File_Cleanup\Florida_Agents_Processed_v2.csv"

# if not output_file:
#     print("output file exists. Deleting.")
#     os.remove(output_file)

line_number = 0

file_encoding = 'utf-16'

headers_row = '{-}Board{-},{-}Board Name{-},{-}Licensee Name{-},{-}DBA Name{-},{-}Rank{-},{-}Address 1{-},{-}Address 2{-},{-}Address 3{-},{-}City{-},{-}State{-},{-}Zip{-},{-}County Code{-},{-}County Name{-},{-}License Number{-},{-}Primary Status{-},{-}Secondary Status{-},{-}Original License Date{-},{-}Status Effective Date{-},{-}License Expiration Date{-},{-}Alternate License Number{-},{-}Self Proprietor Name{-},{-}Employer Name{-},{-}Employer License Number{-}'

# Patterns of bad data and their appropriate replacements for this file
# ---------------------------------------------------------------------
blank_string_good_data_pattern = ''

bad_data_pattern_1 = '",'
good_data_pattern_1 = '{-},'

bad_data_pattern_2 = '|,'
good_data_pattern_2 = good_data_pattern_1

bad_data_pattern_3 = ',"'
good_data_pattern_3 = ',{-}'

bad_data_pattern_4 = ',|'
good_data_pattern_4 = good_data_pattern_3

bad_data_pattern_5 = '"Board'
good_data_pattern_5 = '{-}Board'

bad_data_pattern_6 = '|Board'
good_data_pattern_6 = good_data_pattern_5

bad_data_pattern_7 = '"25"|,'
good_data_pattern_7 = '{-}25{-},'

bad_data_pattern_8 = '"25",'
good_data_pattern_8 = good_data_pattern_7

bad_data_pattern_9 = '"|"'
good_data_pattern_9 = '{-},{-}'

bad_data_pattern_10 = '"\n'
good_data_pattern_10 = '{-}\n'

bad_data_pattern_11 ='\r\n'
good_data_pattern_11 = blank_string_good_data_pattern

bad_data_pattern_12 = '\t'
good_data_pattern_12 = blank_string_good_data_pattern

# weird edge case that happens after other parsing
bad_data_pattern_13 = '"25'
good_data_pattern_13 = '{-}25'

bad_data_pattern_14 = '\x8d'
good_data_pattern_14 = blank_string_good_data_pattern

bad_data_pattern_15 = '\x81'
good_data_pattern_15 = blank_string_good_data_pattern

bad_data_pattern_16 = '{-}Board"|{-}Board Name{-},{-}Licensee Name{-},{-}DBA Name{-},{-}Rank{-},{-}Address 1{-},{-}Address 2{-},{-}Address 3{-},{-}City{-},{-}State{-},{-}Zip{-},{-}County Code{-},{-}County Name{-},{-}License Number{-},{-}Primary Status{-},{-}Secondary Status{-},{-}Original License Date{-},{-}Status Effective Date{-},{-}License Expiration Date{-},{-}Alternate License Number{-},{-}Self Proprietor Name{-},{-}Employer Name{-},{-}Employer License Number{-}'
good_data_pattern_16 = '\n'

bad_data_pattern_17 =',","'
good_data_pattern_17 = '{-},{-}'

bad_data_pattern_18 = '",, '
good_data_pattern_18 = '{-}'


# extensible because this allows more more edge cases to be added as they appear without a ton of extra work
data_pattern_replacement_dictionary = {
    bad_data_pattern_1 : good_data_pattern_1,
    bad_data_pattern_2 : good_data_pattern_2,
    bad_data_pattern_3 : good_data_pattern_3,
    bad_data_pattern_4 : good_data_pattern_4,
    bad_data_pattern_5 : good_data_pattern_5,
    bad_data_pattern_6 : good_data_pattern_6,
    bad_data_pattern_7 : good_data_pattern_7,
    bad_data_pattern_8 : good_data_pattern_8,
    bad_data_pattern_9 : good_data_pattern_9,
    bad_data_pattern_10 : good_data_pattern_10,
    bad_data_pattern_11 : good_data_pattern_11,
    bad_data_pattern_12 : good_data_pattern_12,
    bad_data_pattern_13 : good_data_pattern_13,
    bad_data_pattern_14 : good_data_pattern_14,
    bad_data_pattern_15 : good_data_pattern_15,
    bad_data_pattern_16 : good_data_pattern_16,
    bad_data_pattern_17 : good_data_pattern_17,
    # bad_data_pattern_18 : good_data_pattern_18,
}

# replace any of the bad data patterns with good ones for each line in the text
def multiple_replace(text, word_dictionary):
    text = text.lstrip()
    for key in word_dictionary:
        if key in text:
            text = text.replace(key, word_dictionary[key]) # replaces a known faulty pattern with an intended one
            # text = text.title()
            # text = remove_accents_from_text(text, file_encoding)

        else:
            pass
    return text

def remove_accents_from_text(text, encoding):
    byte_string = text.encode(encoding)
    unicode_string = byte_string.decode(encoding)
    return unicode_string

logging.info('Preparing to parse file.')

with open(input_file, 'r', encoding=file_encoding) as file_to_process:
    with open(output_file, 'w') as file_processed:

        # empties the output CSV if exists
        if file_processed:
            file_processed.truncate()

        for line in file_to_process:
            line_number += 1
            try:
                #print('line before:', line)
                line = multiple_replace(line, data_pattern_replacement_dictionary)
                #print('line after: ', line)
                print("line number: ", line_number)
                if (headers_row in line) and line_number > 1:
                    line = blank_string_good_data_pattern

                elif (line_number == 1) and headers_row not in line:
                    line = headers_row

                # elif line.endswith(''):
                #     line = 

                file_processed.write(line)

            # Capture compiler error + useful information, send to log file
            except Exception as exception_error:
                logging_failure_line_number = line_number
                logging_failure_line = line
                error_message = 'Error: ' + str(exception_error)
                process_logging_message = 'processed failed on CSV line: ' + str(logging_failure_line_number) +', line that caused failure:' + logging_failure_line
                logging.info(exception_error)
                logging.info(process_logging_message)
                file_to_process.close()
                file_processed.close()
                break #stop program if an error is reached (easier to debug, since there's nearly 2 million rows)
