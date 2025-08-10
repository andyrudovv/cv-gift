# CV Generator Bot

A Telegram bot that generates basic CVs using AI. The bot collects user information and creates a beautifully formatted PDF CV using Gemini AI.

## 🌟 Features

- Interactive CV data collection through Telegram
- AI-powered CV content generation using Google's Gemini AI
- basic PDF generation with custom formatting
- Docker containerization for easy deployment
- Microservice architecture (separate bot and backend services)

## 🏗 Architecture

The project consists of two main services:

1. **Telegram Bot Service**: Handles user interactions and PDF generation
2. **Backend Service**: Manages AI integration and CV content generation

## 🛠 Tech Stack

- Python 3.11
- aiogram 3.x (Telegram Bot Framework)
- FastAPI (Backend API)
- Google Gemini AI
- ReportLab (PDF Generation)
- Docker & Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Google Gemini API Key

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cv-generator-bot.git
cd cv-generator-bot
```

2. Create `.env` file in the project root:
```env
TELEGRAM_BOT_KEY=your_telegram_bot_token
GEMINI_API_KEY=your_gemini_api_key
```

3. Build and run the services:
```bash
docker compose up --build
```

## 💬 Bot Commands
- `/generate_cv` - Begin CV generation process

## 📝 CV Generation Process

1. The bot will ask for your:
   - Full Name
   - Work Experience
   - Education
   - Technical Skills

2. The AI will generate basic CV content

3. You'll receive a formatted PDF with your CV

## 🐳 Docker Services

### Bot Service
- Handles Telegram interactions
- Manages conversation flow
- Generates PDF documents

### Backend Service
- Processes AI requests
- Generates CV content
- Provides RESTful API


### Local Development
 Run services separately for development:
```bash
docker-compose up --build

Contributions are welcome! Please feel free to submit a Pull Request.
