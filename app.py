from flask import Flask, request, render_template, send_file, redirect, url_for
import os
from dotenv import load_dotenv
import openai
from utils import generate_general_prompt, generate_custom_prompt, create_excel_file, validate_custom_API_response, matching_custom_columns, call_OPENAI

app = Flask(__name__)

file_names = {}


# Route for the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Route for processing using OpenAI API
@app.route('/process', methods=['POST', 'GET'])
def process():
    input_text = request.form.get('input_text')
    general_prompt = generate_general_prompt(input_text)
    result = call_OPENAI(general_prompt)
    print(" Response from  OPENAI : ", result)
    create_excel_file(result)
    data = result['choices'][0]['message']['content']
    return redirect(url_for('results', data=data ))



# Route for custom headers using OpenAI API
@app.route('/custom_page', methods=['POST', 'GET'])
def custom_page():
    return render_template('custom.html')


# route for processing the custom headers 
@app.route('/custom_process', methods=['GET', 'POST'])
def custom_process():
    headers = request.form.get('custom_headers')
    input_text = request.form.get('input_text')
    custom_prompt = generate_custom_prompt(input_text, headers)
    print('custom prompt generated is : ', custom_prompt)
    result = call_OPENAI(custom_prompt)
    print(" Response from  OPENAI : ", result)

    matching_custom_columns(result, headers, custom_prompt)
    data = result['choices'][0]['message']['content']
    return redirect(url_for('results', data=data))


@app.route('/results', methods=['GET'])
def results():
    # sample = get_sample(data)                               # getting the sample for 5 rows for users to see 

    data = request.args.get('data')

    print('after receiving :', data)

    data = data.split('\n')
    data = data[:min(5, len(data))]                           # sampling to min 5 or if data < length 5

    result = []
    for item in data:
        print(item)
        result.append(
            # 'first':item.split()[0],
            # 'second':item.split()[1],
            # 'third':item.split()[2]
            [i for i in item.split()]

        )
    return render_template('show_results.html', data=result)



@app.route('/download_result', methods = ['GET'])
def download_result():
    return send_file(path_or_file='./Excel_files/text_to_csv.xlsx', download_name='text_to_excel.xlsx', as_attachment=True,)



if __name__ == '__main__':
    app.run(debug=True)



