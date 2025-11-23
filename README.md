# HR AI Bot - Complete README

## Project Description

**HR AI Bot** is an intelligent AI-powered Telegram bot platform that revolutionizes recruitment processes and job searching. Built with modern AI capabilities, it serves as a comprehensive HR platform providing tailored experiences for both recruiters and job seekers through sophisticated role-based interactions.

## 🚀 Key Features

### **For Recruiters & HR Professionals:**
- **Smart Vacancy Management** - Create, analyze, and optimize job postings
- **AI-Powered Candidate Search** - Intelligent matching and filtering
- **Automated Resume Analysis** - Instant screening and scoring
- **Bulk Invitation System** - Streamlined candidate outreach
- **Candidate Scoring & Ranking** - Data-driven decision support

### **For Job Seekers:**
- **AI Resume Builder** - Create professional, optimized resumes
- **Interview Preparation** - Practice questions and answer assistance
- **Skill Assessment** - Test mode with various challenges
- **Personalized Learning** - Course recommendations and career development
- **Application Tracking** - Manage your job search journey

## 🏗️ Architecture & AI Integration

This platform leverages **Spoon AI SDK** and advanced machine learning to provide:
- Natural language processing for resume and vacancy analysis
- Intelligent candidate-job matching algorithms
- Automated screening and scoring systems
- Personalized recommendations and insights

## 📁 Project Structure

```
hr-ai-bot/
├── main.py                     # Main application entry point
├── bot/                        # Core bot functionality
│   ├── roles/                  # Role-based feature separation
│   │   ├── recruiter/          # Recruiter-specific modules
│   │   │   ├── vacancy.py      # Vacancy creation & management
│   │   │   ├── search.py       # Candidate search & filtering
│   │   │   ├── analyze.py      # Resume analysis & parsing
│   │   │   └── invite.py       # Invitation management
│   │   └── candidate/          # Job seeker modules
│   │       ├── resume_builder.py    # Resume creation & optimization
│   │       ├── answer_helper.py     # Interview preparation
│   │       ├── test_mode.py         # Skills assessment
│   │       └── courses.py           # Learning recommendations
│   ├── auth/                   # Authentication & authorization
│   │   ├── register.py         # User registration system
│   │   └── role_detector.py    # Role detection & assignment
│   ├── ai/                     # AI/ML core modules
│   │   ├── client.py           # AI service client & integration
│   │   ├── vacancy_analyzer.py # Vacancy parsing & analysis
│   │   ├── candidate_scorer.py # Candidate evaluation & scoring
│   │   └── screening_bot.py    # Automated screening system
│   ├── database/               # Data persistence layer
│   │   ├── user_storage.py     # User management & profiles
│   │   └── vacancy_storage.py  # Vacancy database operations
│   └── utils/                  # Utility functions
│       ├── file_parser.py      # Document parsing (PDF, DOCX)
│       ├── validator.py        # Data validation & sanitization
│       └── logger.py           # Logging configuration
├── config/                     # Configuration management
│   ├── settings.py             # Application settings
│   ├── prompts.py              # AI prompts & templates
│   └── role_flow.py            # Conversation flows & states
├── .env                        # Environment variables
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## 🛠️ Installation & Setup

### Quick Installation Guide

#### Option A: Complete Installation (Recommended)

1. **Create and activate virtual environment**

```bash
# macOS/Linux
python3 -m venv hr-ai-env
source hr-ai-env/bin/activate

# Windows (PowerShell)
python -m venv hr-ai-env
.\hr-ai-env\Scripts\Activate.ps1
```

2. **Install all dependencies**

```bash
# Core AI dependencies
pip install spoon-ai-sdk spoon-toolkits

# Project-specific dependencies
pip install python-telegram-bot==21.3 httpx==0.25.2 pydantic==2.7.1 pyyaml==6.0.1 python-dotenv==1.0.0 pdfminer.six==20231228 python-docx==1.1.2 python-magic==0.4.27 pandas==2.0.3 scikit-learn==1.5.0 numpy==1.24.3 fastapi==0.110.0 uvicorn==0.29.0
```

#### Option B: Alternative Installation

```bash
# Simplified installation
pip install python-telegram-bot==20.6 httpx pydantic pyyaml python-dotenv pdfminer.six python-docx python-magic fastapi uvicorn spoon-ai-sdk spoon-toolkits
```

### 3. Environment Configuration

Create `.env` file with required variables:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token_here

# AI Service Configuration
AI_API_KEY=your_spoon_ai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./hr_bot.db

# Application Settings
LOG_LEVEL=INFO
DEBUG=False
```

### 4. Launch the Application

```bash
# Start the HR AI Bot
python main.py

# Alternative startup method
python -m bot.main
```

## 📦 Dependencies

### Core AI Framework
- `spoon-ai-sdk` - Advanced AI capabilities and models
- `spoon-toolkits` - Extended AI tools and utilities

### Core Application
- `python-telegram-bot==21.3` - Modern Telegram Bot API integration
- `fastapi==0.110.0` - High-performance web framework for APIs
- `uvicorn==0.29.0` - ASGI server implementation

### Data Processing & ML
- `pandas==2.0.3` - Data manipulation and analysis
- `scikit-learn==1.5.0` - Machine learning algorithms
- `numpy==1.24.3` - Numerical computing

### File Processing
- `pdfminer.six==20231228` - PDF document parsing
- `python-docx==1.1.2` - Word document handling
- `python-magic==0.4.27` - File type detection

### Utilities
- `pydantic==2.7.1` - Data validation and settings management
- `httpx==0.25.2` - Modern HTTP client
- `pyyaml==6.0.1` - YAML configuration parsing
- `python-dotenv==1.0.0` - Environment variable management

## 🎯 Usage

### For Recruiters:
1. Start chat with `@HRleadersbot`
2. Register as recruiter
3. Create vacancies with AI assistance
4. Search and screen candidates automatically
5. Manage invitations and communications

### For Job Seekers:
1. Start chat with `@HRleadersbot`
2. Build AI-optimized resume
3. Practice interview questions
4. Take skill assessments
5. Receive personalized job recommendations

## 🔧 Development

### Adding New Features:
1. Identify target role (recruiter/candidate)
2. Create module in appropriate role directory
3. Implement handlers in main application
4. Update configuration and prompts
5. Test role-specific workflows

### Code Structure Guidelines:
- Keep role-specific logic separated
- Use AI client for all intelligence features
- Follow consistent logging practices
- Maintain clear configuration separation

## 👥 Development Team

**Project Lead & AI Specialist:**  
- Анфиса Игоревна Пишук @Anfpi

**Technical Architect & Developer:**  
- Артём Витальевич Кучинский @GuruProger

## 📄 License

[Specify project https://t.me/InfiniteleadersTech! 

---

*HR AI Bot - Transforming Recruitment with ArtificiSpoon OS thank of token al Intelligence* for @denis3034


