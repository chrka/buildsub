# buildsub

Merges Python files into single file suitable for submission as a Kaggle code
competition kernel.

**NB. This is a bit of a hack, so don't try anything fancy.  It's definitely
possible to do this in a more robust fashion, and if you find such a tool
feel free to drop me a message to tell me about it! (For now, this does the
job well enough for my purposes.)**

If you organize your competition code as a single Python package, `buildsub`
will recursively replace any imports of the form

```python
from competition.subpackages.package import *
```

with the contents of the deepest package (`package` in this example.) 

Only top-level absolute imports, and in particular, only imports of everything 
(`*`) are recognized (this is by design).

This does mean that you have to take extra care so that names do not clash.

## Installation

```shell script
pip install git+https://github.com/chrka/buildsub.git
```

## Usage

```shell script
buildsub --base=BASE_PACKAGE INPUT_FILE OUTPUT_FILE
```
The `INPUT_FILE` and `OUTPUT_FILE` arguments can be replaced with `-` for
standard input/output.

## Example

Say that you have your competition-specific files (models, preprocessing, 
evaluation, submitting procedure, etc.) in a package `competition` in the
same directory as the file implementing your submission, `submission.py`.

For example, something like this:

```
.
├── competition
│   ├── __init__.py
│   ├── models
│   │   ├── __init__.py
│   │   └── advanced
│   │       └── __init__.py
│   ├── preprocess.py
│   └── submit.py
└── submission.py
```

where the files might look something like:

**submission.py**:
```python
from competition.preprocess import *
from competition.models.advanced.secretsauce import *
from competition.submit import *

import pandas as pd

train_df = pd.read_csv("train.csv")
X_train = FeaturePreprocessor.fit_transform(train_df)
y_train = TargetPreprocessor.fit_transform(train_df)

model = SecretSauce()
model.fit(X_train, y_train)

submit(model)
```

**competition/preprocess.py**:
```python
from sklearn.base import BaseEstimator, TransformerMixin

class FeaturePreprocessor(BaseEstimator, TransformerMixin):
    ...

class TargetPreprocessor(BaseEstimator, TransformerMixin):
    ...
```

**competition/models/advanced/secretsauce.py**:
```python
from sklearn.linear_model import LinearRegression
from sklearn.base import BaseEstimator, RegressorMixin

class SecretSauce(BaseEstimator, RegressorMixin):
    ... 
```

**competition/submit.py**:
```python
import pandas as pd
from competition.preprocess import *

def submit(model):
    test_df = pd.read_csv("data/test.csv")
    X_test = FeaturePreprocessor.fit_transform(test_df)
    ...
```

(`buildsub` will take care and try not to include the same file twice.)

Then you can merge the files into a single file, `kernel.py`, which you can
submit as an entry in a Kaggle code competition that does not allow external
data — or the use of utility scripts — by the following command:

```shell script
buildsub --base=competition submission.py kernel.py
```