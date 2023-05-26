## Import all the dependent libraries
import PyPDF2

pdf_path = r"/content/chapter-2.pdf"
pdf_file = open(pdf_path, 'rb')
pdf_reader = PyPDF2.PdfReader(pdf_file)

text_content = ''
for page in pdf_reader.pages:
    text_content += page.extract_text()

pdf_file.close()

text_file_path = r"/content/New Text Document.txt"
with open(text_file_path, 'w', encoding='utf-8') as text_file:
    text_file.write(text_content)
file = open(r"/content/New Text Document.txt", encoding = 'utf-8')
text = file.read()
import nltk

nltk.download('punkt')

from nltk.tokenize import sent_tokenize

# Function to extract important lines from a paragraph
def extract_important_lines(paragraph, num_lines):
    # Tokenize the paragraph into sentences
    sentences = sent_tokenize(paragraph)
    
    # Calculate the importance score for each sentence (example: sentence length)
    importance_scores = [len(sentence) for sentence in sentences]
    
    # Sort the sentences based on importance score (in descending order)
    sorted_sentences = [sentence for _, sentence in sorted(zip(importance_scores, sentences), reverse=True)]
    
    # Extract the specified number of important lines
    important_lines = sorted_sentences[:num_lines]
    # Join the important lines to form a shortened paragraph
    shortened_paragraph = ' '.join(important_lines)
    
    return shortened_paragraph

paragraph = text

# Specify the number of important lines to extract
num_lines = 10

# Extract important lines and obtain the shortened paragraph
shortened_paragraph = extract_important_lines(paragraph, num_lines)
import openai

# Set up your OpenAI API credentials
openai.api_key = "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"
import openai

def mca_questions(paragraph, num_questions, num_options, num_correct_answers):
    prompt = f"Generate five multiple-choice questions with four options and with multiple correct answers based on the following paragraph:\n\n{paragraph}\n\n"
    questions = ""
    options = ["A", "B", "C", "D"]

    for i in range(num_questions):
        question_number = i + 1

        # Generate options
        option_choices = ""
        correct_answers = []
        for j in range(num_options):
            option_choice = options[j]
            option_choices += f"{option_choice}) [Option {option_choice}]\n"

            # Keep track of correct answers
            if j < num_correct_answers:
                correct_answers.append(option_choice)

        # Construct the question
        question = f"Q: {option_choices}"

        # Append the correct answer choices
        question += f"Correct Options: ({', '.join(correct_answers)})\n\n"

        questions += question

    # Concatenate the prompt and questions
    complete_prompt = prompt + questions

    # Generate multiple-choice questions
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=complete_prompt,
        max_tokens=300,
        n=2,
        stop=None,
        temperature=0.8
    )

    # Extract the generated questions from the response
    generated_questions = response.choices[0].text.strip().split("\n\nCorrect Options:")

    return generated_questions



num_questions = 5
num_options = 4
num_correct_answers = 2

for i in range(num_questions):
     generated_questions = mca_questions(shortened_paragraph, num_questions, num_options, num_correct_answers)
     for i, question in enumerate(generated_questions):
            print(i , question)

