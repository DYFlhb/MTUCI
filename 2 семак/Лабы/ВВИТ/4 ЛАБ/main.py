from fastapi import FastAPI, status
from pydantic import BaseModel
import pyjokes

app = FastAPI ()

class Joke(BaseModel):
    friend: str
    joke: str
class JokeInput(BaseModel):
  friend: str

@app.get("/", status_code = status.HTTP_200_OK)
def joke():
 return pyjokes.get_joke()

@app.post('/', status_code = status.HTTP_201_CREATED)
def create_joke(joke_input: JokeInput):
 return Joke(friend=joke_input.friend, joke=pyjokes.get_joke())