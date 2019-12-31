# billsnap

Congress.gov can be a pain to navigate. `billsnap` is an easier way to get US legislative data.

In progress.

## Table of contents
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)

## Setup
pip later. For now:

```python
from billsnap import BillSnap
```

## Usage
Initialize a BillSnap object with:
* chamber label (House or Senate)
* bill number
* congressional session (default is 115)

```python
bs = BillSnap('House', 183, 113)
```

Your BillSnap object can tell you things like:
* bill title (`bs.title`)
* bill summary (`bs.summary`)

## License
[MIT](https://choosealicense.com/licenses/mit/)
