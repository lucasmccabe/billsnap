# billsnap

Congress.gov can be a pain to navigate. `billsnap` is an easier way to get US legislative data.

In progress.

## Table of contents
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)

## Setup
pip later. To get started scraping Congress.gov with `billsnap`:

```python
from billsnap import Scrape
```

## Usage
To scrape bill contents from Congress.gov, initialize a Scrape object with:
* chamber label (House or Senate)
* bill number
* congressional session (default is 115)

```python
bill = Scrape('House', 183, 113)
```

For a given bill, `billsnap` can tell you neat things like:
* title (`bill.get_title()`)
* summary (`bill.get_summary()`)
* policy area(s) (`bill.get_policy_areas()`)
* full text (`bill.get_text()`)
* sponsor (`bill.get_sponsor()`)
* cosponsors (`bill.get_cosponsors()`)

## License
[MIT](https://choosealicense.com/licenses/mit/)
