import os
import uuid
from sqlalchemy import create_engine, Column, String, DateTime, Integer, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func


Base = declarative_base()

class ServiceConfiguration(Base):
    __tablename__ = 'service_configuration'
    __table_args__ = {'schema': 'wechat'}
    # 如果不需要指定schema或者schema是默认的，可以移除 __table_args__
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_name = Column(String(255), nullable=False)
    appid = Column(String(255), nullable=False, unique=True)
    appsecret = Column(Text, nullable=False)
    parse_message_bot_url = Column(String(2048), nullable=True)  # 设定了长度的字符串
    parse_event_url = Column(String(2048), nullable=True)
    token = Column(String(255), nullable=False)

    # __repr__函数用于提供类的“官方”字符串表示
    def __repr__(self):
        return f"<ServiceConfiguration(id={self.id}, project_name='{self.project_name}', appid='{self.appid}')>"
