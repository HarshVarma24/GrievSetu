from tensorflow.keras.models import load_model
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences

bilstm = load_model('/home/harsh/Desktop/UPES/SEM 6/Minor/Saved Models/bilstm_model.keras')
with open('/home/harsh/Desktop/UPES/SEM 6/Minor/Saved Models/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('/home/harsh/Desktop/UPES/SEM 6/Minor/Saved Models/label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

def text_model(text):
    seq = tokenizer.texts_to_sequences([text])
    padded_seq = pad_sequences(seq, maxlen = 100)

    prediction = bilstm.predict(padded_seq)

    prediction_class = prediction.argmax(axis=1)

    category = label_encoder.inverse_transform([prediction_class[0]])
    confidence = prediction[0][prediction_class[0]]

    return category[0], float(confidence)




