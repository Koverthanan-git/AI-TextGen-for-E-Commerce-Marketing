from flask import Flask, request, jsonify
from pymongo import MongoClient
from transformers import T5Tokenizer, T5ForConditionalGeneration
import datetime
import torch
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Connect to MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
    db = client["textgen_db"]
    collection = db["outputs"]
    logger.info("Connected to MongoDB")
except Exception as e:
    logger.error(f"Failed to connect to MongoDB: {str(e)}")
    raise

# Load fine-tuned T5 model and tokenizer
model_path = "./fine_tuned_t5"
try:
    logger.info(f"Loading model from {model_path}")
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    model = T5ForConditionalGeneration.from_pretrained(model_path)
    model = model.to("cpu")  # Use CPU for MacBook
    logger.info("Model and tokenizer loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")
    raise

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        data = request.json
        product_name = data["product_name"]
        category = data["category"]
        features = data["features"]
        audience = data["audience"]
        tone = data["tone"]
        output_type = data["output_type"]

        # Format input prompt
        input_text = f"Generate {output_type} for product: {product_name}, category: {category}, features: {features}, audience: {audience}, tone: {tone}"
        logger.info(f"Processing input: {input_text}")

        # Generate text
        inputs = tokenizer(input_text, return_tensors="pt", max_length=128, truncation=True)
        with torch.no_grad():
            outputs = model.generate(
                inputs["input_ids"].to("cpu"),
                max_length=256,
                num_beams=5,
                early_stopping=True
            )
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info(f"Generated text: {generated_text}")

        # Store in MongoDB
        record = {
            "product_name": product_name,
            "category": category,
            "features": features,
            "audience": audience,
            "tone": tone,
            "output_type": output_type,
            "generated_text": generated_text,
            "timestamp": datetime.datetime.utcnow()
        }
        collection.insert_one(record)
        logger.info("Stored result in MongoDB")

        return jsonify({"generated_text": generated_text})
    except Exception as e:
        logger.error(f"Error in /generate: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    logger.info("Starting Flask server")
    app.run(debug=True, host="0.0.0.0", port=5000)