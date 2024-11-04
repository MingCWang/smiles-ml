from fastapi import FastAPI, HTTPException
import numpy as np
from transformers import BertTokenizerFast, BertForSequenceClassification
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("Agg")
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw
from fastapi.responses import StreamingResponse
from pymongo import MongoClient, server_api
import io
import os
from fastapi.middleware.cors import CORSMiddleware

# TODO: put this in env file
# port = int(os.getenv("PORT", 8000))
CONNECTION_STRING  = os.getenv("DATABASE_URL", "mongodb://localhost:27017/defaultdb")
FRONT_END_ORIGIN = os.getenv("FRONT_END_ORIGIN", "http://localhost:5173")
try:
    ckpt_path = "./checkpoints/"
    # Paths to tokenizer files
    tokenizer_files = {
        "vocab_file": ckpt_path + "vocab.txt",
        "tokenizer_file": ckpt_path + "tokenizer.json",
        "tokenizer_config_file": ckpt_path + "tokenizer_config.json",
        "special_tokens_map_file": ckpt_path + "special_tokens_map.json",
    }
    tokenizer = BertTokenizerFast(
        vocab_file=tokenizer_files["vocab_file"],
        tokenizer_file=tokenizer_files["tokenizer_file"],
        tokenizer_config=tokenizer_files["tokenizer_config_file"],
        special_tokens_map_file=tokenizer_files["special_tokens_map_file"],
    )
    MODEL = BertForSequenceClassification.from_pretrained(ckpt_path, num_labels=10)
except Exception as e:
    print(f"Error loading tokenizer: {e}")


DB = MongoClient(
    CONNECTION_STRING,
    server_api=server_api.ServerApi(version="1", strict=True, deprecation_errors=True),
)["data"]

SMILES = DB["smiles"]
RESULTS = DB["results"]

app = FastAPI()

# List of allowed origins 
origins = [
    "http://localhost:5173",  # Frontend origin
    FRONT_END_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # Allow specific frontend origin
    allow_origins=["*"],  # allow all origins for testing
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


@app.get("/")
def read_root():
    return {"message": "SMILE PREDICTION API"}


@app.post("/predict")
def predict(smiles: str, save: bool = False):
    """
    Predicts:
        model predictions, molecule structures
    Args:
        smiles (str):
        e.g. 'CCO'

    Returns:
        dict:  {'predictions': predictions, 'mol_img': mol_img, 'to_plot': to_plot}
    """
   
    if Chem.MolFromSmiles(smiles):
        is_valid = True
    else:
        is_valid = False
        return {"smiles": smiles, "predictions": [], "is_valid_smile": is_valid}
        
 

    tokens = tokenizer(smiles, return_tensors="pt")
    predictions = MODEL(**tokens)
    to_plot = predictions.logits.detach().numpy()[0]
    if save:
        # Store the prediction as a list to avoid deepcopy errors
        RESULTS.insert_one(
            {
                "smiles": smiles,
                "predictions": to_plot.tolist(),  # Store as a list, not a tensor
                "is_valid_smile": is_valid
            }
        )
    return {
        "smiles": smiles,
        "predictions": to_plot.tolist(),
        "is_valid_smile": is_valid
    }

@app.get("/results")
def get_results(result_num):
    '''
    generates prediction from randomly selected data from smiles collection 
    and store in results collection
    '''
    data = list(SMILES.aggregate([{"$sample": {"size": int(result_num)}}]))
    results = []
    for d in data:
        smiles_string = d["SMILES"]
        existing_result = RESULTS.find_one({"smiles": smiles_string})
        if existing_result:
            results.append(existing_result)
        else:
            prediction = predict(smiles_string, save=True)
            results.append(prediction)  
        
    return {"message": "Ten results generated and stored in the database", "results": results}
    

@app.get("/mol_image")
def generate_mol_img(smiles):
    # Convert the SMILES string to a molecule object
    mol = Chem.MolFromSmiles(smiles)
    # Check if the molecule was parsed correctly
    if mol is None:
        raise HTTPException(status_code=400, detail="Invalid SMILES string")
    else:
        img = Draw.MolToImage(mol, size=(300, 300))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return StreamingResponse(buffer, media_type="image/png")


@app.get("/plot")
def generate_plot(to_plot):
    to_plot = list(map(float, to_plot.split(",")))
    max_index = np.argmax(to_plot)
    max_value = to_plot[max_index]
    indices = np.arange(len(to_plot))
    plt.plot(indices, to_plot, color="blue", label="Data")
    plt.plot(max_index, max_value, "ro", label="Maximum Value")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Logits")
    plt.legend()
    # Save the plot to an in-memory buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
