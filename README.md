# Trivia API
This project allows users to view trivia questions and play the trivia game.
The main objectives of this project is to:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started
### Pre-requisites and Local Development
Developers using this project should already have Python3, pip, and node installed on their local machines.

#### Backend
From the backend folder run ```pip install -r requirements.txt```. All required packages are included in the requirements file.

To run the application, run the following commands:
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the ```__init__.py``` file in our flaskr folder.

The application is run on ```http://127.0.0.1:5000/``` by default and is a proxy in the frontend configuration.

#### Frontend
From the frontend folder, run the following commands to start the client:
```
npm install // only once to install dependencies
npm start
```
By default, the frontend will run on ```localhost:3000```.

#### Tests
In order to run tests, navigate to the backend folder and run the following commands:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
The first time you run the tests, omit the dropdb command.

## API Reference
### Getting Started
- Base URL: This app can only run locally. The backend app is hosted at default, ```http://127.0.0.1:5000/```, which is set as a proxy in the frontend conifguration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling
Errors are returned as JSON objects in the following format:
```
  {
    'success': False,
    'error': 400,
    'message': "Bad Request"
  }
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints
#### GET /categories
- General:
  - Returns a dictionary of categories and success value.
- Sample: ```curl http://127.0.0.1:5000/categories```
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
#### GET /questions
- General:
  - Returns a list of question objects, dictionary of categories, success value, and total number of questions.
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: ```curl http://127.0.0.1:5000/questions```
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

#### GET /categories/<int:id>/questions
- General:
  - Returns the specific category, list of question objects in the specific category, success value, and total number of questions in that specific category.
- Sample: ```curl http://127.0.0.1:5000/categories/1/questions```
```
{
  "current_category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "total_questions": 3
}

```

#### POST /questions
- General:
  - Creates a new question using the submitted question, answer, difficulty, and category. 
  - Returns the id of the created question, success value, and total numbers of question.
- Sample: ```curl -X POST -H "Content-Type: application/json" -d '{"question": "What is the largest planet in the Solar System?", "answer": "Jupiter", "difficulty": "1", "category": "1"}' http://127.0.0.1:5000/questions```
```
{
  "created": 24, 
  "question": {
    "answer": "Jupiter", 
    "category": 1, 
    "difficulty": 1, 
    "id": 24, 
    "question": "What is the largest planet in the Solar System?"
  }, 
  "success": true, 
  "total_questions": 20
}
```

#### POST /questions/search
- General:
  - Searches for questions that matches the searchTerm
  - Returns a list of question objects, success value, and total number of questions that matched the search.
- Sample: ```curl -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Tim"}' http://127.0.0.1:5000/questions/search```
```
{
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}
```

#### POST /quizzes
- General:
  - Allows the user to play the quiz game.
  - Returns a random question, list of IDs of previous questions, success value, and total number of questions.
- Sample: ```curl -X POST -H "Content-Type: application/json" -d '{"previous_questions": [16], "quiz_category": {"id": "2", "type": "Art"}}' http://127.0.0.1:5000/quizzes```
```
{
  "previousQuestion": [
    16
  ], 
  "question": {
    "answer": "One", 
    "category": 2, 
    "difficulty": 4, 
    "id": 18, 
    "question": "How many paintings did Van Gogh sell in his lifetime?"
  }, 
  "success": true, 
  "totalQuestions": 4
}
```

#### DELETE /questions/<int:id>
- General:
  - Deletes the question of the given ID if it exists. 
  - Returns the id of the deleted question, success value, list of question objects, and total number of questions.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/questions/20?page=2```
```
{
  "deleted": 20, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Jupiter", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "What is the largest planet in the Solar System?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

## Deployment N/A
## Authors
Patricia Luz

## Acknowledgements
Udacity
