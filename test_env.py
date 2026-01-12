print("Testing Python Environment")
print("=" * 40)

try:
    import tensorflow as tf
    print(f"TensorFlow: {tf.__version__} - OK")
except ImportError:
    print("TensorFlow: NOT INSTALLED")

try:
    import pandas as pd
    print(f"Pandas: {pd.__version__} - OK")
except ImportError:
    print("Pandas: NOT INSTALLED")

try:
    import numpy as np
    print(f"NumPy: {np.__version__} - OK")
except ImportError:
    print("NumPy: NOT INSTALLED")

try:
    from sklearn.model_selection import train_test_split
    import sklearn
    print(f"scikit-learn: {sklearn.__version__} - OK")
except ImportError:
    print("scikit-learn: NOT INSTALLED")

print("\n" + "=" * 40)
print("Environment test complete")
