""" DATASTORE module contains current data store structures. """
import asyncio
import re
from datetime import timezone, datetime
from typing import List, Optional, Union, NamedTuple
from uuid import uuid4

from pydantic import BaseModel, field_serializer
from pydantic_core import from_json
from redis.asyncio import Redis
from redis.commands.search.document import Document
from redis.commands.search.field import Field, TextField, NumericField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from redis.commands.search.result import Result
from redis.commands.search.query import Query
from redis.exceptions import ResponseError

# from app.logger import logger
""" ******************************************************** DONE *********************************************************
    reference: notion tech spec/notes;
    
    class DriverInfo(NamedTuple):
        
        number: int
        
        full_name: str
        
    
    class Meeting(BaseModel):
    
			year: int
			
			meeting_name: str # look at typing library and strings
			
			session_key: int  # foreign key; via openF1 and the session endpoint;
			
			participating_drivers: List[DriverInfo] # list of DriverInfo tuples;
		
		
		class Driver(BaseModel):
		
			session_key: int  # foreign key
			
			driver_number: int
			
			radio_transcript: List[Dict{}]
			
			lap_avg_sentiment: float
			
			team_name: str
			
			full_name: str
			~OPTIONAL~
    
			mode_lap_time: float
				# lap_duration - requires laps endpoint to be called, might be for v2 


    domain model;
    document model;
    TBD: collection model -> class YourCollectionModel(BaseModel):
                                total: int
                                items: List[YourDocumentModel]
    
    repo model:
    class YourRepository:
        def __init__(self, redis: Redis):
            self.redis = redis
            self.INDEX = "your-index"
            self.PREFIX = "your-prefix:"
        
        async def initialize(self) -> None:
            await self.create_index_if_not_exists()
        
        # Implement CRUD operations following the same patterns
        # reference redis-starter:store.py
    
    Key Patterns to Adopt
    
    1. Enum-based constraints for controlled vocabularies
    2. Custom field serializers for consistent API formats
    3. Separate domain and document models for clean architecture
    4. Async batch operations for performance
    5. Comprehensive error handling with specific exception types
    6. Idempotent initialization methods
    7. Type hints everywhere for better IDE support and runtime validation
    
    4. Redis-Specific Best Practices
    
    1. Use prefixes to organize different document types
    2. Create search indices for complex queries
    3. Leverage JSON paths for nested field indexing
    4. Handle Redis-specific errors gracefully
    5. Use connection pooling (handled by redis-py automatically)
"""

DRIVER_INDEX = "driver-idx"
DRIVER_PREFIX = "driver:"
MEETING_INDEX = "meeting-idx"
MEETING_PREFIX = "meeting"


class DriverInfo(NamedTuple):
    number: int
    full_name: str


class Meeting(BaseModel):
    """
    defines a meeting...
    """
    year: int
    session_key: int  # foreign key; via openF1 and the session endpoint;
    meeting_name: str # look at typing library and strings;
    participating_drivers: List[DriverInfo] # list of DriverInfo tuples;
    created_date: Optional[datetime]
    
    @field_serializer("created_date")
    def serialize_created_date(self, dt: datetime) -> str:
        """ datetime.now(timezone.utc) in create method that passes the dt object """
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
		
		
class Driver(BaseModel):
    """
    defines a driver...
    """
    number: int
    full_name: str
    session_key: int  # foreign key
    radio_transcript: List[dict]
    lap_avg_sentiment: float
    team_name: str
    created_date: Optional[datetime]
    
    @field_serializer("created_date")
    def serialize_created_date(self, dt: datetime) -> str:
        """ datetime.now(timezone.utc) in create method that passes the dt object """
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


class MeetingDocument(BaseModel):
    """
    defines a meeting document;
    """
    id: str
    value: Meeting


class DriverDocument(BaseModel):
    """
    defines a driver document;
    """
    id: str
    value: Driver


class Meetings(BaseModel):
    """ a list of meeting documents """
    docs: List[MeetingDocument]


class Drivers(BaseModel):
    """ a list of driver documents """
    docs: List[DriverDocument]


class RaceStore:
    """ stores and retrieves meeting and driver documents """
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
        self.MEETING_INDEX = MEETING_INDEX
        self.MEETING_PREFIX = MEETING_PREFIX
        self.DRIVER_INDEX = DRIVER_INDEX
        self.DRIVER_PREFIX = DRIVER_PREFIX
    
    async def initialize(self) -> None:
        """ sets up redis to store meetings and drivers """
        await self.create_index_if_not_exists()
        return None
    
    async def have_index(self, target_index: str) -> bool:
        """ checks if MEETING_INDEX and DRIVER_INDEX exist in Redis """
        try:
            await self.redis.ft(target_index).info()
            
        except ResponseError as e:
            if "Unknown index name" in str(e) or "no such index" in str(e):
                # logger.debug(f"Indexes) need to see if i can parse requested index for the error
                return False
        
        # logger.debug(f"Indexes exist.")
        return True
    
    async def create_index_if_not_exists(self) -> None:
        """ creates the required indicies """
        meeting_index_exists = self.have_index(self.MEETING_INDEX)
        driver_index_exists = self.have_index(self.DRIVER_INDEX)
        
        if meeting_index_exists and driver_index_exists:
            return None
        
        # logger.debug("creating index {self.index}")
        
        meeting_schema = [
            NumericField("$.year", as_name="year"),
            NumericField("$.session_key", as_name="session_key"),
            TextField("$.meeting_name", as_name="meeting_name")
        ]
        
        driver_schema: List[Field] = [
            NumericField("$.driver_number", as_name="driver_number"),
            NumericField("$.session_key", as_name="session_key")
        ]
        
        try:
            if not meeting_index_exists:
                await self.redis.ft(self.MEETING_INDEX).create_index(
                    meeting_schema,
                    definition=IndexDefinition(prefix=[self.MEETING_PREFIX], index_type=IndexType.JSON)
                )

        except Exception as e:
            # logger.error(f"Error creating meeting index: {e}...")
            raise
        
        # logger.debug("meeting index created...")

        try:
            if not driver_index_exists:
                await self.redis.ft(self.DRIVER_INDEX).create_index(
                    driver_schema,
                    definition=IndexDefinition(prefix=[self.DRIVER_PREFIX], index_type=IndexType.JSON)
                )

        except Exception as e:
            # logger.error(f"Error creating driver index: {e}...")
            raise
        
        # logger.debug("meeting index created...")

        return None
    
    async def drop_index(self) -> None:
        """ drops index ... implement for testing """
        pass
    
    def format_id(self, id: str, target_prefix: str) -> str:
        if re.match(f"^{target_prefix}", id):
            return id
        
        return f"{target_prefix}{id}"
    
    def deserialize_meeting_document(self, document: Document) -> MeetingDocument:
        """ returns meeting document..."""
        return MeetingDocument(
            id=document.id,
            value=Meeting(**from_json(document.json), allow_partial=True)  # type: ignore
        )

    def deserialize_driver_document(self, document: Document) -> DriverDocument:
        """ returns driver document """
        return DriverDocument(
            id=document.id,
            value=Driver(**from_json(document.json), allow_partial=True)  # type: ignore
        )
    
    def deserialize_meetings(self, documents: List[Document]) -> Meetings:
        """ modular can take args with a string model target """
        meetings = Meetings(docs=[])
        
        for d in documents:
            meetings.docs.append(self.deserialize_meeting_document(document=d))
        
        return meetings
    
    def deserialize_drivers(self, documents: List[Document]) -> Drivers:
         """ modular can take args with a string model target """
         drivers = Drivers(docs=[])
         
         for d in documents:
             drivers.docs.append(self.deserialize_driver_document(document=d))
         
         return drivers


    async def search_year(self, year: int) -> Union[Meetings, None]:
        search = []
        
        if year is not None and year > 2000:
            search.append(f"@year:{year}")
        
        try:
            results: Result = await self.redis.ft(self.MEETING_INDEX).search(Query(" ".join(search)))  # type: ignore
            deserialized_results = self.deserialize_meetings(documents=results.docs)
            
            return deserialized_results
        
        except Exception as e:
            # logger.error(f"error getting meeting by year: {e}...")
            return None
    
    async def search_driver(self, driver_number: int, session_key: int) -> Union[Drivers, None]:
        search = []
        
        search.extend([f"@number:({driver_number})", f"@session_key:({session_key})"])
        
        try:
            result: Result = await self.redis.ft(self.DRIVER_INDEX).search(Query(" ".join(search)))  # type: ignore
            deserialized_results = self.deserialize_drivers(documents=result.docs)
            
            return deserialized_results

        except Exception as e:
            # logger.error(f"error getting driver: {e}...")
            return None
    
    async def create_meeting(self, **kwargs) -> MeetingDocument:
        """
        key word arguments that defines a meeting:
        
        year: int
        session_key: int  # foreign key; via openF1 and the session endpoint;
        meeting_name: str # look at typing library and strings;
        participating_drivers: List[DriverInfo] # list of DriverInfo tuples;
        
        """
        
        time_now = datetime.now(timezone.utc)
        
        required = ["year", "session_key", "meeting_name", "participating_drivers"]
        
        input_args = { req_key: kwargs.get(req_key, None) for req_key in required }  # gathered args
        
        if not all(input_args.values()):
            raise Exception(f"Meeting requires all values; inputs given: {input_args}")
            
        meeting = MeetingDocument(id=self.format_id(id=str(uuid4()), target_prefix=self.MEETING_PREFIX),
                                  value=Meeting(
                                      year=kwargs["year"],
                                      session_key=kwargs["session_key"],
                                      meeting_name=kwargs["meeting_name"],
                                      participating_drivers=kwargs["participating_drivers"],
                                      created_date=time_now
                                  )
        )
        
        try:
            success = await self.redis.json().set(meeting.id, "$", meeting.value.model_dump())  # type: ignore
        except Exception as e:
            # logger.error(f"error creating meeting")
            raise

        if not success:
            raise Exception(f"error creating meeting: {meeting}")
        
        return meeting
    
    async def create_driver(self,**kwargs) -> DriverDocument:
        """
        key word arguments that defines a driver:
        
        number: int
        full_name: str
        session_key: int  # foreign key
        radio_transcript: List[dict]
        lap_avg_sentiment: float
        team_name: str
        
        """
        time_now = datetime.now(timezone.utc)
        
        required = ["number", "full_name", "session_key", "radio_transcript", "lap_avg_sentiment", "team_name"]
        
        input_args = { req_key: kwargs.get(req_key, None) for req_key in required}
        
        if not all(input_args.values()):
            raise Exception(f"Driver requires all values; inputs given: {input_args}")
        
        driver = DriverDocument(
                    id=self.format_id(id=str(uuid4()), target_prefix=self.DRIVER_PREFIX),
                    value=Driver(
                        number=kwargs["number"],
                        full_name=kwargs["full_name"],
                        session_key=kwargs["session_key"],
                        radio_transcript=kwargs["radio_transcript"],
                        lap_avg_sentiment=kwargs["lap_avg_sentiment"],
                        team_name=kwargs["team_name"],
                        created_date=time_now
                    )
        )

        try:
            success = await self.redis.json().set(driver.id, "$", driver.value.model_dump())  # type: ignore
        except Exception as e:
            # logger the e
            raise
        
        if not success:
            raise Exception(f"error creating driver: {driver}")
        
        return driver

# from fastapi import Depends ******************************************************** OLD STORE *********************************************************

# import pandas as pd


# class SessionData:
#     """
#     API Data Store class containing all necessary data structures needed across
#         all requests throughout a session.
#     """
#     def __init__(self,
#                  drivers: dict = {"session_key": []},
#                  laps: dict = {"session_key": []},
#                  meetings: dict = {"year": []},
#                  radios: dict = {"session_key": []},
#                  sessions: dict = {"session_key": []},
#                  session_key: int = 0,
#                  meeting_key: int = 0,
#                  year: int = 2023) -> None:

#         self.drivers_df = pd.DataFrame(drivers)
#         self.laps_df = pd.DataFrame(laps)
#         self.meetings_df = pd.DataFrame(meetings)
#         self.radios_df = pd.DataFrame(radios)
#         self.sessions_df = pd.DataFrame(sessions)
#         self.current_session_key = session_key
#         self.current_meeting_key = meeting_key
#         self.desired_year = year

# app_session_data = SessionData()  # Instantiate app data store object


# def get_app_session_data():
#     """
#     Retrieves SessionData data store object for endpoints.
#     """
#     return app_session_data

# # Utility functions using dependency injection.
# def get_session_key(data: SessionData = Depends(get_app_session_data)):
#     return data.current_session_key

# def get_desired_year(data: SessionData = Depends(get_app_session_data)):
#     return data.desired_year

# def get_drivers_df(data: SessionData = Depends(get_app_session_data)):
#     return data.drivers_df

# def get_meetings_df(data: SessionData = Depends(get_app_session_data)):
#     return data.meetings_df

# def get_sessions_df(data: SessionData = Depends(get_app_session_data)):
#     return data.sessions_df
