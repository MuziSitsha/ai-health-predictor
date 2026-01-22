with open('app.py', 'r') as f:
    lines = f.readlines()

# Fix line 113-116 (first neural network check)
for i in range(len(lines)):
    if 'joblib.load(\'models/neural_network_model.pkl\')' in lines[i] and 'try:' in lines[i-1]:
        # This is the problematic try block
        # Let's check if the next line is the except block
        if i+2 < len(lines) and 'except:' in lines[i+2]:
            # Fix the loading to be more robust
            new_code = '''        try:
            import os
            if os.path.exists('models/neural_network_model.pkl'):
                nn_model = joblib.load('models/neural_network_model.pkl')
                # Check if model has required methods
                if hasattr(nn_model, 'predict') and hasattr(nn_model, 'predict_proba'):
                    model_options.append('Neural Network')
                else:
                    raise ValueError("Model missing required methods")
            else:
                raise FileNotFoundError("Model file not found")
        except Exception as e:
            print(f"Neural network check failed: {e}")
            st.info("Neural Network not trained yet")'''
            
            # Find the start of this try block
            start = i-1
            while start >= 0 and not lines[start].strip().startswith('try:'):
                start -= 1
            
            # Find the end of this except block
            end = i+3
            while end < len(lines) and not lines[end].strip().startswith('st.info('):
                end += 1
            end += 1
            
            # Replace the block
            lines[start:end] = [new_code + '\n']
            print("Fixed first neural network check")
            break

# Fix lines 193-196 (second neural network check)
for i in range(len(lines)):
    if 'joblib.load(\'models/neural_network_model.pkl\')' in lines[i] and i+3 < len(lines) and 'st.metric("Neural Network"' in lines[i+3]:
        # This is the metrics display
        new_code = '''            try:
                import os
                if os.path.exists('models/neural_network_model.pkl'):
                    nn_model = joblib.load('models/neural_network_model.pkl')
                    if hasattr(nn_model, 'predict') and hasattr(nn_model, 'predict_proba'):
                        st.metric("Neural Network", "Available", "3 Hidden Layers")
                    else:
                        st.metric("Neural Network", "Incomplete", "Retrain needed")
                else:
                    st.metric("Neural Network", "Not Trained", "Train required")
            except:
                st.metric("Neural Network", "Not Trained", "Train required")'''
        
        # Find start and end of this block
        start = i-1
        while start >= 0 and not lines[start].strip().startswith('try:'):
            start -= 1
        
        end = i+4
        while end < len(lines) and not lines[end].strip().startswith('st.metric("Neural Network"'):
            end += 1
        
        lines[start:end] = [new_code + '\n']
        print("Fixed second neural network check")
        break

# Fix lines 241-243 (prediction loading)
for i in range(len(lines)):
    if 'model = joblib.load(\'models/neural_network_model.pkl\')' in lines[i]:
        # This is in the prediction section
        new_code = '''                try:
                    model = joblib.load('models/neural_network_model.pkl')
                    # Load neural network scaler if exists
                    if os.path.exists('models/nn_scaler.pkl'):
                        scaler = joblib.load('models/nn_scaler.pkl')
                except Exception as e:
                    st.error(f"Failed to load neural network: {e}")
                    # Fallback to random forest
                    model = joblib.load('models/random_forest.pkl')
                    scaler = joblib.load('models/scaler_retrained.pkl')'''
        
        lines[i] = new_code + '\n'
        print("Fixed neural network prediction loading")
        break

with open('app.py', 'w') as f:
    f.writelines(lines)
