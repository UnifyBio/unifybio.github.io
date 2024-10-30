# Your First Import

This tutorial takes you through the process of creating, then importing your own
minimal UnifyBio dataset. Before attempting to these steps, make sure you have a
local environment capable of completing all the steps in the [quickstart](quickstart.md).

## Organizing Files

The following shows an example directory structure for our simple import, which corresponds
to conventions used in the Pattern Data Commons system:

```
import-dataset
  ├── config.yaml
  ├── mappings.yaml
  ├── data
  │   ├── processed
  │   │   ├── measurements.tsv
  │   │   ├── patients.tsv
  │   │   └── samples.tsv
  │   └── raw
  │       ├── clinical.xlsx
  │       └── molecular.csv
  └── scripts
      ├── clinical.py
      └── molecular.py
```

For smaller and medium sized imports, Pattern uses ordinary git version control (sometimes with LFS enabled)
to manage the state of the import that is the basis for the UnifyBio dataset. This ensures that database
states can be linked back to git repos and commit hashes, ensuring a traceable history which can be used to
source causes of error, or forward propagate changes.

You do not necessarily need to use this exact scheme in your own work, but some similar
discipline about storing and tracking versions of data is recommended.

Importantly, this captures the typical components of an import:

- raw data (stored in `data/raw`)
- scripts for preprocessing the raw data into the form imported into the UnifyBio system.
- the data as produced by the scripts, in `data/processed/`
- the `config.yaml` and `mappings.yaml` files which contain the mappings and import directives which
  specify to the Unify CLI how the data should be imported.

## Creating TSVs

The present version of the Unify CLI can only process TSV files for input. Unify uses tab-separated files
to avoid any of the ambiguities and problems that occur with arbitrarily delimited files, given that
compact and obscure data encodings and fulltext natural language sentences and similar are often 
imported and harmonized into clinical and molecular dataset. The TSV files do not need to
correspond to any particular data model, but there should be a column to column mappings to attributes
in the schema.

## Creating an Import Config

```yaml
:unify/import
  :user "some.user@gmail.com"
dataset:
  name: "yadayda"
  tbd: "more yaml here"
```

### Setting Up Your Editor

The Unify CLI can generate a JSON Schema you can apply to your YAML editing process in
order to provide static checks on the structure and content of the import, as well as
to provide autocomplete, attribute documentation, and more. If you are using the Pattern UnifyBio distribution,
this has been pregenerated for you and can be found under the distribution directry
as the file `candel-import-config-schema.json`. If you need to generate it, you can do so
with this CLI command:

```
bin/unify infer-json-schema --json-schema "YOUR-FILE-NAME-HERE.json"
```

Below are links for how to configure common editors to use JSON Schema when editing YAML files:

- VSCode, via the [Red Hat YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
  steps are documented [here](https://developers.redhat.com/blog/2020/11/25/how-to-configure-yaml-schema-to-make-editing-files-easier).
- JetBrains products such as IntelliJ, Dataspell, and PyCharm, using the processes documented
[here](https://www.jetbrains.com/help/idea/yaml.html#json_schema).

These are summarized in the Unify docs as well (Links TBD).

### Running import steps again with the new dataset.

### Further Steps

To see most of what's possible in a Unify import, refer to the template dataset. In addition,
RCRF makes several dataset imports publicaly available, a list of which can be found 

TBD