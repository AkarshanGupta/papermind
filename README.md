# Research Paper Summarizer

A tool to process research papers in PDF format and generate concise summaries of key sections like Abstract, Introduction, Methodology, Results, Discussion, and Conclusion.

## Introduction

Research papers often contain valuable insights but are lengthy and time-consuming to read. This tool streamlines the process by automatically summarizing key sections, allowing researchers and professionals to quickly grasp the essence of a paper without going through it entirely.

## Objective

The primary objective of this project is to leverage AI and NLP technologies to:

- Automate the extraction and summarization of research papers.
- Provide concise and accurate summaries for various sections of a paper.
- Improve accessibility and productivity for researchers and professionals.

## Features

- Extracts text from uploaded PDF files.
- Identifies and summarizes key sections of the research paper.
- Utilizes the [Flan-T5](https://huggingface.co/google/flan-t5-base) model for summarization.
- Handles long texts effectively by truncating and processing content efficiently.
- User-friendly interface built with [Gradio](https://gradio.app/).

## Technology

The project utilizes the following technologies:

- **Hugging Face Transformers**: For leveraging state-of-the-art NLP models like Flan-T5.
- **Gradio**: To create an interactive and user-friendly web application.
- **PyPDF2**: For extracting text from PDF files.
- **NLTK**: For natural language processing tasks like sentence tokenization.
- **Python**: The primary programming language for the project.

## Demo

Upload a research paper in PDF format to receive summarized insights for each section.

## Requirements

- Python 3.8+
- pip (Python package manager)
- GPU recommended for faster processing, but not required.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/research-paper-summarizer.git
cd research-paper-summarizer
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Download NLTK resources:

```bash
python -c "import nltk; nltk.download('punkt')"
```

## Usage

1. Run the application:

```bash
python app.py
```

2. Open the Gradio interface in your browser. Upload a research paper in PDF format to get section-wise summaries.

## File Structure

```
.
├── app.py              # Main application code
├── requirements.txt    # Python dependencies
├── nltk_data/          # NLTK data directory (auto-downloaded)
└── README.md           # Project documentation
```

## Example Output

When you upload a research paper, you will receive summaries for sections like:

```json
{
  "abstract": "This study explores...",
  "introduction": "In recent years, ...",
  "methodology": "The experiment was conducted...",
  "results": "The findings indicate...",
  "discussion": "These results suggest...",
  "conclusion": "In summary, the study shows..."
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for the Flan-T5 model.
- [Gradio](https://gradio.app/) for the easy-to-use interface.
- [NLTK](https://www.nltk.org/) for text tokenization.
