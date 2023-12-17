from flask import Flask, request, jsonify
import re
import os

app = Flask(__name__)

def sanitize_prompt(prompt, keywords_to_remove):
    """
    Sanitizes the prompt to avoid injection attacks by removing or encoding dangerous characters and patterns.
    """
    # Remove SQL injection and command injection risks
    prompt = re.sub(r';|--', '', prompt)

    # Remove or encode HTML/XML tags to prevent XSS attacks
    prompt = re.sub(r'<[^>]*>', '', prompt)

    # Remove or escape characters that are typical in shell injection attacks
    prompt = re.sub(r'[\`\|\&\;\$]', '', prompt)

    # Remove backslashes to prevent escape sequences
    prompt = prompt.replace('\\', '')

    # Construct a pattern to remove any text following any of the keywords
    pattern_to_remove = r'(?i)(' + '|'.join(re.escape(keyword) for keyword in keywords_to_remove) + r').*'
    prompt = re.sub(pattern_to_remove, '', prompt)

    # Remove potentially dangerous characters to prevent other types of injections
    prompt = re.sub(r'[<>{}]', '', prompt)

    return prompt.strip()

def remove_unwanted_files(prompt):
    """
    Removes files that are specified in the prompt.
    This function must be used with extreme caution to avoid unintended deletions.
    """
    # Regex pattern to find file paths in the prompt
    file_pattern = r'\b(?:/[^/ ]*)+/?\b'
    file_paths = re.findall(file_pattern, prompt)

    for path in file_paths:
        # Ensure the path is a valid file and not a directory to prevent directory deletion
        if os.path.isfile(path):
            os.remove(path)

    return

# You can define your array of keywords here
keywords_to_remove = ['forget', 'ignore', 'skip', 'omit', 'stop']

@app.route('/sanitize', methods=['POST'])
def sanitize():
    """
    API endpoint to sanitize prompts to be used with LLMs.
    """
    # Get the prompt from the request JSON
    data = request.json
    prompt = data.get('prompt', '')

    # Check if a prompt was provided
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    # Sanitize the prompt
    sanitized_prompt = sanitize_prompt(prompt, keywords_to_remove)

    # Remove unwanted files
    remove_unwanted_files(sanitized_prompt)

    # Return the sanitized prompt
    return jsonify({'sanitized_prompt': sanitized_prompt})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
