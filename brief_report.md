# AI-Automated Product Listing Generation

## Overview
The team needs to automate the creation of product listings from product images and basic information. Instead of manually writing descriptions, we use ChatGPT's vision capabilities to generate compelling product listings automatically. 

## How the API Integration Works
The pipeline connects a HuggingFace image dataset to OpenAI's vision-capable chat model in five stages:
1. **Dataset loading** — The `fashion-product-images-small` dataset is pulled via load_dataset(), converted to a pandas DataFrame, and a subset of images is cached locally as JPEGs to avoid repeated re-reads of the HuggingFace dataset object.
2. **Image encoding** — Each image is written to an in-memory buffer (BytesIO) and base64-encoded, since the OpenAI Chat Completions API requires images to be sent either as URLs or as base64-encoded data URIs (data:image/jpeg;base64,...).
3. **Prompt construction** — A structured prompt combines the product's dataset metadata (name, category, gender, color, season, usage) with explicit formatting instructions, asking the model to return a JSON object containing a title, description, features, and SEO keywords.
4. **API call** — The prompt and encoded image are sent together in a single user message to gpt-4o-mini, using `response_format={"type": "json_object"}` to force the model to return valid, parsable JSON rather than free-form text.
5. **Batch processing** — The pipeline loops through all products, generates a listing for each, and writes results incrementally to processed_listings.json so progress isn't lost if the run is interrupted.

## Challenges Faced
- **Image object incompatibility:** Image objects can't be saved directly with a string path in some contexts; they need to be routed through a BytesIO buffer before base64 encoding.
- **Ensuring valid JSON output:** Without response_format={"type": "json_object"}, the model can wrap JSON in markdown code fences or add explanatory text, breaking json.loads(). This was mitigated by forcing JSON mode on the API call.
- **Inconsistent metadata fields:** Not every product row has complete or non-null values for fields like season or usage, requiring .get() with fallback defaults (e.g., "N/A") to avoid KeyErrors.
- **Error resilience in batch runs:** A single failed API call (rate limit, malformed response, missing image) could halt the entire batch if not caught. This was addressed with per-product try/except blocks and a continue statement so the loop keeps going.

## Quality of Generated Listings
The output quality is generally coherent, largely due to the use of a multimodal model (gpt-4o-mini) that can "see" the product, and follow the requested JSON structure reliably when JSON mode is enabled.

## Potential Improvements
To transition this script into a production-grade system, the following improvements are recommended:
- **Validation Layer:** Integrate a library like Pydantic to validate the JSON schema of the API response, ensuring that the model always returns the expected fields before the data is committed to storage.
- **Rate Limit Management:** Implement an exponential backoff strategy for API retries to handle rate limits gracefully, ensuring the process remains stable when scaled to thousands of products.
- **Log failures separately:** to make it easier to re-run only the products that errored out, instead of re-processing the full batch.

