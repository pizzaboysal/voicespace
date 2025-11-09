VoiceSpace — Anonymous Student Reporting

VoiceSpace is a platform that allows students to safely submit sensitive experiences — discrimination, harassment, bullying, microaggressions, unfair grading — without revealing their identity. Teachers and school staff are able to sign in through Firebase and view the messages directed specifically to them. Students never log in, which lowers friction and increases the chance that they actually speak up.

Why this matters

A very large share of discriminatory events in schools are never reported because students fear backlash, embarrassment, social consequences, or being labeled a “problem maker.” They worry teachers won’t believe them, or that a classmate will find out. The result is silence — which allows harm to continue.

Evidence that the problem is real:

57% of students in the United States say they experienced or witnessed harassment in school but did not report it.
Source: https://www.stopbullying.gov/resources/facts

32% of K–12 students of color identified fear of retaliation as the number-one reason they do not report discriminatory treatment.
Source: U.S. Dept of Education Civil Rights Data — https://ocrdata.ed.gov/

63% of students prefer indirect or digital channels when reporting sensitive issues.
Source: DOI — https://doi.org/10.1080/15388220.2022.2035367

VoiceSpace aims to solve that.
It removes identity from the equation so the focus stays on the message — not the messenger.

How VoiceSpace works

Students do not sign in

Students choose a teacher from a list

Students submit what happened anonymously

Their message is stored in Firestore under that teacher’s ID

Teachers sign in with Firebase Auth

When logged in, teachers see only the reports sent to them — not other teachers’ reports

Tech used

Streamlit (UI)

Python

Firebase Firestore

Firebase Authentication (email + password for teachers)

Firebase Admin SDK

### Firebase Key Setup
Create a `firebase_key.json` file in the project root using your Firebase service account credentials.
