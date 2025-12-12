from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title='TamagoAPI',
    description='Tamagotchi API - A fun API to manage virtual pets. Users can create pets, check their state (hunger, happiness, energy), and interact with them by feeding, playing, or putting them to sleep. JWT authentication secures user actions.',
    contact={
        "name": "Marchello",
        "url": "https://github.com/Marchello-Projects",
        "email": "paskalovmarkus@gmail.com",
    }
)

if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', port=8000, reload=True)