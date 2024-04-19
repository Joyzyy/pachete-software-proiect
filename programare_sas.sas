/* 1. Crearea unui set de date SAS din fisiere externe */
proc import datafile='data/dataStudentPerformance.csv'
    out=work.StudentData
    dmbs=csv
    replace;
run;

/* 2. Creare si folosirea de formate definite de utilizator */
proc format;
	value marital_fmt
		1 = "Single"
		2 = "Married"
		3 = "Widower"
		4 = "Divorced"
		5 = "Facto union"
		6 = "Legally separated";
run;

data NStudentData;
	set work.StudentData;
	format "Marital Status"N marital_fmt.;
run;

/* 3. Procesarea iterativa si conditionala a datelor */
data UpdatedData;
	set work.StudentData;
	if "Age at enrollment"N > 25 then adult_student = "YES";
	else adult_student = "NU";
run;

/* 4. Crearea de subseturi de date */
data SubsetData;
	set work.StudentData;
	where "Marital Status"N = 1 and "Age at enrollment"N > 20;
run;

/* 5. Utilizarea de functii SAS */
data FunctiiSasData;
	set work.StudentData;
	if "Admission grade"n > 0 then LogAdmissionGrade = log10("Admission grade"N);
	else LogAdmissionGrade = .;
run;

data FunctiiSasData_2;
	set work.StudentData;
	CombinedData = catx(' - ', "Marital status"N, "Mother's qualification"N, "Mother's occupation"N);
run;

/* 6. Combinarea seturilor de date prin proceduri specifice SAS si SQL */
data TeachersData;
	input Course $ Teacher $;
	datalines;
	171 Ana
	8014 Liviu
	9003 Gabriel
;
run;

proc sql
	create table CombinedData as
	select a.*, b.Teacher
	from work.StudentData as a left join TeacherData as b
	on a.Course = b.Course;
quit;

/* 7. Utilizarea de masive */
data MasiveData;
	set work.StudentData;
    array SemGrades{2} 'Curricular units 1st sem (grade)'n 'Curricular units 2nd sem (grade)'n;
    array Status{2} $7. Status1-Status2;
	do i = 1 to 2;
		if SemGrades{i} >= 15 then Status{i} = "Passed";
		else Status{i} = "Failed";
	end;
run;

/* 9. Folosirea de proceduri statistice */
proc means data=work.StudentData;
	var "Admission grade"n;
	output out=StatsResults mean=MeanGrade std=StdDevGrade;
run;

/* 10. Generarea de grafice */
proc sgplot data=StudentData;
	histogram "Admission grade"n;
	density "Admission grade"n;
run;