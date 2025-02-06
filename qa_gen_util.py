import pandas as pd
import random
def generate_drug_outcome_questions(df, qa_pairs):
    for index, row in df.iterrows():
        patient_id = row['bcr_patient_uuid']
        drug = row['pharmaceutical_therapy_drug_name']
        outcome = row['measure_of_response']
        if pd.notna(drug) :
            question = f"What is the outcome of the patient treated with {drug} ?"
            answer = outcome
            qa_pairs.append((patient_id, question, answer))
    return qa_pairs

def generate_drug_questions(df, qa_pairs):
    for index, row in df.iterrows():
        patient_id = row['bcr_patient_uuid']
        drug = row['pharmaceutical_therapy_drug_name']
        outcome = row['measure_of_response']

        # age = row['age_at_initial_pathologic_diagnosis']
        # gender = row['gender']
        # vital_status = row['vital_status']
        if pd.notna(drug) and outcome != 'Clinical Progressive Disease':
            question = f"What drug was prescribed to the patient?"
            answer = drug
            qa_pairs.append((patient_id, question, answer))
        # if pd.notna(therapy):
        #     question = "What therapy is prescribed to the patient?"
        #     answer = therapy
        #     qa_pairs.append((patient_id, question, answer))
        # if pd.notna(drug) and pd.notna(age) and vital_status == 'Alive':
        #     question = f"What therapy and drug is prescribed to the patient at {age} and {gender} ?"
        #     answer = f'{drug} and {therapy}'
        #     qa_pairs.append((patient_id, question, answer))

    return qa_pairs



def generate_drug_multiple_choice_questions(df, qa_pairs):

    for index, row in df.iterrows():
        patient_id = row['bcr_patient_uuid']
        drug = row['pharmaceutical_therapy_drug_name']
        therapy = row['pharmaceutical_therapy_type']


        # Multiple-choice questions
        if pd.notna(drug):
            # Randomly select distractors from the dataset
            drug_choices = df['pharmaceutical_therapy_drug_name'].dropna().unique().tolist()
            drug_distractors = random.sample([d for d in drug_choices if d != drug], min(2, len(drug_choices)-1))
            choices = [drug] + drug_distractors + ["None"]
            random.shuffle(choices)

            mc_question = f"What drug was prescribed to the patient?"
            mc_answer = drug
            qa_pairs.append((patient_id, mc_question, {"choices": choices, "answer": mc_answer}))
        if pd.notna(drug):
            # Randomly select distractors from the dataset
            drug_choices = df['pharmaceutical_therapy_drug_name'].dropna().unique().tolist()
            drug_distractors = random.sample([d for d in drug_choices if d != drug], min(2, len(drug_choices)-1))
            choices = drug_distractors + ["None"]
            random.shuffle(choices)

            mc_question = f"What drug was prescribed to the patient?"
            mc_answer = "None"
            qa_pairs.append((patient_id, mc_question, {"choices": choices, "answer": mc_answer}))

        if pd.notna(therapy):
            # Randomly select distractors from the dataset
            therapy_choices = df['pharmaceutical_therapy_type'].dropna().unique().tolist()
            therapy_distractors = random.sample([t for t in therapy_choices if t != therapy], min(2, len(therapy_choices)-1))
            choices = [therapy] + therapy_distractors + ["None"]
            random.shuffle(choices)

            mc_question = f"What type of therapy is prescribed to the patient?"
            mc_answer = therapy
            qa_pairs.append((patient_id, mc_question, {"choices": choices, "answer": mc_answer}))

        # Combination multiple-choice
        if pd.notna(drug) and pd.notna(therapy):
            # Create distractors for drug and therapy combinations
            drug_choices = df['pharmaceutical_therapy_drug_name'].dropna().unique().tolist()
            therapy_choices = df['pharmaceutical_therapy_type'].dropna().unique().tolist()

            combo_answer = f"{drug} and {therapy}"
            distractor_combos = [
                                    f"{random.choice(drug_choices)} and {random.choice(therapy_choices)}"
                                    for _ in range(2)
                                ] + ["None"]
            choices = [combo_answer] + distractor_combos
            random.shuffle(choices)

            mc_question = f"Which combination of drug and therapy is prescribed to the patient?"
            qa_pairs.append((patient_id, mc_question, {"choices": choices, "answer": combo_answer}))

    return qa_pairs

def generate_cancer_questions(df, qa_pairs):
    for index, row in df.iterrows():
        patient_id = row['bcr_patient_uuid']
        cancer = row['Cancer']

        if pd.notna(cancer):
            question = f"What type of cancer is present in the WSI?"
            answer = cancer
            qa_pairs.append((patient_id, question, answer))

    return qa_pairs

def save_qa_pairs(qa_pairs_df, output_file='drug_qa_pairs.csv'):
    qa_pairs_df.to_csv(output_file, index=False)
    print(f"Generated {len(qa_pairs_df)} question-answer pairs")