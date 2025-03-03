# Step 1: Set Up Your Environment
import pandas as pd
import numpy as np
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

# Initialize Vertex AI
aiplatform.init(project="dk-medical-solutions", location="asia-northeast3")

# Load the text embedding model
embedding_model = TextEmbeddingModel.from_pretrained("textembedding-gecko@latest")

# Step 2: Prepare Your Operation Data
# Sample data structure
operations_data = [
    {"id": "OP001", "operation_name": """	Vaginal mass excision""", 
     "procedure_text": """3cm sized mass at left vaginal wall near anterior cervix@Under intravenous sedation with intubation, the patient was placed on the operation table

 with lithotomy position. Routine sterile preparation and drape was done as usual method 

after douche of vagina.



 After adequate exposure of uterine cervix with surgical speculum, the cervix was grasped 

with tenaculum at 12 o'clock. Schiller test was done with iodine solution and confirmed 

the squamo-columnar junction. Loop electrosurgical excision was done including all the

squamocolumnar junction. Hemostasis was assured and additional hemostasis was done with 

leep coagulator (high frequency surgical unit).



 The patient tolerated the procedure well and was sent to the recovery room with stable 

condition. 



Albothyl soaked cotton ball x 1 and gauze x 1 were packed in the vaginal cavity.

Estimated blood loss: some 



assistant: 

scrub nurse:""", 
     "findings_text": "Gallbladder with multiple stones. No evidence of inflammation..."},
    {"id": "OP002", "operation_name": """	1차봉합술[귀]
""", 
     "procedure_text": """Under local  anesthesia simple skin preparation and drapping is done.
우측 귀 입구 및 postauricualr 부위로 deep lax.  연골 노출되어있는 상황
Bleeding control is done with bipolar tip.
Vicyrl 및 nylon No 5-0로suture 
@
""", 
     "findings_text": "Inflamed appendix with no perforation..."},
    {"id": "OP003", "operation_name": """	ESS & polypectomy
""", 
     "procedure_text": """"1. 전신마취하에서 환자는 position을 취하고 routine skin prep 과 draping 시행 
2. 1:100,000 epinephrine mixed lidocaine inject.
3. Debrider를 이용하여 antrum 주변과 middle meatus주변의 비정상 점막과 polyp  제거 
4. Lt uncinate process 제거 후 bullar ethmoidalis제거 (both ethmoidal sinus filled with pus )
5. Lt. MMA 시행
6. Rt. MMA with polypecotmy 시행
7. septum 및 turbinate 의 열상 및 혈종 등 이상 부위 없음을 확인하고 Merocel packing 시행@
""", 
     "findings_text": "Inflamed appendix with no perforation..."},
    # More operations...
]

# Convert to DataFrame for easier handling
operations_df = pd.DataFrame(operations_data)

# Step 3: Generate Embeddings for All Operations
def generate_embedding(text):
    embeddings = embedding_model.get_embeddings([text])
    return embeddings[0].values  # Get the vector

# Create embeddings for all operation names
operations_df["embedding"] = operations_df["operation_name"].apply(generate_embedding)

# Get the dimension of embeddings
embedding_dimension = len(operations_df["embedding"].iloc[0])
print(f"Embedding dimension: {embedding_dimension}")

# # Create vector search index
index = aiplatform.MatchingEngineIndex.create(
    display_name="dk-medical-operations-index",
    dimensions=embedding_dimension,
    approximate_neighbors_count=20,
    distance_measure_type="COSINE_DISTANCE"
)

# Create an index endpoint
index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name="dk-medical-operations-endpoint"
)

# Deploy index to endpoint
deployed_index = index_endpoint.deploy_index(
    index=index,
    deployed_index_id="dk-medical-operations-deployed"
)

# Step 5: Index Your Operations Data
# Prepare datapoints for indexing
datapoints = []
for _, row in operations_df.iterrows():
    datapoint = {
        "id": row["id"],
        "embedding": row["embedding"]
    }
    datapoints.append(datapoint)

# Upsert datapoints to the index
deployed_index.upsert(
    embeddings=datapoints
)

# Wait for indexing to complete
print("Indexing complete!")

# Step 6: Create a Lookup Table for Operation Details
# Create a dictionary for quick lookup of operation details by ID
operation_lookup = operations_df.set_index("id")[["operation_name", "procedure_text", "findings_text"]].to_dict(orient="index")

# Step 7: Search Function to Find Similar Operations
def find_similar_operations(query_operation, top_k=3):
    """
    Find similar operations to the query operation name.
    
    Args:
        query_operation: The operation name to search for
        top_k: Number of similar operations to return
        
    Returns:
        List of similar operations with their details
    """
    # Generate embedding for the query operation
    query_embedding = generate_embedding(query_operation)
    
    # Search for similar operations
    response = deployed_index.find_neighbors(
        embedding=query_embedding,
        num_neighbors=top_k
    )
    
    # Extract results
    similar_operations = []
    for neighbor in response[0]:
        operation_id = neighbor.id
        similarity_score = 1 - neighbor.distance  # Convert distance to similarity
        
        # Get operation details from lookup table
        operation_details = operation_lookup[operation_id]
        
        # Add to results
        similar_operations.append({
            "operation_id": operation_id,
            "operation_name": operation_details["operation_name"],
            "procedure_text": operation_details["procedure_text"],
            "findings_text": operation_details["findings_text"],
            "similarity_score": similarity_score
        })
    
    return similar_operations

# Step 8: Use the Function to Find Similar Operations
# Example usage
query = "	ESS Polypectomy"  # Non-exact match for "Laparoscopic Cholecystectomy"
similar_ops = find_similar_operations(query, top_k=3)

# Display results
for op in similar_ops:
    print(f"\nOperation: {op['operation_name']}")
    print(f"Similarity: {op['similarity_score']:.2f}")
    print(f"\nPROCEDURE:")
    print(op['procedure_text'][:200] + "...")  # Show first 200 chars
    print(f"\nFINDINGS:")
    print(op['findings_text'][:200] + "...")   # Show first 200 chars
    print("-" * 80)

# Step 9: Template Generation Function
from vertexai.generative_models import GenerativeModel

# Load text generation model
text_model = GenerativeModel("gemini-1.5-pro")

def generate_operation_template(query_operation, similar_operations):
    """
    Generate a template for the requested operation based on similar operations.
    
    Args:
        query_operation: The requested operation name
        similar_operations: List of similar operations found
        
    Returns:
        Generated template with procedures and findings
    """
    # Create prompt with examples
    prompt = f"""
    Generate a detailed medical operation template for: {query_operation}
    
    Based on these similar procedures:
    
    """
    
    # Add examples from similar operations
    for i, op in enumerate(similar_operations, 1):
        prompt += f"""
        EXAMPLE {i}: {op['operation_name']} (Similarity: {op['similarity_score']:.2f})
        
        PROCEDURE:
        {op['procedure_text']}
        
        FINDINGS:
        {op['findings_text']}
        
        """
    
    # Add instructions for template generation
    prompt += """
    Please create a comprehensive template for the requested operation following the structure of these examples.
    Include typical procedures and possible findings, using placeholder text where appropriate for patient-specific details.
    Format the template with clear sections for PROCEDURE and FINDINGS.
    """
    
    # Generate template
    response = text_model.generate_content(prompt)
    return response.text

# Step 10: Complete Example Usage
# Find similar operations
query_operation = "Lap chole with common bile duct exploration"  # Non-exact match
similar_ops = find_similar_operations(query_operation, top_k=3)

# Generate template based on similar operations
template = generate_operation_template(query_operation, similar_ops)

# Print the generated template
print("\n--- GENERATED TEMPLATE ---\n")
print(template)

