# AI-TextGen-for-E-Commerce-Marketing
Text generation for E-Commerce &amp; digital marketing using fine-tuned pre trained of T5-Small with aprox 60 million parameters using my dataset for Digital Marketing Ad and as well as E-commerse .The webpage displayed by using streamlit 

Here i provided other complete detail 

## Tech Stack
- **Python 3.13**: Core language.
- **Transformers (4.38.2)**: T5-small for text generation.
- **SentencePiece (0.2.0)**: Tokenization for T5.
- **PyTorch (2.2.1)**: Model inference.
- **Flask (2.3.3)**: API for inference and MongoDB storage.
- **Streamlit (1.38.0)**: Web UI.
- **MongoDB/PyMongo (4.6.1)**: Database for storing results.
- **Pandas (2.2.2)**: Data preprocessing and display.
- **Colab**: Model training (~10–15 min, 150 examples).

## Setup
1. **Environment**:
   - Create virtual environment: `python3 -m venv h`
   - Install dependencies: `pip install -r requirements.txt`
2. **MongoDB**:
   - Install: `brew install mongodb-community`
   - Run: `mongod --config /usr/local/etc/mongod.conf`
3. **Model**:
   - Fine-tune T5-small in Colab (see training script).
   - Copy `fine_tuned_t5` to project root.
4. **Run**:
   - Backend: `python app.py` (runs on `localhost:5000`).
   - Frontend: `streamlit run frontend.py` (runs on `localhost:8501`).

## Training
- Dataset: `dataset_transformed.csv` (input/text columns, ~150 examples).
- Colab script: Fine-tunes T5-small (1 epoch, batch size 16, FP16, ~10–15 min).
- Output: `fine_tuned_t5` folder.

## API Endpoints
- **POST /generate**:
  - Input: JSON with `product_name`, `category`, `features`, `audience`, `tone`, `output_type`.
  - Output: JSON with `generated_text`.

## Database
- **MongoDB**: `textgen_db.outputs` collection.
- Fields: `product_name`, `category`, `features`, `audience`, `tone`, `output_type`, `generated_text`, `timestamp`.

