from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.pet import PetResponse, PetCreate, PetUpdate
from configs.configdb import get_db
from routes.auth import get_current_user
from database.models import Pet, User

router = APIRouter(prefix='/pets', tags=['Pets & Actions'])

def check_not_pet(pet):
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Pet not found or access denied'
        )

@router.post('/create', response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    pet_create: PetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet = await db.execute(
        select(Pet).where(
            Pet.name == pet_create.name,
            Pet.owner_id == current_user.id
        )
    )
    
    existing_pet = get_pet.scalar_one_or_none()
    if existing_pet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Pet already exists'
        )
    
    new_pet = Pet(
        name=pet_create.name,
        owner_id=current_user.id
    )

    db.add(new_pet)
    await db.commit()
    await db.refresh(new_pet)

    return new_pet

@router.get('/{pet_id}', response_model=PetResponse)
async def get_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Pet).where(
            Pet.id == pet_id,
            Pet.owner_id == current_user.id
        )
    )

    pet = result.scalar_one_or_none()

    check_not_pet(pet)

    return pet

@router.patch('/{pet_id}', response_model=PetResponse)
async def update_pet(
    pet_id: int,
    pet_update: PetUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet = await db.execute(
        select(Pet).where(
            Pet.id == pet_id,
            Pet.owner_id == current_user.id
        )
    )

    pet = get_pet.scalar_one_or_none()

    check_not_pet(pet)

    if pet_update.name is not None:
        pet.name = pet_update.name

    await db.commit()
    await db.refresh(pet)

    return pet

@router.delete('/{pet_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet(
    pet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_pet = await db.execute(
        select(Pet).where(
            Pet.id == pet_id, 
            Pet.owner_id == current_user.id
        )
    )
    
    pet = get_pet.scalar_one_or_none()

    check_not_pet(pet)
    
    await db.delete(pet)
    await db.commit()

    await db.execute(text("ALTER SEQUENCE pets_id_seq RESTART WITH 1"))
    await db.commit()

    return None