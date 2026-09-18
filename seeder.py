#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Puebla la tabla de personas con datos iniciales."""

from sqlalchemy.orm import Session
from src.database.database import engine, Base
from src.entities.persona import Persona

def seed_data():
    """Crea las tablas e inserta una persona si la base esta vacia."""
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        if not session.query(Persona).first():
            print("Insertando datos iniciales de Persona...")
            nueva_persona = Persona(
                nombre="Vilmar",
                apellido="Rivas"
            )
            session.add(nueva_persona)
            session.commit()
            print("? Seeder ejecutado con �xito.")
        else:
            print("? Los datos ya existen en la base de datos de Neon.")

if __name__ == "__main__":
    seed_data()
