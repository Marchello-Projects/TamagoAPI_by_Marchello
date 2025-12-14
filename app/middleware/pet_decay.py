from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import select
from datetime import datetime, timezone
from database.models import Pet
from configs.configdb import async_session

class PetDecayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        async with async_session() as db:
            result = await db.execute(select(Pet))
            pets = result.scalars().all()

            now = datetime.now(timezone.utc)

            for pet in pets:
                elapsed_seconds = (now - pet.last_updated).total_seconds()
                if elapsed_seconds <= 0:
                    continue

                elapsed_minutes = elapsed_seconds / 60
                decay_per_minute = 0.5  
                max_decay = 50  

                decay = min(decay_per_minute * elapsed_minutes, max_decay)

                pet.hunger = max(pet.hunger - decay, 0)
                pet.energy = max(pet.energy - decay, 0)
                pet.happiness = max(pet.happiness - decay, 0)

                pet.last_updated = now
                db.add(pet)

            await db.commit()

        response = await call_next(request)
        return response