# AIVA v2 - AI Academic Assistant

AIVA is an intelligent academic assistant that helps students manage tasks, plan studies, and organize their workload using AI-powered natural language processing.

## Features

- 🤖 **AI-Powered Task Management** - Convert natural language into structured tasks using OpenAI API
- 📋 **Smart Task Organization** - Categorize tasks and set priorities
- 📅 **Study Planning** - Generate personalized study plans
- 💬 **Conversation History** - Maintain context across multiple interactions
- ⚠️ **Workload Detection** - Identify and alert when tasks are overloaded
- 📊 **Task Tracking** - Track completion status and deadlines

## Project Structure

```
AIVA-v2/
├── backend/
│   ├── app/
│   │   ├── ai_service.py          # OpenAI integration & intent processing
│   │   ├── conversation_service.py # Conversation history management
│   │   ├── database.py             # Database connection setup
│   │   ├── date_utils.py           # Date utility functions
│   │   ├── models.py               # SQLAlchemy models (Task, etc.)
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── task_service.py         # Task management logic
│   │   └── main.py                 # FastAPI app entry point
│   ├── requirements.txt            # Python dependencies
│   └── .env.example                # Environment variables template
├── frontend/                       # Frontend application
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## Available Intents

AIVA supports the following conversational intents:

- `create_task` - Add a new task
- `update_task` - Modify an existing task
- `delete_task` - Remove a task
- `today_plan` - Get today's task plan
- `list_tasks` - List all tasks
- `check_overload` - Check if tasks are overloaded
- `generate_study_plan` - Generate a personalized study plan

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- OpenAI API key

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AIVA-v2
```

### 2. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Then edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_api_key_here
```

> **⚠️ Security Note:** Never commit `.env` to git. Use `.env.example` as a template.

## Running the Application

### Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Access the interactive API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend

```bash
cd frontend
# Run frontend setup commands here
```

## Example Usage

### Create a Task

```
User: "Add DSA practice tomorrow for 2 hours"

AIVA Response:
{
  "intent": "create_task",
  "title": "DSA practice",
  "category": "Competitive",
  "estimated_hours": 2,
  "deadline": "tomorrow"
}
```

### Generate Study Plan

```
User: "Plan my study for next 3 days"

AIVA Response:
{
  "intent": "generate_study_plan",
  "days": 3,
  "plan": [...study details...]
}
```

## Database

The application uses SQLAlchemy ORM with a database for persisting:

- Tasks (title, category, deadline, priority, completion status)
- Conversation history
- Study plans

## Technology Stack

- **Backend Framework:** FastAPI
- **Database ORM:** SQLAlchemy
- **AI/ML:** OpenAI API
- **HTTP Server:** Uvicorn
- **Environment Management:** python-dotenv

## Dependencies

See [requirements.txt](backend/requirements.txt) for the complete list of dependencies.

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## Security

- ✅ API keys are protected via `.gitignore`
- ✅ Use environment variables for sensitive data
- ✅ Never commit `.env` files
- ✅ Regenerate API keys if exposed

## License

[Add your license here]

## Support

For issues and questions, please open an issue in the repository.

---

**Made with ❤️ for academic success**
