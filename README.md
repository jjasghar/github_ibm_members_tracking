# taxonomy tracking

## Scope

This is a simple script to start capturing trending data for the [taxonomy repository][repo] for [InstructLab][lab].
The inital release of this will only output daily to a CSV, but there are plans to add more information and
states to this.

Right now we track:
- Total open PRs
- Total open Requested Changes PRs
- Total open Triage Needed PRs
- Total open Triage Need AND Requested Changes PRs
- Total open PreCheck-Generated Ready PRs
- Total Open and Closed Triage Rejected PRs

## Usage

```bash
git clone https://github.com/jjasghar/taxonomy_tracking
cd taxonomy_tracking
# Maybe you just want the CSV? you can read it because it's here. :)
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# copy config.toml-example to config.toml (or use ENV vars)
GH_TOKEN="MY_AWESOME_T0KEN" python create_csv.py
```


## License & Authors

If you would like to see the detailed LICENSE click [here](./LICENSE).

- Author: JJ Asghar <awesome@ibm.com>

```text
Copyright:: 2024- IBM, Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```




[repo]: https://github.com/instructlab/taxonomy
[lab]: https://github.com/instructlab
