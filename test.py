import requests

url = 'https://texlive.net/cgi-bin/latexcgi'
latex_code = '\documentclass{article}\n\n\\begin{document}\n\n\\begin{center}\n{\\LARGE \\textbf{Muhammad Usman}}\n\\end{center}\n\n\\begin{center}\nHouse No. 1, Lane 10, Royal Avenue Near Comsats Tarlai kalan\\\\\n03069116931\\\\\niammuhammadusman1@gmail.com\\\\\n\\end{center}\n\n\\vspace{0.2in}\n\n\\textbf{Objective:}\n\nTo obtain a position that utilizes my skills and experience to contribute to an organization\'s success.\n\n\\vspace{0.2in}\n\n\\textbf{Skills:}\\\\\n- (Insert relevant skills here)\n\n\\vspace{0.2in}\n\n\\textbf{Awards:}\\\\\n- (Insert relevant awards here)\n\n\\vspace{0.2in}\n\n\\textbf{Professional Affiliations:}\\\\\n- (Insert relevant professional affiliations here)\n\n\\vspace{0.2in}\n\n\\textbf{References:}\\\\\n- (Insert relevant references here)\n\n\\vspace{0.2in}\n\n\\textbf{Additional Information:}\\\\\n- (Insert any relevant additional information here)\n\n\\vspace{0.2in}\n\n\\textbf{Education:}\\\\\n- (Insert relevant education here)\n\n\\vspace{0.2in}\n\n\\textbf{Work Experience:}\\\\\n- (Insert relevant work experience here)\n\n\\vspace{0.2in}\n\n\\textbf{Internship Experience:}\\\\\n- (Insert relevant internship experience here)\n\n\\end{document}'

# Prepare the form data
form_data = {
    'return': 'pdf',
    'engine': 'pdflatex',
    'filecontents[]': latex_code.encode('utf-8'),
    'filename[]': 'document.tex'
}

# Send the POST request
response = requests.post(url, files=form_data)

if response.status_code == 200:
    print(response.content)
    # Save the PDF file
    with open('document.pdf', 'wb') as file:
        file.write(response.content)
    print('PDF saved successfully.')
else:
    print('PDF compilation failed. Status code:', response.status_code)