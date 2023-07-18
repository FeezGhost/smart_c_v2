import re


def convert_latex_format(latex_code):
    # Remove newlines and extra spaces
    latex_code = re.sub(r"\n\s*", "", latex_code)

    # Remove unnecessary commands
    latex_code = re.sub(r"\\usepackage\{.*?\}", "", latex_code)
    latex_code = re.sub(r"\\geometry\{.*?\}", "", latex_code)
    latex_code = re.sub(r"\\subsection\*", r"\\section*", latex_code)
    latex_code = re.sub(r"\\\\",r"\\", latex_code)
    return latex_code


laa = convert_latex_format("\\documentclass{letter}\n\n\\usepackage{geometry}\n\\geometry{letterpaper, margin=1in}\n\n\\begin{document}\n\n\\begin{center}\n\t\\textbf{Muhammad Usman} \\\\\n\t\\textbf{House No. 1, Lane 10, Royal Avenue Near Comsats Tarlai kalan} \\\\\n\t\\textbf{03069116931} \\\\\n\t\\textbf{iammuhammadusman1@gmail.com}\n\\end{center}\n\n\\bigskip\n\nDear Hiring Manager,\n\nI am writing to express my interest in the \\textbf{[Job Title]} position at \\textbf{[Company Name]}. As a highly motivated individual with a [Number of years] years of experience in [Sector related to job], I believe that I possess the necessary skills and experience to excel in this role.\n\nDuring my role as [Job Title] at [Previous Company], I developed [Skill relevant to job], managed [Number of people or projects], and [Accomplishment related to job]. Moreover, while working at [Previous Company], I gained [Experience relevant to job] and learned [Knowledge related to job].\n\nI am eager to bring [Skill relevant to job], [Experience relevant to job] and my passion for [Sector related to job] to \\textbf{[Company Name]}. My experience honed my skills in [Skill relevant to job], and my passion for [Sector related to job] only continues to grow. In addition to my qualifications, I am a [Personal trait relevant to job] who recognizes the importance of [Core value of the company], and believes that they align closely with those of \\textbf{[Company Name]}.\n\nI am excited at the prospect of joining \\textbf{[Company Name]} and look forward to discussing my qualifications in further detail. Thank you for considering my application.\n\nSincerely,\n\nMuhammad Usman\n\n\\end{document}")
print(laa)