with open('app.py', 'r') as f:
    content = f.read()

# Find where model_options is defined
if "model_options = ['Random Forest']" in content:
    # Add neural network check after this line
    nn_check = '''    # Check which models are available
    model_options = ['Random Forest']
    
    # Check neural network
    nn_ready, nn_message = check_neural_network()
    if nn_ready:
        model_options.append('Neural Network')'''
    
    content = content.replace(
        "    # Model Selection\n    st.subheader(\"Model Selection\")\n    model_options = ['Random Forest']",
        '''    # Model Selection
    st.subheader("Model Selection")
    
    # Check which models are available
    model_options = ['Random Forest']
    
    # Check neural network
    nn_ready, nn_message = check_neural_network()
    if nn_ready:
        model_options.append('Neural Network')'''
    )
    
    print("✓ Added proper neural network check")

with open('app.py', 'w') as f:
    f.write(content)
