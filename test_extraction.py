#!/usr/bin/env python3
"""
Test script to verify document extraction and auto-fill functionality
"""

from backend.app.services.document_parser import extract_structured_data

# Test 1: English text extraction
english_text = """
Patient Name: John Smith
Birthdate: 15/04/1985
Gender: Male
Nationality: British
Ship: MV Ocean Explorer
Coordinates: 55.329, 11.138

Problem description: The patient reports shortness of breath after exertion.

Vital Signs:
Breathing rate: 24 breaths/min
Oxygen saturation SpO2: 92%
Pulse: 95 beats/min
Blood pressure: 135/85
Temperature: 37.2°C
Blood sugar: 6.5 mmol/l

Clinical findings:
Airway: Clear and patent
Consciousness: Alert and oriented
Pupil reaction: Normal and reactive
"""

print("Testing English text extraction...")
extracted = extract_structured_data(english_text)
print(f"Extracted data: {extracted}")
print()

# Test 2: Danish text extraction
danish_text = """
Patientnavn: Mohammad Abd Al Rahem
Fødselsdato: 15/04/1998
Køn: Mand
Nationalitet: Syrisk
Skib: Titanic Training Vessel
Koordinater: 55.329, 11.138

Problembeskrivelse: Patienten siger, at hjertet banker meget hurtigt efter løb på dækket. Han føler sig svimmel og lidt forpustet.

Vitale værdier:
Respirationsfrekvens: 22 vejrtrækninger/min
Iltmætning SpO2: 96%
Puls: 126 slag/min
Blodtryk: 145/92
Temperatur: 36.9°C
Blodsukker: 5.4 mmol/l

Kliniske fund:
Luftvej: Klar og fri
Bevidsthed: Vågen og orienteret
Pupilreaktion: Normal og reaktiv
"""

print("Testing Danish text extraction...")
extracted_da = extract_structured_data(danish_text)
print(f"Extracted data: {extracted_da}")
print()

# Test 3: Verify key fields are extracted
print("Verification:")
print(f"✓ English - Name extracted: {'name_title' in extracted}")
print(f"✓ English - Breathing rate extracted: {'breathing_rate' in extracted}")
print(f"✓ English - Blood pressure extracted: {'systolic_bp' in extracted and 'diastolic_bp' in extracted}")
print(f"✓ Danish - Name extracted: {'name_title' in extracted_da}")
print(f"✓ Danish - Breathing rate extracted: {'breathing_rate' in extracted_da}")
print(f"✓ Danish - Blood sugar extracted: {'blood_sugar' in extracted_da}")
