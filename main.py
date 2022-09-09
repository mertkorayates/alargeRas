import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db


jsonfile = r"alarge-firebase.json"
cred = credentials.Certificate(jsonfile)
firebase_admin.initialize_app(cred,{'databaseURL': 'https://alarge-79fc5-default-rtdb.europe-west1.firebasedatabase.app/'})
docName = ""
firestoreDb = firestore.client()
writeCollection = firestoreDb.collection("Devices")
readstream = firestoreDb.collection("Devices").stream()

result = writeCollection.document(docName).get()

print(result)