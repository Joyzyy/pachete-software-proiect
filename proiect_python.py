import pandas as pd

# citirea datelor din fisierul csv
data = pd.read_csv('./data/datasetStudentPerformance.csv')

# definirea si apelarea unei functii pt calcul ratei de succes
def calculate_success_rate(enrolled, approved):
    if enrolled > 0:
        return approved / enrolled
    else:
        return 0
    
data['1st Semester Success Rate'] = data.apply(lambda row: calculate_success_rate(row['Curricular units 1st sem (enrolled)'], row['Curricular units 1st sem (approved)']), axis=1)

# utilizarea structurilor conditionale pentru a determina promovabilitatea
data['1st Semester Pass'] = data['1st Semester Success Rate'].apply(lambda x: 'Passed' if x == 1 else 'Failed')

# accesarea datelor cu loc si iloc
# selectarea studentilor cu varsta peste 25 de ani folosind loc
students_over_25 = data.loc[data['Age at enrollment'] > 25]
print('students over 25: ', students_over_25)

# accesarea primelor 3 randuri si coloanele pentru calificarile parintilor folosind iloc
parent_qualifications = data.iloc[:3, data.columns.get_loc("Mother's qualification"):data.columns.get_loc("Father's qualification")+1]
print('parent qualifications: ', parent_qualifications)

# aplicarea functiilor de grup
# calcularea mediei notelor de admitere pe diferite moduri de aplicare
admission_grade_means = data.groupby('Application mode')['Admission grade'].mean()
print('admission grade means: ', admission_grade_means)

# mapare a statutului marital, genului si grupei de varsta
marital_status_map = {
    1: 'Single', 2: 'Married', 3: 'Widower', 4: 'Divorced', 5: 'Facto Union', 6: 'Legally Separated'
}
data['Marital status'] = data['Marital status'].map(marital_status_map)

gender_map = {0: 'Female', 1: 'Male'}
data['Gender'] = data['Gender'].map(gender_map)

data['Age Group'] = pd.cut(data['Age at enrollment'], bins=[0, 20, 25, 30, 40, 100], 
                           labels=['<20', '20-25', '25-30', '30-40', '>40'])

print(data[['Marital status', 'Gender', 'Age Group']].head())

# vizualizarea datelor folosing histograma, care arata distributia varstei studentilor si statusul marital
import matplotlib.pyplot as plt

age_group_outcome = pd.crosstab(data['Age Group'], data['Target'])
marital_status_outcome = pd.crosstab(data['Marital status'], data['Target'])

fig, axes = plt.subplots(1, 2, figsize=(18, 6))

age_group_outcome.plot(kind='bar', stacked=True, ax=axes[0])
axes[0].set_title('Student Outcome Distribution by Age Group')
axes[0].set_ylabel('Number of Students')
axes[0].set_xlabel('Age Group')

marital_status_outcome.plot(kind='bar', stacked=True, ax=axes[1])
axes[1].set_title('Student Outcome Distribution by Marital Status')
axes[1].set_ylabel('Number of Students')
axes[1].set_xlabel('Marital Status')

plt.tight_layout()
plt.show()

# antrenarea unui model de clasificare pentru a prezice rezultatul studentilor pe baza datelor disponibile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

label_encoders = {}
for column in ['Marital status', 'Gender', 'Application mode', 'Course', 'Nacionality', 'Mother\'s qualification',
               'Father\'s qualification', 'Mother\'s occupation', 'Father\'s occupation', 'Age Group', '1st Semester Pass']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

target_encoder = LabelEncoder()
data['Target'] = target_encoder.fit_transform(data['Target'])
target = data['Target']
features = data.drop(['Target'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

classification_results = classification_report(y_test, y_pred, target_names=target_encoder.classes_, output_dict=True)
print(classification_results)