from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_models import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session

router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def create(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    new_course = CourseModel(title=course.title, classes=course.classes, hours=course.hours)
    db.add(new_course)
    await db.commit()

    return new_course


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CourseSchema])
async def get_all(db: AsyncSession = Depends(get_session)):
    # courses = session.execute(select(CourseModel)).all()
    async with db as session:
        query = select(CourseModel)
        result = await session.execute(query)
        courses: List[CourseModel] = result.scalars().all()

        return courses


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_by_id(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CourseModel).filter(CourseModel.id == id)
        result = await session.execute(query)
        course = result.scalar_one_or_none()

        if not course:
            raise HTTPException(detail='Course not found', status_code=status.HTTP_404_NOT_FOUND)

        return course


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=CourseSchema)
async def update(id: int, course_schema: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        course = await get_by_id(id, db)

        course.title = course_schema.title
        course.classes = course_schema.classes
        course.hours = course_schema.hours

        await session.commit()

        return course


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        course = await get_by_id(id, db)

        await session.delete(course)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
