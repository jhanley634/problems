#! /usr/bin/env python
# Copyright 2024 John Hanley. MIT licensed.
from sqlalchemy import Float, Integer, Text
from sqlalchemy.orm import declarative_base, mapped_column

Base = declarative_base()


class ApnAddress(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "apn_address"

    apn = mapped_column(Text, primary_key=True)
    situs_addr = mapped_column(Text, index=True, nullable=False)


class Owner(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "owner"

    apn = mapped_column(Text, primary_key=True)
    category = mapped_column(Text, nullable=False)
    units = mapped_column(Integer, nullable=False)
    first_owner = mapped_column(Text, index=True, nullable=False)
    bus_name = mapped_column(Text)
    address = mapped_column(Text, index=True, nullable=False)
    city = mapped_column(Text)
    st = mapped_column(Text)
    zip = mapped_column(Text, nullable=False)


class Location(Base):  # type: ignore [misc, valid-type]
    __tablename__ = "location"

    addr_upper = mapped_column(Text, primary_key=True)
    addr = mapped_column(Text, index=True, nullable=False)
    zipcode = mapped_column(Text)
    lat = mapped_column(Float, nullable=False)
    lon = mapped_column(Float, nullable=False)
