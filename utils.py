
from openpyxl import Workbook
import openai, os
import uuid

def generate_general_prompt(input_text):
    general_case_prompt =  [ {"role": "system", "content": '''you are en expert in csv files and converting messy text data to csv formats.
    You will accept the input_text and understand the context present in it to create proper column names and its respective value, 
    you only give the final result csv format'''},
	
    {"role": "user", "content": "jagadeesha 25 M jordan 20 M anitha 34 f"},
	
    {"role": "assistant", "content": '''name, age, sex
            jagadeesha, jordan, anitha
            25, 20, 34
            M, M, F'''},
			
    {"role": "user", "content": '''Canada After beating Switzerland, today, Canada stands as the number 1 country in the world. 
    Canada has the third-largest reserves of oil and is the world's fourth-major oil producing country. Australia Overall,
    Australia ranks No. 5 for the second consecutive year in a row,  Japan Since 2020, Japan has moved up one spot to No. 2.  
    Switzerland As of this year, Switzerland has dropped three spots to No. 4 Best Country.  Germany is placed at No. 3 in the world
    and is listed in the top five for entrepreneurship, power, and agility, as well.'''},
	
	{"role": "assistant", "content": '''country, rank, information
    Canada, 1, After beating Switzerland, today, Canada stands as the number 1 country in the world. Canada has the third-largest reserves of oil and is the world's fourth-major oil producing country.
    Australia, 5, Overall, Australia ranks No. 5 for the second consecutive year in a row,
    Japan, 2, Since 2020, Japan has moved up one spot to No. 2.
    Switzerland, 4, As of this year, Switzerland has dropped three spots to No. 4 Best Country.
    Germany, 3, Germany is placed at No. 3 in the world and is listed in the top five for entrepreneurship, power, and agility, as well.'''},
	
    {"role": "user", "content": input_text}]

    return general_case_prompt


def generate_custom_prompt(input_text, columns):
    general_case_prompt =  [ {"role": "system", "content": '''you are en expert in csv files and converting messy text data to csv formats.
    You will accept the input_text and the columns user is looking for in the text to convert to csv, understand the context present in input_text and get the data for those columns from text to convert to csv
  '''},
	
    {"role": "user", "content": "jagadeesha 25 M jordan 20 M anitha 34 f"},
	
    {"role": "assistant", "content": '''name, age, sex
            jagadeesha, jordan, anitha
            25, 20, 34
            M, M, F'''},
			
    {"role": "user", "content": '''Canada After beating Switzerland, today, Canada stands as the number 1 country in the world. 
    Canada has the third-largest reserves of oil and is the world's fourth-major oil producing country. Australia Overall,
    Australia ranks No. 5 for the second consecutive year in a row,  Japan Since 2020, Japan has moved up one spot to No. 2.  
    Switzerland As of this year, Switzerland has dropped three spots to No. 4 Best Country.  Germany is placed at No. 3 in the world
    and is listed in the top five for entrepreneurship, power, and agility, as well.'''},
	
	{"role": "assistant", "content": '''country, rank, information
    Canada, 1, After beating Switzerland, today, Canada stands as the number 1 country in the world. Canada has the third-largest reserves of oil and is the world's fourth-major oil producing country.
    Australia, 5, Overall, Australia ranks No. 5 for the second consecutive year in a row,
    Japan, 2, Since 2020, Japan has moved up one spot to No. 2.
    Switzerland, 4, As of this year, Switzerland has dropped three spots to No. 4 Best Country.
    Germany, 3, Germany is placed at No. 3 in the world and is listed in the top five for entrepreneurship, power, and agility, as well.'''},
	
    {"role": "user", "content": input_text},
    
    {"role": "assistant", "content": columns}]

    return general_case_prompt


def create_excel_file(data):

    data = data['choices'][0]['message']['content']

    # Create a new workbook
    workbook = Workbook()

    # Select the active worksheet
    sheet = workbook.active                                 # we can even select the sheets 

    data_lists = data.split('\n')

    chars_list = ['ABCDEFGHIJKLOMNPQRSTUVWXYZ']             # for indexing the columns 
    chars_ind = 0
    for row in data_lists:
        row = row.split(',')                                # separating the words by comma
        for val_ind in range(len(row)):
            sheet[chars_list[0][chars_ind]+str(val_ind+1)] = row[val_ind]       # storing the values in cells
        chars_ind = chars_ind + 1                           # for incrementing the rows

    # Save the workbook to a new file

    workbook.save(f'./Excel_files/text_to_csv.xlsx')          


def validate_custom_API_response(data, columns):

    data = data['choices'][0]['message']['content'] 
    first_row = data.split('\n')[0]                     # getting the first row
    custom_columns = first_row.split(',')

    columns = columns.split(" ")                        # columns is in text format separated by space

    for cols in zip(custom_columns, columns):
        if cols[0]!=cols[1]:
            return False
        else:
            continue
    return True


def call_OPENAI(prompt):
    openai.api_key = os.getenv("OPEN_AI_API_KEY")
    result = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=prompt,
    max_tokens=3000,
    temperature=0.6
    )
    return result


def matching_custom_columns(result, headers, custom_prompt):
    flag = False
    for i in range(2):                                                  # for trying max of 3 times to match the columns specified
        if validate_custom_API_response(data=result, columns=headers):  # valdiating the columns 
            create_excel_file(result)
            flag=True
            break
        else:
            result = call_OPENAI(custom_prompt)
            continue
    
    if not flag:                                                        # if for all 3 tries it didn;t work out then saving the final res as it is 
        create_excel_file(result)

    return 


