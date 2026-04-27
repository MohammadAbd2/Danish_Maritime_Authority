from app.models.schemas import RMRSubmission, Finding

FAST_HEART_WORDS = ["heart is beating too fast", "hart is beating too fast", "heart beating too fast", "fast heart", "racing heart", "palpitations", "hjerte banker hurtigt", "hurtig puls", "hjertebanken"]
RUNNING_WORDS = ["running", "ran", "løb", "løber", "jogging"]


def _finding(severity, section, en, da, rec_en, rec_da):
    return Finding(
        severity=severity,
        section=section,
        message_en=en,
        message_da=da,
        recommendation_en=rec_en,
        recommendation_da=rec_da,
    )


def evaluate_rules(record: RMRSubmission):
    a = record.assessment
    p = record.patient
    findings = []
    text = f"{p.problem_description} {a.performed_actions}".lower()

    if not p.name_title or not p.birthdate_cpr:
        findings.append(_finding("minor", "Patient identity", "Patient name/title or birthdate/CPR is missing.", "Patientens navn/titel eller fødselsdato/CPR mangler.", "Complete identity fields before sending the record.", "Udfyld identitetsfelterne før journalen sendes."))
    if not p.ship_name or not p.coordinates:
        findings.append(_finding("major", "Voyage details", "Ship name or coordinates are missing.", "Skibsnavn eller koordinater mangler.", "Radio Medical needs location and vessel details to assess urgency and evacuation options.", "Radio Medical har brug for position og skibsoplysninger for at vurdere hast og evakuering."))
    if not p.problem_description.strip():
        findings.append(_finding("major", "Problem description", "Problem description is empty.", "Problembeskrivelsen er tom.", "Describe what happened, where, when, and current symptoms.", "Beskriv hvad der skete, hvor, hvornår og de aktuelle symptomer."))

    if a.airway_clear is False and not (a.jaw_lift or a.suction_applied or a.guedel_airway or a.cpr_initiated_at):
        findings.append(_finding("critical", "A: Airway", "Airway is marked not clear, but no airway intervention or CPR time is documented.", "Luftvejen er markeret som ikke fri, men der er ikke dokumenteret luftvejsintervention eller CPR-tid.", "Document jaw lift, suction, Guedel airway and CPR start time if breathing is absent or gasping.", "Dokumentér jaw lift, sug, Guedel-tube og tidspunkt for CPR hvis vejrtrækning mangler eller er gispende."))
    if a.oxygen_l_min and a.oxygen_l_min > 10 and "hudson" not in a.oxygen_method.lower():
        findings.append(_finding("major", "A: Airway/Oxygen", "Oxygen flow is above 10 l/min but Hudson mask is not selected.", "Iltflow er over 10 l/min, men Hudson-maske er ikke valgt.", "Use Hudson mask for >10 l/min or document why another delivery method was used.", "Brug Hudson-maske ved >10 l/min eller dokumentér hvorfor en anden metode blev brugt."))
    if a.oxygen_l_min and a.oxygen_l_min <= 5 and "nasal" not in a.oxygen_method.lower() and "næse" not in a.oxygen_method.lower():
        findings.append(_finding("minor", "A: Oxygen", "Low-flow oxygen is documented without nasal cannula selection.", "Lavt iltflow er dokumenteret uden valg af næsekateter.", "For ≤5 l/min, nasal cannula is normally expected unless another method is justified.", "Ved ≤5 l/min forventes normalt næsekateter, medmindre andet er begrundet."))

    if a.breathing_rate is not None and not 12 <= a.breathing_rate <= 16:
        findings.append(_finding("major", "B: Breathing", f"Breathing rate is {a.breathing_rate}/min, outside the normal 12-16 range.", f"Respirationsfrekvensen er {a.breathing_rate}/min, uden for normalområdet 12-16.", "Describe breathing depth/effort, oxygen saturation, oxygen delivery and reassessment.", "Beskriv dybde/arbejde, iltmætning, iltbehandling og plan for revurdering."))
    if a.oxygen_saturation is not None and a.oxygen_saturation < 95:
        findings.append(_finding("major", "B: Breathing", f"Oxygen saturation is {a.oxygen_saturation}%, below the normal 95-100% range.", f"Iltmætning er {a.oxygen_saturation}%, under normalområdet 95-100%.", "Document oxygen intervention and repeat SpO2 after treatment.", "Dokumentér iltbehandling og gentag SpO2 efter indsats."))

    if a.capillary_response_seconds is not None and a.capillary_response_seconds > 2 and a.venous_cannula_inserted is not True:
        findings.append(_finding("major", "C: Circulation", "Capillary response is more than 2 seconds without documented venous cannula insertion.", "Kapillærrespons er over 2 sekunder uden dokumenteret venekanyle.", "Record whether a venous cannula was inserted or why it was not possible.", "Angiv om venekanyle blev anlagt eller hvorfor det ikke var muligt."))
    if a.pulse is not None and not 60 <= a.pulse <= 80:
        findings.append(_finding("major", "C: Circulation", f"Pulse is {a.pulse}/min, outside the normal 60-80 range.", f"Pulsen er {a.pulse}/min, uden for normalområdet 60-80.", "Connect pulse findings to symptoms, skin colour, capillary response and blood pressure trend.", "Kobl pulsfundet til symptomer, hudfarve, kapillærrespons og blodtrykstrend."))
    if any(w in text for w in FAST_HEART_WORDS) and a.pulse is None:
        findings.append(_finding("major", "C: Circulation", "The description suggests a fast heartbeat, but no pulse value is documented.", "Beskrivelsen tyder på hurtig hjerterytme, men pulsværdi er ikke dokumenteret.", "Measure and record pulse per minute, rhythm regularity, blood pressure, SpO2, and repeat after rest.", "Mål og dokumentér puls/minut, regelmæssighed, blodtryk, SpO2 og gentag efter hvile."))
    if any(w in text for w in FAST_HEART_WORDS) and any(w in text for w in RUNNING_WORDS):
        findings.append(_finding("minor", "Clinical context", "Fast heartbeat may be related to recent running, but this needs reassessment after rest.", "Hurtig puls kan være relateret til nylig løb, men skal revurderes efter hvile.", "Let the patient rest, repeat pulse/BP/SpO2, and document whether symptoms persist or include chest pain, dizziness or shortness of breath.", "Lad patienten hvile, gentag puls/BT/SpO2, og dokumentér om symptomer fortsætter eller om der er brystsmerter, svimmelhed eller åndenød."))
    if a.systolic_bp is not None and a.diastolic_bp is not None and not (120 <= a.systolic_bp <= 140 and 60 <= a.diastolic_bp <= 90):
        findings.append(_finding("minor", "C: Circulation", f"Blood pressure is {a.systolic_bp}/{a.diastolic_bp}, outside the normal 120-140/60-90 range.", f"Blodtrykket er {a.systolic_bp}/{a.diastolic_bp}, uden for normalområdet 120-140/60-90.", "Recheck blood pressure and document the trend in the observation chart.", "Mål blodtryk igen og dokumentér udviklingen i observationsskemaet."))

    if a.consciousness_level in {3, 4} and not a.pupil_reaction_description.strip() and a.pupil_reaction_normal is not True:
        findings.append(_finding("major", "D: Disability", "Reduced consciousness is recorded without a clear pupil reaction description.", "Nedsat bevidsthed er registreret uden klar beskrivelse af pupilreaktion.", "Describe pupil size, equality and light reaction.", "Beskriv pupilstørrelse, ensartethed og lysreaktion."))
    if a.convulsions is True:
        findings.append(_finding("major", "D: Disability", "Convulsions are marked yes.", "Kramper er markeret ja.", "Document duration, recovery, injuries, blood sugar if possible, and contact Radio Medical urgently.", "Dokumentér varighed, opvågning, skader, blodsukker hvis muligt, og kontakt Radio Medical akut."))

    if a.expose_exam_performed is False:
        findings.append(_finding("minor", "E: Expose", "Top-to-toe examination is marked as not performed.", "Top-til-tå-undersøgelse er markeret som ikke udført.", "Document why it could not be performed and what may still need checking.", "Dokumentér hvorfor den ikke kunne udføres, og hvad der stadig skal kontrolleres."))
    if a.temperature_measured is False:
        findings.append(_finding("minor", "E: Expose", "Temperature measurement is marked as not performed.", "Temperaturmåling er markeret som ikke udført.", "Measure temperature when possible, especially with infection, hypothermia or overheating concerns.", "Mål temperatur når muligt, især ved mistanke om infektion, hypotermi eller overophedning."))

    if not record.observations:
        findings.append(_finding("minor", "Observation chart", "No observation chart rows are recorded.", "Der er ingen rækker i observationsskemaet.", "Add at least one observation row and repeat values after interventions.", "Tilføj mindst én observationsrække og gentag værdier efter interventioner."))
    return findings
