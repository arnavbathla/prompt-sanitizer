from flask import Flask, request, jsonify
import re

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

    # Return the sanitized prompt
    return jsonify({'sanitized_prompt': sanitized_prompt})

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
