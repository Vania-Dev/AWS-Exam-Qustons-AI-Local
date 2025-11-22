# AWS Exam Questions AI Processor

An intelligent automation system that processes AWS certification exam questions from images and uploads them to Notion with AI-powered analysis and explanations.

## 🚀 Features

- **OCR Text Extraction**: Converts exam question images to readable text
- **AI-Powered Analysis**: Uses local LLM (Ollama) to analyze questions and provide explanations
- **Notion Integration**: Automatically uploads structured questions to Notion pages
- **Multi-language Support**: Questions in English, explanations in Spanish
- **Automated Workflow**: Complete pipeline from image to organized knowledge base

## 🏗️ Architecture

```
Image Input → OCR Processing → AI Analysis → Notion Upload
     ↓              ↓              ↓            ↓
  Raw Image    Text Extract   JSON Structure  Formatted Page
```

## 📋 Prerequisites

- Python 3.8+
- Ollama with llama3.2:3b model
- Notion API access
- CUDA-compatible GPU (optional, for faster processing)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Vania-Dev/AWS-Exam-Qustons-AI-Local.git
   cd AWS_Exam_Questions_AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama and model**
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   ollama pull llama3.2:3b
   ```

4. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

## ⚙️ Configuration

Create a `.env` file with the following variables:

```env
NOTION_TOKEN=your_notion_integration_token
NOTION_PARENT_PAGE_ID=your_notion_page_id
```

### Getting Notion Credentials

1. Go to [Notion Developers](https://developers.notion.com/)
2. Create a new integration
3. Copy the Internal Integration Token
4. Share your target page with the integration
5. Copy the page ID from the URL

## 🚀 Usage

### Basic Usage

```python
from aws_question_agent import graph

# Process a single image
input_state = {"file_path": "path/to/your/question_image.png"}
result = graph.invoke(input_state)
```

### Command Line Usage

```bash
python aws_question_agent.py
```

### Batch Processing

```python
import os
from aws_question_agent import graph

# Process multiple images
image_folder = "images/"
for filename in os.listdir(image_folder):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        input_state = {"file_path": os.path.join(image_folder, filename)}
        graph.invoke(input_state)
```

## 📁 Project Structure

```
AWS_Exam_Questions_AI/
├── utils/
│   ├── ocr.py          # OCR text extraction 
│   ├── llm.py          # AI model interaction
│   └── notion.py       # Notion API integration
├── images/             # Input images directory
├── outputs/            # Processed images (debug)
├── aws_question_agent.py  # Main workflow orchestrator
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🔧 Core Components

### OCR Processing (`utils/ocr.py`)
- Image preprocessing and enhancement
- Text extraction using EasyOCR
- Dark background detection and inversion
- Noise reduction and adaptive thresholding

### AI Analysis (`utils/llm.py`)
- Local LLM integration with Ollama
- Structured prompt engineering
- JSON response parsing
- Multi-language explanation generation

### Notion Integration (`utils/notion.py`)
- API payload construction
- Toggle block formatting
- Color-coded correctness indicators
- Automated page updates

### Workflow Orchestration (`aws_question_agent.py`)
- LangGraph state management
- Pipeline coordination
- Error handling and logging
- Modular processing steps

## 📊 Output Format

The system generates structured Notion pages with:

- **Numbered Questions**: Automatically numbered exam questions
- **Toggle Answers**: Expandable answer options (A, B, C, D)
- **Color Coding**: Green for correct answers, red for incorrect
- **Explanations**: Detailed Spanish explanations for each option

## 🔍 Example Workflow

1. **Input**: Image containing AWS exam question
2. **OCR**: Extract text from image
3. **AI Analysis**: Process with local LLM
4. **Output**: Structured Notion page with formatted question

## 🛡️ Error Handling

- **Image Processing**: Validates file existence and format
- **OCR Failures**: Handles empty text extraction
- **AI Responses**: Validates JSON format
- **Notion API**: Manages upload failures and retries

## 🎯 Use Cases

- **Exam Preparation**: Organize AWS certification questions
- **Study Groups**: Share structured question banks
- **Knowledge Management**: Build searchable question databases
- **Training Materials**: Create formatted study resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check existing GitHub issues
- Create a new issue with detailed description
- Include error logs and system information

## 🔮 Future Enhancements

- [ ] Support for multiple question formats
- [ ] Batch processing interface
- [ ] Custom explanation languages
- [ ] Integration with other note-taking platforms
- [ ] Question difficulty assessment
- [ ] Performance analytics dashboard


Craft it with the kind of ❤️ that leaves fingerprints on the soul.