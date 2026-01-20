with open('app.py', 'r') as f:
    content = f.read()

# Add this function near the top after imports
nn_check_function = '''
def check_neural_network():
    """Check if neural network is properly trained and available"""
    try:
        import os
        import joblib
        
        # Check if files exist
        if not os.path.exists('models/neural_network_model.pkl'):
            return False, "Model file not found"
        
        if not os.path.exists('models/nn_scaler.pkl'):
            return False, "Scaler file not found"
        
        # Try to load model
        model = joblib.load('models/neural_network_model.pkl')
        scaler = joblib.load('models/nn_scaler.pkl')
        
        # Check model attributes
        if not hasattr(model, 'predict'):
            return False, "Model missing predict method"
        
        if not hasattr(model, 'predict_proba'):
            return False, "Model missing predict_proba method"
        
        # Test prediction
        import numpy as np
        test_input = np.array([[1, 100, 70, 20, 80, 25.0, 0.5, 30]])
        test_scaled = scaler.transform(test_input)
        
        try:
            prediction = model.predict(test_scaled)
            probability = model.predict_proba(test_scaled)
            return True, "Neural network is ready"
        except:
            return False, "Model failed test prediction"
            
    except Exception as e:
        return False, f"Error: {str(e)}"
'''

# Add after imports
if 'import streamlit as st' in content:
    # Find end of imports
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            continue
        else:
            # Insert before first non-import line
            lines.insert(i, nn_check_function)
            break
    
    content = '\n'.join(lines)

# Update the neural network checks to use this function
# Find the first check (around line 113)
if 'model_options.append(\'Neural Network\')' in content:
    # Replace the try-except block
    new_check = '''        # Check neural network
        nn_ready, nn_message = check_neural_network()
        if nn_ready:
            model_options.append('Neural Network')
        else:
            print(f"Neural network not available: {nn_message}")
            st.info("Neural Network not trained yet")'''
    
    # Find and replace
    import re
    pattern = r"try:\s*joblib\.load.*?st\.info\('Neural Network not trained yet'\)"
    content = re.sub(pattern, new_check, content, flags=re.DOTALL)

with open('app.py', 'w') as f:
    f.write(content)

print("Added neural network verification function")
