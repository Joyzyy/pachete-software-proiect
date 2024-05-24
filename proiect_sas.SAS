* interpretare organizatie;
proc import datafile='~/datasetStudentPerformance.csv'
	out=StudentData
	dbms=csv
	replace;
run;

data ProcessedData;
    set StudentData;
    array sem1{*} "Curricular units 1st sem (grade)"N--"Curricular units 1st sem (grade)"N;
    array sem2{*} "Curricular units 2nd sem (grade)"N--"Curricular units 2nd sem (grade)"N;
    do i = 1 to dim(sem1);
        if sem1{i} = . then sem1{i} = 0;
    end;
    do i = 1 to dim(sem2);
        if sem2{i} = . then sem2{i} = 0;
    end;
    drop i;
run;

data ExternalFactors;
    input "Marital status"N "Unemployment rate"N "Inflation rate"N GDP;
    datalines;
    1 6.5 1.2 50000
    2 7.0 1.5 55000
    3 5.5 1.1 47000
    4 6.8 1.4 58000
    ;
run;


data SubsetStudentPerformance;
	set StudentData;
	where "Marital Status"N eq 1;
	keep "Martial Status"N "Unemployment rate"N "Inflation rate"N GDP;
run;

proc print data=SubsetStudentPerformance;
run;

* subset de date - altfel - cu set data, etc;

data ExternalFactors;
    input "Marital status"N "Unemployment rate"N "Inflation rate"N GDP;
    datalines;
    1 6.5 1.2 50000
    2 7.0 1.5 55000
    3 5.5 1.1 47000
    4 6.8 1.4 58000
    ;
run;

proc sql;
    create table ComprehensiveData as
    select a.*, b."Unemployment rate"N, b."Inflation rate"N, b.GDP
    from StudentData as a left join ExternalFactors as b
    on a."Marital status"N = b."Marital Status"N
    where a."Age at enrollment"N > 18 and a."Gender"N = 1
    order by a."Admission grade"N desc;
quit;

proc format;
	value MaritalFmt
		1 = 'Single'
		2 = 'Married'
		3 = 'Widower'
		4 = 'Divorced'
		5 = 'Facto Union'
		6 = 'Legally Separated';
run;

proc format;
	value GenderFmt
		0 = 'Male'
		1 = 'Female';
run;

proc format;
	value ScholarshipFmt
		0 = 'Yes'
		1 = 'No';
run;

proc report data=StudentData nowd;
    column "Marital status"N Gender "Scholarship holder"N "Admission grade"N;
    define "Marital status"N / group 'Marital Status' format=MaritalFmt. width=12;
    define Gender / group 'Gender' format=GenderFmt. width=8;
    define "Scholarship holder"N / group 'Scholarship' format=ScholarshipFmt. width=10;
    define "Admission grade"N / mean 'Mean Admission Grade' format=8.2;
    title "Summary Report of Student Admission Grades";
run;


/* folosind sgplot */
proc sgplot data=StudentData;
    scatter x="Age at enrollment"N y="Admission grade"N / group=Gender markerattrs=(symbol=circlefilled);
    xaxis label='Age at Enrollment';
    yaxis label='Admission Grade';
    title 'Scatter Plot of Admission Grades by Age and Gender';
run;

/* regresie folosind reg - interpretare rezultatului */
proc reg data=StudentData;
    model "Admission grade"N = "Age at enrollment"N "Previous qualification (grade)"N;
    output out=RegResults p=predicted_values r=residuals;
run;
