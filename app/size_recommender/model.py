import os
from typing import Literal, Optional

import joblib
import pandas as pd
from pydantic import BaseModel


class InputModel(BaseModel):
    Gender: str
    Garment_Type: Literal["Tops", "Pants"]
    Height: Optional[float] = None
    Chest: Optional[float] = None
    Waist: Optional[float] = None
    Hip: Optional[float] = None

    def preprocess(self):
        # Encode gender
        gender_encoding = {"male": 1, "female": 2}
        gender_encoded = gender_encoding.get(self.Gender, 0)

        # Convert to dictionary and create a DataFrame
        data = {
            "Gender_encoded": gender_encoded,
            "Height": self.Height,
            "Chest": self.Chest,
            "Waist": self.Waist,
            "Hip": self.Hip,
        }

        return pd.DataFrame([data])


class SizeRecommendationModel:
    def __init__(self):
        # Define the path to the model files
        self.base_model_path = "app/models/"
        self.tops_model_filename = "tops_model.pkl"
        self.pants_model_filename = "pants_model.pkl"
        self.jacket_model_filename = "jacket_model.pkl"
        self.tops_label_encoder_filename = "tops_label_encoder.pkl"
        self.pants_label_encoder_filename = "pants_label_encoder.pkl"
        self.jacket_label_encoder_filename = "jacket_label_encoder.pkl"

        # Load the models and label encoders
        self.tops_model = self.load_pickle(self.tops_model_filename)
        self.pants_model = self.load_pickle(self.pants_model_filename)
        self.jacket_model = self.load_pickle(self.jacket_model_filename)
        self.tops_label_encoder = self.load_pickle(self.tops_label_encoder_filename)
        self.pants_label_encoder = self.load_pickle(self.pants_label_encoder_filename)
        self.jacket_label_encoder = self.load_pickle(self.jacket_label_encoder_filename)

    def load_pickle(self, filename):
        with open(os.path.join(self.base_model_path, filename), "rb") as file:
            obj = joblib.load(file)
        return obj

    def preprocess_data(self, input_model: InputModel):
        df = input_model.preprocess()

        if input_model.Garment_Type == "Tops":
            X = df[["Gender_encoded", "Height", "Chest", "Waist", "Hip"]]
        elif input_model.Garment_Type == "Pants":
            X = df[["Gender_encoded", "Waist"]]
        elif input_model.Garment_Type == "Jacket":
            X = df[["Gender_encoded", "Height", "Chest", "Waist", "Hip"]]

        return X

    def predict(self, input_model: InputModel):
        X = self.preprocess_data(input_model)

        if input_model.Garment_Type == "Tops":
            prediction = self.tops_model.predict(X).astype(int)
            encoded = self.tops_label_encoder.inverse_transform(prediction)[0]
        elif input_model.Garment_Type == "Pants":
            prediction = self.pants_model.predict(X).astype(int)
            encoded = self.pants_label_encoder.inverse_transform(prediction)[0]
        elif input_model.Garment_Type == "Jacket":
            prediction = self.pants_model.predict(X).astype(int)
            encoded = self.jacket_label_encoder.inverse_transform(prediction)[0]

        return encoded
