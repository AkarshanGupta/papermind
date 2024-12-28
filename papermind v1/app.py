import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize
import re
import os
import io

# Configure NLTK data directory
nltk_data_path = "./nltk_data"
if os.path.exists(nltk_data_path):
    os.environ['NLTK_DATA'] = nltk_data_path

# Ensure NLTK data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK 'punkt' resource...")
    nltk.download('punkt', quiet=True)


class ResearchPaperProcessor:
    def __init__(self, model_name="google/flan-t5-base"):
        """
        Initialize the research paper processor.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)

    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extract text from the uploaded PDF.
        """
        try:
            pdf_file = io.BytesIO(pdf_file)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            full_text = ""

            for page in pdf_reader.pages:
                text = page.extract_text()
                full_text += text + "\n"

            return full_text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")

    def extract_sections(self, text: str) -> dict:
        """
        Extract common sections from the research paper text.
        """
        sections = {
            "abstract": "",
            "introduction": "",
            "methodology": "",
            "results": "",
            "discussion": "",
            "conclusion": ""
        }

        patterns = {
            "abstract": r"(?i)abstract\s*(.*?)(?=\n\s*(?:introduction|1\.)|$)",
            "introduction": r"(?i)(?:introduction|1\.)\s*(.*?)(?=\n\s*(?:methodology|methods|2\.)|$)",
            "methodology": r"(?i)(?:methodology|methods|2\.)\s*(.*?)(?=\n\s*(?:results|3\.)|$)",
            "results": r"(?i)(?:results|findings|3\.)\s*(.*?)(?=\n\s*(?:discussion|4\.)|$)",
            "discussion": r"(?i)(?:discussion|4\.)\s*(.*?)(?=\n\s*(?:conclusion|5\.)|$)",
            "conclusion": r"(?i)(?:conclusion|5\.)\s*(.*?)(?=\n\s*(?:references|bibliography)|$)"
        }

        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            if match:
                sections[section] = match.group(1).strip()

        return sections

    def summarize_section(self, section_text: str) -> str:
        """
        Summarize a given section of text.
        """
        if not section_text:
            return "No content available for summarization."

        try:
            input_text = f"Summarize: {section_text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=1024).to(self.device)
            outputs = self.model.generate(inputs.input_ids, max_length=150, num_beams=2, temperature=0.7)
            summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return summary
        except Exception as e:
            return f"Error during summarization: {str(e)}"

    def process_paper(self, pdf_file) -> dict:
        """
        Process the uploaded research paper and return summaries of sections.
        """
        full_text = self.extract_text_from_pdf(pdf_file)
        sections = self.extract_sections(full_text)

        summaries = {}
        for section_name, section_content in sections.items():
            summaries[section_name] = self.summarize_section(section_content)

        return summaries


def create_interface():
    """
    Create the Gradio interface for the summarization tool.
    """
    processor = ResearchPaperProcessor()

    def process_file(file):
        if not file:
            return "Error: Please upload a valid PDF file."
        try:
            summaries = processor.process_paper(file)
            return summaries
        except Exception as e:
            return {"Error": str(e)}

    iface = gr.Interface(
        fn=process_file,
        inputs=gr.File(label="Upload Research Paper (PDF)", type="binary", file_types=[".pdf"]),
        outputs=gr.JSON(label="Section Summaries"),
        title="Research Paper Summarizer",
        description="Upload a research paper in PDF format to get summaries of its sections.",
        theme=gr.themes.Soft()
    )

    return iface


if __name__ == "__main__":
    iface = create_interface()
    iface.launch()
