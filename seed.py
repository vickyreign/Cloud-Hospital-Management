from datetime import date, datetime, timedelta
from app import create_app
from models import db
from models.hospital_models import User, Department, Doctor, Patient, Appointment, MedicalRecord, Bill, Payment
from services.appointment_service import TIME_SLOTS


def seed_all_data():
    """Seed comprehensive, realistic demo dataset for MediCloud HMS."""
    # Clear existing tables
    db.drop_all()
    db.create_all()

    print("[*] Creating Departments...")
    departments_data = [
        {"code": "CARD", "name": "Cardiology", "description": "Heart care, diagnostic ECG, echocardiogram and cardiovascular management", "floor_location": "2nd Floor, Wing A"},
        {"code": "NEUR", "name": "Neurology", "description": "Brain, nerve, spine disorders and electroencephalography", "floor_location": "3rd Floor, Wing B"},
        {"code": "PED", "name": "Pediatrics", "description": "Infant, child and adolescent health and immunization", "floor_location": "1st Floor, Wing C"},
        {"code": "ORTH", "name": "Orthopedics", "description": "Bone, joint, muscular rehabilitation and sports injuries", "floor_location": "Ground Floor, Wing D"},
        {"code": "GEN", "name": "General Medicine", "description": "Primary healthcare, preventive medicine and comprehensive consultations", "floor_location": "Ground Floor, Wing A"}
    ]
    
    depts = {}
    for d in departments_data:
        dept = Department(code=d["code"], name=d["name"], description=d["description"], floor_location=d["floor_location"])
        db.session.add(dept)
        db.session.flush()
        depts[d["code"]] = dept

    print("[*] Creating Doctors...")
    doctors_data = [
        {"code": "DOC-001", "name": "Dr. Sarah Smith", "email": "dr.smith@medicloud.health", "phone": "+1-555-0101", "spec": "Interventional Cardiology", "dept": "CARD", "fee": 650.0, "status": "Available", "qual": "MD, FACC"},
        {"code": "DOC-002", "name": "Dr. David Chen", "email": "dr.chen@medicloud.health", "phone": "+1-555-0102", "spec": "Clinical Neurology", "dept": "NEUR", "fee": 700.0, "status": "Available", "qual": "MD, FAAN"},
        {"code": "DOC-003", "name": "Dr. Emily Taylor", "email": "dr.taylor@medicloud.health", "phone": "+1-555-0103", "spec": "Pediatric Medicine", "dept": "PED", "fee": 500.0, "status": "Available", "qual": "MBBS, MD (Ped)"},
        {"code": "DOC-004", "name": "Dr. Marcus Johnson", "email": "dr.johnson@medicloud.health", "phone": "+1-555-0104", "spec": "Orthopedic Surgery", "dept": "ORTH", "fee": 750.0, "status": "Busy", "qual": "MS (Ortho), FRCS"},
        {"code": "DOC-005", "name": "Dr. Priya Patel", "email": "dr.patel@medicloud.health", "phone": "+1-555-0105", "spec": "Internal Medicine", "dept": "GEN", "fee": 450.0, "status": "Available", "qual": "MD (Internal Med)"},
        {"code": "DOC-006", "name": "Dr. Robert Wilson", "email": "dr.wilson@medicloud.health", "phone": "+1-555-0106", "spec": "Cardiology & Rhythm Disorders", "dept": "CARD", "fee": 600.0, "status": "On Leave", "qual": "MD, FHRS"}
    ]

    docs = []
    for doc in doctors_data:
        d = Doctor(
            doctor_code=doc["code"],
            name=doc["name"],
            email=doc["email"],
            phone=doc["phone"],
            specialization=doc["spec"],
            department_id=depts[doc["dept"]].id,
            consultation_fee=doc["fee"],
            availability_status=doc["status"],
            qualification=doc["qual"],
            bio=f"Senior consultant with over 12 years of specialized clinical experience in {doc['spec']}."
        )
        db.session.add(d)
        db.session.flush()
        docs.append(d)

    print("[*] Creating Users & RBAC Accounts...")
    # Admin User
    admin = User(username="admin", email="admin@medicloud.health", role="admin")
    admin.set_password("Admin@123")
    db.session.add(admin)

    # Receptionist User
    receptionist = User(username="reception", email="reception@medicloud.health", role="receptionist")
    receptionist.set_password("Reception@123")
    db.session.add(receptionist)

    # Doctor Accounts
    doc_user_1 = User(username="dr.smith", email="dr.smith@medicloud.health", role="doctor", doctor_id=docs[0].id)
    doc_user_1.set_password("Doctor@123")
    db.session.add(doc_user_1)

    doc_user_2 = User(username="dr.chen", email="dr.chen@medicloud.health", role="doctor", doctor_id=docs[1].id)
    doc_user_2.set_password("Doctor@123")
    db.session.add(doc_user_2)

    print("[*] Creating Patients (24 synthetic profiles)...")
    patients_data = [
        {"name": "James Henderson", "dob": "1982-04-12", "gender": "Male", "blood": "O+", "phone": "+1-555-0201", "email": "james.h@example.com", "addr": "742 Evergreen Terrace, Springfield", "emg": "+1-555-0301", "rel": "Spouse", "hist": "Mild hypertension, penicillin allergy"},
        {"name": "Eleanor Vance", "dob": "1990-11-23", "gender": "Female", "blood": "A+", "phone": "+1-555-0202", "email": "eleanor.v@example.com", "addr": "128 Orchard Way, Brookline", "emg": "+1-555-0302", "rel": "Brother", "hist": "No known allergies"},
        {"name": "Liam Martinez", "dob": "2015-06-08", "gender": "Male", "blood": "B+", "phone": "+1-555-0203", "email": "martinez.family@example.com", "addr": "45 Maple Street, Cambridge", "emg": "+1-555-0303", "rel": "Mother", "hist": "Childhood asthma, managed with inhaler"},
        {"name": "Sophia Reynolds", "dob": "1975-09-17", "gender": "Female", "blood": "AB+", "phone": "+1-555-0204", "email": "sophia.r@example.com", "addr": "89 Beacon Hill Blvd, Boston", "emg": "+1-555-0304", "rel": "Daughter", "hist": "Type 2 Diabetes Mellitus"},
        {"name": "Lucas Kim", "dob": "1998-02-14", "gender": "Male", "blood": "O-", "phone": "+1-555-0205", "email": "lucas.k@example.com", "addr": "310 Commonwealth Ave, Boston", "emg": "+1-555-0305", "rel": "Father", "hist": "ACL repair in 2021"},
        {"name": "Olivia Bennett", "dob": "1988-07-30", "gender": "Female", "blood": "A-", "phone": "+1-555-0206", "email": "olivia.b@example.com", "addr": "19 Highland Ave, Somerville", "emg": "+1-555-0306", "rel": "Spouse", "hist": "Migraine headaches"},
        {"name": "Ethan Wright", "dob": "1964-03-05", "gender": "Male", "blood": "B-", "phone": "+1-555-0207", "email": "ethan.w@example.com", "addr": "502 River Street, Quincy", "emg": "+1-555-0307", "rel": "Son", "hist": "Coronary artery disease, stent in 2018"},
        {"name": "Ava Thompson", "dob": "2001-12-19", "gender": "Female", "blood": "O+", "phone": "+1-555-0208", "email": "ava.t@example.com", "addr": "67 Harvard Ave, Allston", "emg": "+1-555-0308", "rel": "Sister", "hist": "Seasonal allergic rhinitis"},
        {"name": "Mason Clark", "dob": "1994-08-25", "gender": "Male", "blood": "A+", "phone": "+1-555-0209", "email": "mason.c@example.com", "addr": "14 Central Square, Cambridge", "emg": "+1-555-0309", "rel": "Partner", "hist": "Non-smoker, healthy"},
        {"name": "Isabella Flores", "dob": "1985-05-14", "gender": "Female", "blood": "O+", "phone": "+1-555-0210", "email": "isabella.f@example.com", "addr": "92 Washington Street, Salem", "emg": "+1-555-0310", "rel": "Mother", "hist": "Hypothyroidism (Levothyroxine 50mcg)"},
        {"name": "Noah Scott", "dob": "2018-01-20", "gender": "Male", "blood": "B+", "phone": "+1-555-0211", "email": "scott.family@example.com", "addr": "23 Elm Court, Newton", "emg": "+1-555-0311", "rel": "Father", "hist": "Standard pediatric immunization up to date"},
        {"name": "Mia Garcia", "dob": "1992-10-03", "gender": "Female", "blood": "AB-", "phone": "+1-555-0212", "email": "mia.g@example.com", "addr": "78 Pine Street, Medford", "emg": "+1-555-0312", "rel": "Spouse", "hist": "No known allergies"},
        {"name": "Alexander Murphy", "dob": "1970-04-18", "gender": "Male", "blood": "O+", "phone": "+1-555-0213", "email": "alex.m@example.com", "addr": "156 Walnut Rd, Malden", "emg": "+1-555-0313", "rel": "Wife", "hist": "Hyperlipidemia"},
        {"name": "Charlotte Cooper", "dob": "1995-03-29", "gender": "Female", "blood": "A+", "phone": "+1-555-0214", "email": "charlotte.c@example.com", "addr": "400 Tremont Street, Boston", "emg": "+1-555-0314", "rel": "Friend", "hist": "Lactose intolerant"},
        {"name": "Daniel Rivera", "dob": "1983-09-11", "gender": "Male", "blood": "B+", "phone": "+1-555-0215", "email": "daniel.r@example.com", "addr": "88 Pleasant Blvd, Waltham", "emg": "+1-555-0315", "rel": "Brother", "hist": "Occasional back pain"},
        {"name": "Harper King", "dob": "2003-07-22", "gender": "Female", "blood": "O-", "phone": "+1-555-0216", "email": "harper.k@example.com", "addr": "34 South St, Jamaica Plain", "emg": "+1-555-0316", "rel": "Mother", "hist": "Sulfa antibiotic allergy"},
        {"name": "Benjamin Adams", "dob": "1958-12-04", "gender": "Male", "blood": "A-", "phone": "+1-555-0217", "email": "ben.adams@example.com", "addr": "210 Centre Street, Roxbury", "emg": "+1-555-0317", "rel": "Daughter", "hist": "Osteoarthritis in left knee"},
        {"name": "Amelia Baker", "dob": "1989-06-15", "gender": "Female", "blood": "O+", "phone": "+1-555-0218", "email": "amelia.b@example.com", "addr": "60 Prospect Street, Cambridge", "emg": "+1-555-0318", "rel": "Spouse", "hist": "Iron deficiency anemia"},
        {"name": "Henry Mitchell", "dob": "1978-01-31", "gender": "Male", "blood": "B-", "phone": "+1-555-0219", "email": "henry.m@example.com", "addr": "115 Broadway, Arlington", "emg": "+1-555-0319", "rel": "Wife", "hist": "Gastroesophageal reflux (GERD)"},
        {"name": "Evelyn Nelson", "dob": "1996-08-09", "gender": "Female", "blood": "A+", "phone": "+1-555-0220", "email": "evelyn.n@example.com", "addr": "51 Winter Street, Boston", "emg": "+1-555-0320", "rel": "Father", "hist": "None"},
        {"name": "Jack Campbell", "dob": "2010-05-16", "gender": "Male", "blood": "AB+", "phone": "+1-555-0221", "email": "campbell.j@example.com", "addr": "18 School Street, Belmont", "emg": "+1-555-0321", "rel": "Mother", "hist": "Peanut allergy"},
        {"name": "Grace Hall", "dob": "1980-11-02", "gender": "Female", "blood": "O+", "phone": "+1-555-0222", "email": "grace.h@example.com", "addr": "72 Park Avenue, Watertown", "emg": "+1-555-0322", "rel": "Husband", "hist": "Hypothyroidism"},
        {"name": "Samuel Perez", "dob": "1968-07-19", "gender": "Male", "blood": "A-", "phone": "+1-555-0223", "email": "samuel.p@example.com", "addr": "430 Main Street, Everett", "emg": "+1-555-0323", "rel": "Son", "hist": "Hypertension"},
        {"name": "Victoria Green", "dob": "1993-04-27", "gender": "Female", "blood": "B+", "phone": "+1-555-0224", "email": "victoria.g@example.com", "addr": "15 Forest Hills, Boston", "emg": "+1-555-0324", "rel": "Sister", "hist": "No known drug allergies"}
    ]

    patients = []
    current_year = datetime.utcnow().year
    for idx, p in enumerate(patients_data, start=1):
        patient = Patient(
            patient_id=f"PAT-{current_year}-{idx:04d}",
            full_name=p["name"],
            dob=datetime.strptime(p["dob"], '%Y-%m-%d').date(),
            gender=p["gender"],
            blood_group=p["blood"],
            contact_number=p["phone"],
            email=p["email"],
            address=p["addr"],
            emergency_contact=p["emg"],
            emergency_relation=p["rel"],
            medical_history_summary=p["hist"],
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=25 - idx)
        )
        db.session.add(patient)
        db.session.flush()
        patients.append(patient)

    print("[*] Creating Appointments (25 appointments across past, today, future)...")
    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    tomorrow = today + timedelta(days=1)
    two_days_later = today + timedelta(days=2)
    three_days_later = today + timedelta(days=3)

    appointment_configs = [
        # Today's appointments
        {"p": 0, "d": 0, "date": today, "slot": "09:00 - 09:30", "status": "Confirmed", "reason": "Follow-up ECG consultation"},
        {"p": 1, "d": 1, "date": today, "slot": "10:00 - 10:30", "status": "Scheduled", "reason": "Recurrent migraine headaches"},
        {"p": 2, "d": 2, "date": today, "slot": "11:00 - 11:30", "status": "Scheduled", "reason": "Annual pediatric checkup and growth tracking"},
        {"p": 3, "d": 4, "date": today, "slot": "14:00 - 14:30", "status": "Confirmed", "reason": "Routine diabetes blood sugar review"},
        {"p": 4, "d": 3, "date": today, "slot": "15:30 - 16:00", "status": "Scheduled", "reason": "Knee joint stiffness and assessment"},

        # Completed past appointments (2 days ago and yesterday)
        {"p": 5, "d": 0, "date": two_days_ago, "slot": "09:00 - 09:30", "status": "Completed", "reason": "Chest tightness and palpitations"},
        {"p": 6, "d": 1, "date": two_days_ago, "slot": "10:30 - 11:00", "status": "Completed", "reason": "Dizziness and visual aura evaluation"},
        {"p": 7, "d": 2, "date": two_days_ago, "slot": "14:00 - 14:30", "status": "Completed", "reason": "Seasonal cold and fever in child"},
        {"p": 8, "d": 3, "date": two_days_ago, "slot": "15:00 - 15:30", "status": "Completed", "reason": "Acute ankle sprain during sport"},
        {"p": 9, "d": 4, "date": yesterday, "slot": "09:30 - 10:00", "status": "Completed", "reason": "General wellness and lipid panel review"},
        {"p": 10, "d": 0, "date": yesterday, "slot": "11:00 - 11:30", "status": "Completed", "reason": "Hypertension medication dosage check"},
        {"p": 11, "d": 1, "date": yesterday, "slot": "14:30 - 15:00", "status": "Completed", "reason": "Post-concussion syndrome assessment"},
        {"p": 12, "d": 3, "date": yesterday, "slot": "16:00 - 16:30", "status": "Completed", "reason": "Lower lumbar spine discomfort"},

        # Cancelled past appointments
        {"p": 13, "d": 4, "date": two_days_ago, "slot": "11:30 - 12:00", "status": "Cancelled", "reason": "Patient rescheduled travel conflict"},
        {"p": 14, "d": 1, "date": yesterday, "slot": "16:30 - 17:00", "status": "Cancelled", "reason": "Work conflict reported by patient"},

        # Upcoming appointments
        {"p": 15, "d": 0, "date": tomorrow, "slot": "09:00 - 09:30", "status": "Scheduled", "reason": "Stress echocardiogram preparation"},
        {"p": 16, "d": 1, "date": tomorrow, "slot": "10:00 - 10:30", "status": "Confirmed", "reason": "Neuropathy tingling in fingers"},
        {"p": 17, "d": 2, "date": tomorrow, "slot": "11:30 - 12:00", "status": "Scheduled", "reason": "Pre-school vaccination booster"},
        {"p": 18, "d": 3, "date": tomorrow, "slot": "14:00 - 14:30", "status": "Confirmed", "reason": "Rotator cuff shoulder mobility follow-up"},
        {"p": 19, "d": 4, "date": two_days_later, "slot": "09:30 - 10:00", "status": "Scheduled", "reason": "Comprehensive physical checkup"},
        {"p": 20, "d": 0, "date": two_days_later, "slot": "11:00 - 11:30", "status": "Scheduled", "reason": "Holter monitor results review"},
        {"p": 21, "d": 1, "date": two_days_later, "slot": "15:00 - 15:30", "status": "Confirmed", "reason": "Sleep apnea and morning fatigue evaluation"},
        {"p": 22, "d": 3, "date": three_days_later, "slot": "10:30 - 11:00", "status": "Scheduled", "reason": "Post-operative meniscus repair review"},
        {"p": 23, "d": 4, "date": three_days_later, "slot": "14:30 - 15:00", "status": "Scheduled", "reason": "Thyroid hormone panel follow-up"},
        {"p": 2, "d": 4, "date": three_days_later, "slot": "16:00 - 16:30", "status": "Scheduled", "reason": "General dietary consultation"}
    ]

    appointments = []
    for idx, ac in enumerate(appointment_configs, start=1):
        apt = Appointment(
            appointment_code=f"APT-{current_year}-{idx:04d}",
            patient_id=patients[ac["p"]].id,
            doctor_id=docs[ac["d"]].id,
            department_id=docs[ac["d"]].department_id,
            appointment_date=ac["date"],
            time_slot=ac["slot"],
            status=ac["status"],
            reason=ac["reason"],
            notes="Booking verified via MediCloud web portal."
        )
        db.session.add(apt)
        db.session.flush()
        appointments.append(apt)

    print("[*] Creating Clinical Medical Records for Completed Appointments...")
    clinical_notes = [
        {
            "apt_idx": 5, "p_idx": 5, "d_idx": 0,
            "symp": "Patient presented with intermittent chest tightness during exertion over 2 weeks, accompanied by palpitations.",
            "diag": "Sinus Tachycardia secondary to stress and borderline essential hypertension (Grade 1).",
            "treat": "Rest ECG normal with elevated heart rate. Advised reduction in caffeine intake, structured stress management, and daily home blood pressure logging.",
            "presc": "Metoprolol Succinate 25mg PO once daily in morning. Aspirin 81mg PO once daily.",
            "vitals": "BP: 138/88 mmHg, Pulse: 88 bpm, SpO2: 99%, Temp: 98.4 F, Weight: 74 kg",
            "follow": today + timedelta(days=14)
        },
        {
            "apt_idx": 6, "p_idx": 6, "d_idx": 1,
            "symp": "Unilateral throbbing headache on left side with photophobia and nausea lasting 18 hours.",
            "diag": "Migraine with typical aura (ICD-10 G43.109).",
            "treat": "Dark room rest recommended. Identified irregular sleep and bright screen exposure as triggers. Prescribed triptan rescue medication.",
            "presc": "Sumatriptan 50mg PO at onset of aura. Ondansetron 4mg PO PRN nausea.",
            "vitals": "BP: 122/78 mmHg, Pulse: 72 bpm, SpO2: 100%, Temp: 98.6 F, Weight: 62 kg",
            "follow": today + timedelta(days=30)
        },
        {
            "apt_idx": 7, "p_idx": 7, "d_idx": 2,
            "symp": "Rhinorrhea, mild dry cough, low grade fever (99.8 F) for 3 days. Eating and drinking adequately.",
            "diag": "Viral Upper Respiratory Tract Infection (Common Cold).",
            "treat": "Supportive care, oral hydration, warm saline gargles, honey-lemon mixture for cough. No antibiotic indicated.",
            "presc": "Acetaminophen pediatric syrup 160mg/5mL, 7.5mL PO Q6H PRN fever/discomfort. Saline nasal drops.",
            "vitals": "Temp: 99.8 F, Pulse: 94 bpm, SpO2: 98%, Weight: 26 kg",
            "follow": None
        },
        {
            "apt_idx": 8, "p_idx": 8, "d_idx": 3,
            "symp": "Inversion injury of the right lateral ankle during recreational soccer. Swelling and lateral malleolus tenderness.",
            "diag": "Right Ankle Inversion Sprain (Grade II ATFL stretch).",
            "treat": "Negative for bony fracture on clinical Ottawa ankle rules. R.I.C.E protocol (Rest, Ice, Compression, Elevation) instituted. Prescribed supportive ankle brace.",
            "presc": "Ibuprofen 400mg PO TID with meals for 5 days. Topical diclofenac gel applied TID.",
            "vitals": "BP: 124/80 mmHg, Pulse: 76 bpm, Temp: 98.4 F, Weight: 81 kg",
            "follow": today + timedelta(days=10)
        },
        {
            "apt_idx": 9, "p_idx": 9, "d_idx": 4,
            "symp": "Routine annual medical assessment. Patient feels active but reports daytime fatigue.",
            "diag": "Subclinical Vitamin D Deficiency and Borderline Hypercholesterolemia.",
            "treat": "Prescribed oral cholecalciferol supplementation and Mediterranean diet with 30 min daily brisk walking.",
            "presc": "Cholecalciferol (Vitamin D3) 50,000 IU orally once weekly for 8 weeks.",
            "vitals": "BP: 118/76 mmHg, Pulse: 68 bpm, SpO2: 99%, Temp: 98.6 F, Weight: 69 kg",
            "follow": today + timedelta(days=60)
        },
        {
            "apt_idx": 10, "p_idx": 10, "d_idx": 0,
            "symp": "Follow up on previously elevated clinic blood pressure measurements. Patient reports no shortness of breath or dizziness.",
            "diag": "Primary Essential Hypertension (well tolerated).",
            "treat": "Dietary Approaches to Stop Hypertension (DASH diet) reviewed. Low sodium diet emphasized.",
            "presc": "Amlodipine Besylate 5mg PO once daily.",
            "vitals": "BP: 134/84 mmHg, Pulse: 74 bpm, SpO2: 98%, Temp: 98.5 F, Weight: 85 kg",
            "follow": today + timedelta(days=45)
        }
    ]

    for idx, cn in enumerate(clinical_notes, start=1):
        rec = MedicalRecord(
            record_code=f"REC-{current_year}-{idx:04d}",
            patient_id=patients[cn["p_idx"]].id,
            doctor_id=docs[cn["d_idx"]].id,
            appointment_id=appointments[cn["apt_idx"]].id,
            visit_date=appointments[cn["apt_idx"]].appointment_date,
            symptoms=cn["symp"],
            diagnosis=cn["diag"],
            treatment_notes=cn["treat"],
            prescription=cn["presc"],
            vitals=cn["vitals"],
            follow_up_date=cn["follow"]
        )
        db.session.add(rec)

    print("[*] Creating Invoices and Billing Records...")
    bills_data = [
        {"p_idx": 5, "apt_idx": 5, "consult": 650.0, "serv": 180.0, "med": 45.0, "tax": 5.0, "disc": 0.0, "paid": 918.75, "status": "Paid", "method": "Credit Card"},
        {"p_idx": 6, "apt_idx": 6, "consult": 700.0, "serv": 120.0, "med": 65.0, "tax": 5.0, "disc": 50.0, "paid": 876.75, "status": "Paid", "method": "Insurance"},
        {"p_idx": 7, "apt_idx": 7, "consult": 500.0, "serv": 50.0, "med": 35.0, "tax": 5.0, "disc": 0.0, "paid": 614.25, "status": "Paid", "method": "Cash"},
        {"p_idx": 8, "apt_idx": 8, "consult": 750.0, "serv": 250.0, "med": 85.0, "tax": 5.0, "disc": 100.0, "paid": 500.0, "status": "Partially Paid", "method": "UPI"},
        {"p_idx": 9, "apt_idx": 9, "consult": 450.0, "serv": 150.0, "med": 40.0, "tax": 5.0, "disc": 0.0, "paid": 300.0, "status": "Partially Paid", "method": "Card"},
        {"p_idx": 10, "apt_idx": 10, "consult": 650.0, "serv": 75.0, "med": 30.0, "tax": 5.0, "disc": 0.0, "paid": 792.75, "status": "Paid", "method": "Bank Transfer"},
        {"p_idx": 0, "apt_idx": 0, "consult": 650.0, "serv": 90.0, "med": 0.0, "tax": 5.0, "disc": 0.0, "paid": 0.0, "status": "Unpaid", "method": None},
        {"p_idx": 1, "apt_idx": 1, "consult": 700.0, "serv": 0.0, "med": 0.0, "tax": 5.0, "disc": 0.0, "paid": 0.0, "status": "Unpaid", "method": None},
        {"p_idx": 2, "apt_idx": 2, "consult": 500.0, "serv": 0.0, "med": 0.0, "tax": 5.0, "disc": 0.0, "paid": 0.0, "status": "Unpaid", "method": None},
        {"p_idx": 3, "apt_idx": 3, "consult": 450.0, "serv": 80.0, "med": 25.0, "tax": 5.0, "disc": 25.0, "paid": 200.0, "status": "Partially Paid", "method": "Cash"}
    ]

    for idx, b_data in enumerate(bills_data, start=1):
        consult = b_data["consult"]
        serv = b_data["serv"]
        med = b_data["med"]
        tax = b_data["tax"]
        disc = b_data["disc"]

        subtotal = consult + serv + med
        taxable = max(0.0, subtotal - disc)
        tax_amt = (tax / 100.0) * taxable
        total = round(taxable + tax_amt, 2)

        bill = Bill(
            bill_code=f"INV-{current_year}-{idx:04d}",
            patient_id=patients[b_data["p_idx"]].id,
            appointment_id=appointments[b_data["apt_idx"]].id if b_data["apt_idx"] is not None else None,
            consultation_fee=consult,
            service_charges=serv,
            medicine_charges=med,
            tax_rate=tax,
            discount=disc,
            total_amount=total,
            paid_amount=b_data["paid"],
            status=b_data["status"],
            due_date=today + timedelta(days=15),
            notes="Standard outpatient medical invoice."
        )
        db.session.add(bill)
        db.session.flush()

        if b_data["paid"] > 0 and b_data["method"]:
            pmt = Payment(
                bill_id=bill.id,
                amount=b_data["paid"],
                payment_method=b_data["method"],
                transaction_ref=f"TXN-{current_year}-{idx:04d}",
                notes="Initial settlement recorded at billing desk."
            )
            db.session.add(pmt)

    db.session.commit()
    print("[OK] MediCloud database successfully seeded!")
    print(f"    - Departments: {len(departments_data)}")
    print(f"    - Doctors: {len(doctors_data)}")
    print(f"    - Patients: {len(patients_data)}")
    print(f"    - Appointments: {len(appointment_configs)}")
    print(f"    - Medical Records: {len(clinical_notes)}")
    print(f"    - Bills/Invoices: {len(bills_data)}")
    print("    - Users created:")
    print("      * admin / Admin@123 (Administrator)")
    print("      * reception / Reception@123 (Receptionist)")
    print("      * dr.smith / Doctor@123 (Doctor)")
    print("      * dr.chen / Doctor@123 (Doctor)")


if __name__ == '__main__':
    app = create_app('development')
    with app.app_context():
        seed_all_data()
