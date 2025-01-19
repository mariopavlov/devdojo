# DevDojo - Coding Practice Environment

DevDojo is a personal coding practice environment that helps you improve your programming skills through spaced repetition learning. It allows you to collect coding problems from various sources, organize them, and practice them based on your mastery level.

## Features

- Add coding problems with descriptions and source URLs
- Tag problems for better organization
- Multiple solutions per problem
- Test cases for each solution
- Spaced repetition system for optimal learning
- Track mastery level for each problem

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your database configuration:
```
DATABASE_URL=sqlite:///./devdojo.db
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Problems
- `POST /problems/` - Create a new problem
- `GET /problems/` - List all problems
- `GET /problems/{problem_id}` - Get a specific problem

### Solutions
- `POST /solutions/` - Add a solution to a problem
- `GET /problems/{problem_id}/solutions/` - Get all solutions for a problem

### Test Cases
- `POST /test-cases/` - Add test cases for a solution

### Practice
- `GET /practice/` - Get problems due for practice
- `POST /practice/{problem_id}/complete` - Complete a practice session

## Database Schema

The application uses the following main entities:
- Problems
- Solutions
- Test Cases
- Tags
- Practice Records

## Contributing

Feel free to submit issues and enhancement requests!
