import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score
import joblib

print("=" * 60)
print("PYTORCH NEURAL NETWORK TRAINING (Simple)")
print("=" * 60)

# Check if PyTorch is available
try:
    import torch
    print("âœ… PyTorch is available")
except ImportError:
    print("âŒ PyTorch not installed. Installing...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
    import torch
    print("âœ… PyTorch installed successfully")

# Load dataset
print("\n1. Loading dataset...")
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
column_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']

df = pd.read_csv(url, names=column_names)
print(f"   Dataset shape: {df.shape}")

# Prepare data
X = df.drop('Outcome', axis=1).values.astype(np.float32)
y = df['Outcome'].values.astype(np.float32)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, 'pytorch_scaler.pkl')
print("   âœ… Scaler saved: pytorch_scaler.pkl")

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train_scaled, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
X_val_tensor = torch.tensor(X_val_scaled, dtype=torch.float32)
y_val_tensor = torch.tensor(y_val, dtype=torch.float32).view(-1, 1)
X_test_tensor = torch.tensor(X_test_scaled, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)

# Define PyTorch model
class SimpleDiabetesNet(nn.Module):
    def __init__(self, input_size):
        super(SimpleDiabetesNet, self).__init__()
        self.layer1 = nn.Linear(input_size, 64)
        self.layer2 = nn.Linear(64, 32)
        self.layer3 = nn.Linear(32, 16)
        self.output = nn.Linear(16, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.dropout(x)
        x = self.relu(self.layer2(x))
        x = self.dropout(x)
        x = self.relu(self.layer3(x))
        x = self.sigmoid(self.output(x))
        return x

# Initialize model
model = SimpleDiabetesNet(X_train.shape[1])
print(f"\n2. Model architecture:")
print(model)

# Loss and optimizer
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
print("\n3. Training model...")
num_epochs = 100
batch_size = 32
n_samples = len(X_train_tensor)

for epoch in range(num_epochs):
    # Shuffle data
    indices = torch.randperm(n_samples)
    X_shuffled = X_train_tensor[indices]
    y_shuffled = y_train_tensor[indices]
    
    # Mini-batch training
    epoch_loss = 0
    for i in range(0, n_samples, batch_size):
        batch_X = X_shuffled[i:i+batch_size]
        batch_y = y_shuffled[i:i+batch_size]
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    
    # Validation
    model.eval()
    with torch.no_grad():
        val_outputs = model(X_val_tensor)
        val_loss = criterion(val_outputs, y_val_tensor)
        val_pred = (val_outputs > 0.5).float()
        val_accuracy = (val_pred == y_val_tensor).float().mean()
    
    model.train()
    
    if (epoch + 1) % 20 == 0:
        print(f"   Epoch {epoch+1}/{num_epochs}, Loss: {epoch_loss:.4f}, Val Loss: {val_loss.item():.4f}, Val Acc: {val_accuracy.item():.4f}")

# Final evaluation
model.eval()
with torch.no_grad():
    test_outputs = model(X_test_tensor)
    test_pred = (test_outputs > 0.5).float()
    test_accuracy = (test_pred == y_test_tensor).float().mean()
    
    # Convert to numpy for sklearn metrics
    test_outputs_np = test_outputs.numpy()
    test_pred_np = test_pred.numpy()
    y_test_np = y_test_tensor.numpy()
    
    test_auc = roc_auc_score(y_test_np, test_outputs_np)

print(f"\n4. Test Results:")
print(f"   í³Š Accuracy: {test_accuracy.item():.4f}")
print(f"   í³Š AUC:      {test_auc:.4f}")

# Save the model
torch.save({
    'model_state_dict': model.state_dict(),
    'input_size': X_train.shape[1],
    'architecture': str(model)
}, 'diabetes_pytorch_model.pth')

print("\n5. Saving model...")
print("   âœ… Model saved: diabetes_pytorch_model.pth")

print("\n" + "=" * 60)
print("í¾‰ PYTORCH TRAINING COMPLETE!")
print("=" * 60)
