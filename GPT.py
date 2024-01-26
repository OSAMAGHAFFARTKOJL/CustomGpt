import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import os
import openai
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai.client.model import Model
from clarifai.client.input import Inputs

os.environ["CLARIFAI_PAT"] = "7a721760203b47449d49d281dd2f3c9c"
openai.api_key ='7a721760203b47449d49d281dd2f3c9c'

PAT = '7a721760203b47449d49d281dd2f3c9c'

# Specify the correct user_id/app_id pairings
USER_ID = 'openai'
APP_ID = 'chat-completion'

# Change these to the appropriate model details
MODEL_ID = 'GPT-4'
MODEL_VERSION_ID = '5d7a50b44aec4a01a9c492c5a5fcf387'

def is_medical_question(question):
    medical_keywords = [
        'medical', 'health', 'doctor', 'hospital', 'treatment',
        'disease', 'condition', 'symptoms', 'diagnosis', 'prescription',
        'medicine', 'vaccine', 'therapy', 'fever', 'surgery', 'nutrition',
        'wellness', 'exercise', 'rehabilitation', 'mental health',
        'cardiology', 'oncology', 'neurology', 'pediatrics', 'geriatrics',
        'infection', 'allergy', 'immunization', 'screening', 'preventive care',
        'chronic', 'acute', 'palliative care', 'genetics', 'radiology',
        'pharmacy', 'laboratory tests', 'emergency', 'ambulance', 'paramedic',
        'physical therapy', 'occupational therapy', 'speech therapy',
        'blood pressure', 'cholesterol', 'diabetes', 'asthma', 'arthritis',
        'cancer', 'heart disease', 'stroke', 'Alzheimer\'s', 'mental illness',
        'flu', 'COVID-19', 'pandemic', 'virus', 'bacteria', 'inflammation',
        'vaccination', 'public health', 'epidemiology', 'healthcare system',
        'pregnancy', 'obstetrics', 'gynecology', 'dermatology', 'orthopedics',
        'urology', 'gastroenterology', 'ophthalmology', 'otolaryngology',
        'endocrinology', 'rheumatology', 'hematology', 'pulmonology',
        'allergies', 'nutritional supplements', 'sleep disorders',
        'sports medicine', 'alternative medicine', 'telemedicine',
        'insurance', 'medication side effects', 'clinical trials',
        'health research', 'medical history', 'family medical history',
        'health screening', 'blood tests', 'vaccination schedule',
        'travel medicine', 'occupational health', 'public health campaigns',
        'counseling', 'therapy options', 'substance abuse', 'addiction treatment',
        'weight management', 'dietary guidelines', 'fitness routines',
        'holistic health', 'alternative therapies', 'yoga', 'meditation',
        'stress management', 'workplace health', 'ergonomics',
        'health education', 'patient advocacy', 'healthcare policy',
        'medical ethics', 'end-of-life care', 'living will', 'organ donation', 'tired','neurolinguistic','sick',
        'ill','well','health','unhealthy','throat','wound','pain','wounds','scratch','accident','swelling','cough',
        'acidity','stiffness','headache','fatigue', 'nausea', 'dizziness', 'breathlessness',
    'chest pain', 'palpitations', 'indigestion', 'constipation', 'diarrhea', 'vomiting',
    'weight changes', 'muscle aches', 'joint pain', 'numbness', 'tingling', 'weakness',
    'vision problems', 'hearing loss', 'skin rash', 'itching', 'bruising', 'hair loss',
    'swollen glands', 'fever', 'chills', 'night sweats', 'cold extremities', 'frequent urination',
    'burning sensation', 'swallowing difficulties', 'hoarseness', 'thirst', 'memory issues',
    'mood swings', 'anxiety', 'depression', 'sleep issues', 'speech delay', 'learning difficulties',
    'ADHD', 'autism', 'down syndrome', 'cerebral palsy', 'seizures', 'headaches', 'sinus issues',
    'ear infections', 'eye conditions', 'gastrointestinal issues', 'urinary tract issues',
    'reproductive health', 'menstrual issues', 'menopause', 'osteoporosis', 'back pain', 'sciatica',
    'carpal tunnel', 'tendonitis', 'bursitis', 'concussions', 'seizures', 'tremors', 'migraines',
    'skin issues', 'cancers', 'anemia', 'hemophilia', 'blood clotting issues', 'bleeding disorders',
    'heart conditions', 'lung conditions', 'diabetes', 'thyroid issues', 'celiac disease',
    'lactose intolerance', 'food allergies', 'nutritional deficiencies', 'vitamin D deficiency',
    'iron deficiency', 'calcium deficiency', 'magnesium deficiency', 'zinc deficiency',
    'sleep hygiene', 'insomnia remedies', 'sleep disorders', 'bedwetting', 'sleepwalking',
    'nightmares', 'teething', 'colic', 'potty training', 'speech delay', 'learning disabilities',
    'ADHD', 'autism', 'intellectual disabilities', 'concussions', 'seizures', 'tremors',
    'muscle weakness', 'numbness', 'balance issues', 'sports injuries', 'athletic training',
    'stress management', 'nutrition counseling', 'weight loss programs', 'fitness programs',
    'exercise routines', 'sports injuries', 'athletic training', 'sports psychology',
    'sports nutrition', 'telehealth', 'telemedicine', 'health insurance', 'medical billing',
    'patient rights', 'healthcare quality', 'patient safety', 'healthcare access',
    'healthcare costs', 'medical ethics', 'research studies', 'clinical trials', 'health research',
    'patient education', 'health promotion', 'disease prevention', 'community health',
    'global health', 'epidemiology', 'infectious diseases', 'vaccination', 'immunization',
    'pandemic preparedness', 'disease surveillance', 'quarantine', 'isolation', 'social distancing',
    'contact tracing', 'healthcare system', 'primary care', 'specialty care', 'hospital care',
    'emergency care', 'urgent care', 'nursing care', 'mental health services', 'dental care',
    'vision care', 'physical therapy services', 'lab tests', 'radiology services',
    'diagnostic imaging', 'surgical services', 'anesthesia', 'intensive care', 'chronic care',
    'long-term care', 'home health care', 'hospice care', 'ambulance services',
    'emergency medical services', 'paramedics', 'preventive care services', 'health screenings',
    'immunization programs', 'cancer screenings', 'family planning services',
    'maternal and child health services', 'childhood immunization', 'prenatal care',
    'postnatal care', 'infant care', 'child health promotion', 'adolescent health services',
    'school health programs', 'occupational health services', 'employee wellness programs',
    'workplace safety', 'environmental health', 'air quality', 'water quality', 'food safety',
    'vector control', 'waste management', 'occupational hygiene', 'chemical exposure',
    'biological hazards', 'radiation protection', 'health education', 'community engagement',
    'patient empowerment', 'health coaching', 'health technology', 'electronic health records',
    'telehealth technology', 'wearable technology', 'health informatics', 'AI in healthcare',
    'robotics in healthcare', 'healthcare analytics', 'data privacy in healthcare',
    'medical cybersecurity', 'healthcare interoperability', 'patient portals',
    'digital therapeutics', 'precision medicine', 'genomic medicine', 'personalized medicine',
    'healthcare decision support', 'point-of-care testing', 'medical imaging technology',
    'telemedicine platforms', 'virtual reality in healthcare', 'augmented reality in healthcare',
    'blockchain in healthcare', '3D printing in healthcare', 'healthcare simulation',
    'healthcare quality improvement', 'patient safety initiatives', 'clinical pathways',
    'evidence-based guidelines', 'patient-centered care', 'shared decision making',
    'patient satisfaction', 'hospital accreditation', 'professional licensure',
    'healthcare workforce development', 'medical education', 'nursing education',
    'allied health education', 'continuing medical education', 'interprofessional education',
    'medical residency programs', 'fellowship programs', 'nursing residency programs',
    'physician assistant training', 'pharmacy education', 'dental education','eye','ear','tooth','hand','brain','hair','foot',
     'teeth','nose','diet','anger','pneumonia','neurolinguistic','depression','stress','mouth','symptoms','precautions','breath',
        'medical','health'
    ]

    return any(keyword in question.lower() for keyword in medical_keywords)

def main():
    
    # Set page title and favicon
    st.set_page_config(page_title="Medical and Health Care BOT", page_icon="💊")

    # Page layout
    st.title("Medical and Health Care BOT")
    st.markdown("### Ask me a Medical and Health related question")
    
    # Get user input
    user_input = st.text_input("**Your Question:**")

    # Check if the question is medical-related
    if is_medical_question(user_input):
        RAW_TEXT = 'Provide relevant medical information and dont extend the answer: ' + str(user_input)
        # Set up Clarifai gRPC channel and stub
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)

        metadata = (('authorization', 'Key ' + PAT),)

        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        # Make a request to Clarifai API
        post_model_outputs_response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,
                inputs=[
                    resources_pb2.Input(
                        data=resources_pb2.Data(
                            text=resources_pb2.Text(
                                raw=RAW_TEXT
                            )
                        )
                    )
                ]
            ),
            metadata=metadata
        )

        # Check the response status
        if post_model_outputs_response.status.code != status_code_pb2.SUCCESS:
            st.error(f"Post model outputs failed, status: {post_model_outputs_response.status.description}")
        else:
            # Retrieve and display the output
            output = post_model_outputs_response.outputs[0].data.text.raw
            st.text_area("**OUTPUT**", value=output, height=150)
            st.warning("Disclaimer: This BOT is not an alternative to a health professional. It is for awareness purposes only. In case of emergency, consult your medical doctor.")
    else:
        st.warning("I only provide you the awareness about medical and health care.")

if __name__ == "__main__":
    main()

