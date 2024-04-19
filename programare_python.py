import pandas as pd

data = pd.read_csv('./data/datasetStudentPerformance.csv')

# 1. Utilizarea listelor si a dictionarelor - crearea unui dictionar pentru codurile cursurilor
course_dict = {
    33: 'Biofuel Production Technologies',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy'
}

data['Course Name'] = data['Course'].map(course_dict)

# 2. Eliminarea duplicatelor din setul de valori ale nationalitatilor pentru manipularea seturilor
nationalities = set(data['Nacionality'])
print(data['Nacionality'])

# 3. Definirea si apelarea unei functii pentru calculul ratei de succes
def calculate_success_rate(enrolled, approved):
    if enrolled > 0:
        return approved / enrolled
    else:
        return 0
    
data['1st Semester Success Rate'] = data.apply(lambda row: calculate_success_rate(row['Curricular units 1st sem (enrolled)'], row['Curricular units 1st sem (approved)']), axis=1)

# 4. Utilizarea structurilor conditionale pentru a determina promovabilitatea
data['1st Semester Pass'] = data['1st Semester Success Rate'].apply(lambda x: 'Passed' if x == 1 else 'Failed')

# 5. Accesarea datelor cu loc si iloc
# Selectarea studentilor cu varsta peste 25 de ani folosind loc
students_over_25 = data.loc[data['Age at enrollment'] > 25]

# Accesarea primelor 3 randuri si coloanele pentru calificarile parintilor folosind iloc
parent_qualifications = data.iloc[:3, data.columns.get_loc("Mother's qualification"):data.columns.get_loc("Father's qualification")+1]

# 6. Modificarea datelor in pandas
# Recalcularea calificativului anterior daca este initial zero
data['Previous qualification (grade)'] = data['Previous qualification (grade)'].apply(lambda x: x if x > 0 else data['Previous qualification (grade)'].mean())

# 7: Utilizarea functiilor de grup
# Calcularea mediei notelor de admitere pe diferite moduri de aplicare
admission_grade_means = data.groupby('Application mode')['Admission grade'].mean()

# 8: Tratarea valorilor lipsa
# Inlocuirea valorilor lipsa din coloana 'GDP' cu media acestei coloane
data['GDP'].fillna(data['GDP'].mean(), inplace=True)

# 9: Stergerea de coloane si inregistrari
# Stergerea coloanei 'Debtor' si a inregistrarilor unde varsta la inscriere este necunoscuta
data.drop('Debtor', axis=1, inplace=True)
data.dropna(subset=['Age at enrollment'], inplace=True)

# 10: Prelucrari statistice, gruparea si agregarea datelor in pandas
# Calculul deviatiei standard si mediei pentru notele din primul semestru
semester_stats = data['Curricular units 1st sem (grade)'].agg(['mean', 'std'])

# 11: Prelucrarea seturilor de date cu merge/join
# Unirea setului de date actual cu un alt set fictional
teachers_data = pd.DataFrame({
    'Course': [171, 8014, 9003],
    'Teacher': ['Alina Paduraru', 'Gabriel Zavoianu', 'Liviu Ioan Zecheru']
})
merged_data = data.merge(teachers_data, on='Course', how='left')

# 12. Reprezentare grafica a datelor cu matplotlib
import matplotlib.pyplot as plt
plt.hist(data['Admission grade'], bins=20, alpha=0.75, label='Note de admitere')
plt.title('Distributia notelor de admitere')
plt.xlabel('Nota')
plt.ylabel('Frecventa')
plt.legend()
plt.show()

# 13. Utilizarea pachetului scikit-learn (clusterizare)
from sklearn.cluster import KMeans
X = data[['Admission grade', 'Age at enrollment']].dropna()
kmeans = KMeans(n_clusters=3)
data['Cluster'] = kmeans.fit_predict(X)

# 14. Utilizarea pachetului statmodels (regresie multipla)
import statsmodels.api as sm
X = sm.add_constant(data[['Previous qualification (grade)', 'Age at enrollment']])
y = data['Curricular units 1st sem (grade)']
model = sm.OLS(y, X, missing='drop').fit()
predictions = model.predict(X)

regression_summary = model.summary()
print(regression_summary)