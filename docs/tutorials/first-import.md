# Your First Import

This tutorial takes you through the process of creating, then importing your own
minimal UnifyBio dataset. Before attempting these steps, make sure you have a
local environment capable of completing all the steps in the [quickstart](quickstart.md).

The import we walk through is the synthetic `example-import` included in the
Pattern UnifyBio distribution. It should be fairly simple to adapt to other
small datasets; we encourage you to work through the tutorial a second time
with some of your own data, once you've completed it for the example case.

At any point, feel free to refer to the [import config](../import-config.md) docs
for a more thorough explanation of any special unify forms or syntax you encounter
during the tutorial.

## Organizing Files

The following shows an example directory structure for our simple import, which corresponds
to conventions used in the Pattern Data Commons system:

```
example-import
├── config.yaml
├── mappings.yaml
└── data
   └── raw
       ├── clinical.tsv
       ├── measurements.tsv
       ├── patients.tsv
       └── samples.tsv
```

For smaller and medium sized imports, Pattern uses ordinary git version control (sometimes with LFS enabled)
to manage the state of the import that is the basis for the UnifyBio dataset. This ensures that database
states can be linked back to git repos and commit hashes, guaranteeing a traceable history which can be used to
source causes of error, or forward propagate changes if issues are found with the underlying dataset.

You do not necessarily need to use this exact scheme in your own work, but some similar
discipline about storing and tracking versions of data as it is imported into UnifyBio is recommended.

Importantly, this captures the typical components of any import:

- the `config.yaml` and `mappings.yaml` files which contain the mappings and import directives which
  specify to the Unify CLI how the data should be imported.
- raw data (stored in `data/raw`)

You will also typically see:

- `scripts/` for preprocessing the raw data into the form imported into the UnifyBio system.
- the data as transformed by the scripts, in `data/processed/`

## Using TSVs

The present version of the Unify CLI can only process TSV files for input. Unify uses tab-separated files
to avoid any of the ambiguities and problems that occur with arbitrarily delimited files, given that
compact and obscure data encodings and fulltext natural language sentences and similar are often 
imported and harmonized into clinical and molecular datasets. The TSV files do not need to
correspond to any particular data model, but there should be column to column mappings to attributes
in the schema.

## Creating an Import Config

We will create our own import config file for the purposes of this tutorial. We will store it
as a sibling to the current reference config file provided in the distribution and name it
`tutorial-config.yaml`.

```hl_lines="3"
example-import
├── config.yaml
├── tutorial-config.yaml
├── mappings.yaml
```

To get started, provide the top level structure in the YAML file.

```yaml title="tutorial-config.yaml"
unify/import:
  user: "some.user@gmail.com"
dataset:
  name: "my-first-import"
```

### Setting Up Your Editor

The Unify CLI can generate a JSON Schema you can apply to your YAML editing process in
order to provide static checks on the structure and content of the import, as well as
to provide autocomplete, attribute documentation, and more. If you are using the Pattern UnifyBio distribution,
this has been pregenerated for you and can be found under the distribution directory
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

These are summarized in the Unify import config docs as well.

### Providing Entries for each File

We have four files to provide mappings for:

```
patients.tsv
clinical.tsv
samples.tsv
measurements.tsv
```

In the following subsections you will write the import config for each of them.

#### Patient / Subject data

The `patients.tsv` file contains data on our patients. Patients are currently modeled
under the `subject` entity in the Pattern schema. A list of available attributes can
be found [here](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/subject.html).
If you have configured your editor, you should get autocomplete suggestions as you type
which contain the same documented information.

In the file, we have the following columns and table shape:

| id                  | age | sex  | disease             |
|---------------------|-----|------|---------------------|
| subject-group-A-860 | 104 | M    | lung adenocarcinoma |
| subject-group-B-478 | 35  | F    | lung adenocarcinoma |
| subject-group-A-437 | 49  | male | lung adenocarcinoma |

Looking at the patient data in the schema, we can find the appropriate attributes to map to:

```
id => :subject/id
age => :subject/age
sex => :subject/sex
disease => :subject/freetext-disease
```

(Well, the last one may not be obvious, but for the purpose of the tutorial, we'll have you
use freetext instead of mapping the terms into an ontology.)

In its simplest form, the yaml config file is just a literal translation of the
mapping from columns to attributes that we just identified. The required update
has been highlighted for you in the snippet below:

```yaml title="tutorial-config.yaml" hl_lines="5-10"
unify/import:
  user: "some.user@gmail.com"
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
```

There's actually one more thing we have to tend to here, though. `:subject/sex`
values should be mapped to an _enum_, not simply read into the schema. You can
find the enums in the [schema visualizer](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/subject.sex.html).

Mapping enums requires an additional `mappings.yaml` file. For now, we won't worry
about writing it, but link to the existing `mappings.yaml` in the example import,
then inspect the relevant contents.


```yaml title="tutorial-config.yaml" hl_lines="3"
unify/import:
  user: "some.user@gmail.com"
  mappings: mappings.yaml
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
```

Here are the contents of mappings.yaml relevant to the `:subject/sex` attribute:

```yaml title="mappings.yaml content"
unify/mappings:
  enum/subject.sex:
    subject.sex/male:
      - "Male"
      - "M"
      - "m"
      - "male"
    subject.sex/female:
      - "Female"
      - "female"
      - "F"
      - "f"
unify/variables:
  subject/sex: enum/subject.sex
```
This mapping lets Unify know that when it encounters literals like "M" or "Male" they should be
mapped to `:subject.sex/male`, and likewise for "F" or "female" to `:subject.sex/female`.

We are now ready to add more data! Note that if you want to, you can incrementally run prepare
or even transact as you go (assuming you're using local dev databases), just to check for errors
or omitted mappings. For the purpose of the tutorial, we'll continue, but at any point you can
refer back to the commands from the [quickstart](quickstart.md) and run the commands there
on your import in progress.

### Samples data

Next we will map in `samples.tsv`. The columns and data layout are as below:

```
| anatomic-location | id               | patient-id          | timepoint |
|-------------------|------------------|---------------------|-----------|
| lung              | sample-HIKIKDGG2 | subject-group-A-860 | baseline  |
| lung              | sample-JJGDJCEB1 | subject-group-B-478 | baseline  |
| pancreas          | sample-BEFKJJCB7 | subject-group-A-437 | baseline  |
| pancreas          | sample-IBHIBFDG3 | subject-group-B-62  | baseline  |
```

Again, we will consult the [schema dashboard](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/index.html)
for [samples](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/sample.html)
to find the right attributes. The new mappings are provided below:

```yaml title="dataset portion of tutorial-config.yaml" hl_lines="8-13"
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
  samples:
    - unify/input-tsv-file: "data/raw/samples.tsv"
      id: "id"
      subject: "patient-id"
      freetext-anatomic-site: "anatomic-location"
      timepoint: "timepoint"
```

There are two attributes used of a new kind here — timepoint and subject are
both _ref_ attributes. That means they refer to other entities, in this case,
the `subject` and `timepoint` entities. You will notice, if you look through
the tables, that we do not have a `timepoints.tsv` file. However, as you can
quickly verify with grep, R, pandas, or spreadsheet software, we only have
two timepoints, the `baseline` timepoint and the `eos` timepoint.

It is not necessary to add every data point in the dataset as a table, we can
actually just use data literals in the import. 

###  Adding timepoints

Data literal entities lack a `unify/input-tsv-file` directive. We'll add one for timepoints
to our import config. First we'll consult the
[schema docs](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/timepoint.html)
and see which attributes are available that we have the information to provide. It looks
like we need to provide a `timepoint/id` and `timepoint/relative-order`. Since we only
have two timepoints, we'll use `1` and `2` for the relative ordering. We can also click
on the enum information for
[`timepoint/type`](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/timepoint.type.html)
and we see our timepoint names `baseline` and `eos` map neatly on to two types, so we'll provide
those values as well.

```yaml title="dataset portion of tutorial-config.yaml" hl_lines="14-20"
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
  samples:
    - unify/input-tsv-file: "data/raw/samples.tsv"
      id: "id"
      subject: "patient-id"
      freetext-anatomic-site: "anatomic-location"
      timepoint: "timepoint"
  timepoints:
    - id: "baseline"
      relative-order: 1
      type: ":timepoint.type/baseline"
    - id: "eos"
      relative-order: 2
      type: ":timepoint.type/eos"
```

_Note_: we supply the _full_ enum attribute name as a string, e.g. `":timepoint.type/baseline"`. Unlike
with attributes that are property names (i.e. map keys), Unify does not infer namespace information or keyword vs string type for literals
that are property values. But it will attempt to parse any string in value position starting with `":"` as a keyword.

### Mapping in measurements.tsv

Measurement, as captured by the `measurement` entity/namespace, is a very broad
entity type in the Pattern and CANDEL schemas. In general, any molecular assay
or measurement taken in a lab is a measurement. When we refer to the
[measurement schema](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/measurement.html) we can
see a host of different measurement types available.

You should think of measurements as duck typed, in that the kind of measurement
represented is inferred from the attributes. Certain kinds of measurements have
certain targets: proteomic assays target proteins, RNA-seq targets gene expression
by way of transcript fragments, and so on. Most measurements are the result of
an assay performed on a sample. UnifyBio's validator will ensure in the
CLI `bin/validate` step that the combination of attributes on any measurement
makes sense and corresponds to specs and expectations.

In our case, we have a fairly straightforward RNA-seq assay to map in:

| fpkm               | hugo         | sample           |
|--------------------|--------------|------------------|
| 393.43107371469574 | SNORA24B     | sample-HIKIKDGG2 |
| 203.42482862644985 | TCAF1P1      | sample-HIKIKDGG2 |
| 965.3775593576936  | ARHGEF35-AS1 | sample-HIKIKDGG2 |
| 320.0502226355575  | PCDH19       | sample-HIKIKDGG2 |
| 486.5600564050051  | ANKRD49P1    | sample-HIKIKDGG2 |

It might not be obvious to non-biologists, but the `hugo` columns refers to genes
(through the indirection of `gene-product` entities in the Pattern schema), and
we can see `:measurement/fpkm` in the measurement entity in the schema, which
stands for _fragments per kilobase million_, i.e. a normalized metric for
RNA transcript counts.

```yaml title="dataset portion of tutorial-config.yaml" hl_lines="21-30"
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
  samples:
    - unify/input-tsv-file: "data/raw/samples.tsv"
      id: "id"
      subject: "patient-id"
      freetext-anatomic-site: "anatomic-location"
      timepoint: "timepoint"
  timepoints:
    - id: "baseline"
      relative-order: 1
      type: ":timepoint.type/baseline"
    - id: "eos"
      relative-order: 2
      type: ":timepoint.type/eos"
  assays:
    - name: "RNAseq"
      technology: ":assay.technology/RNA-seq"
      measurement-sets:
        - name: "standard fpkm"
          measurements:
            - unify/input-tsv-file: "data/raw/measurements.tsv"
              sample: "sample"
              fpkm: "fpkm"
              gene-product: "hugo"
```

A note on the tree structure: `:dataset/assays` contains all assays in a dataset, and
for some datasets, like the one used in the [Prince Study](https://www.nature.com/articles/s41591-022-01829-9)
these can get quite large and detailed. Assays contain one or more measurement sets, which contain one
or more measurement inputs, to provide groupings that might represent different experimental conditions,
or different ways of processing data computationally, etc. Sometimes these introduce derived entities,
like [cell populations](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/cell-population.html)
grouped through flow cytometry, or
[single cells](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/single-cell.html)
detected and separated through chemical or fluidic aspects of assays, or defined computationally through segmentation.

Our case is pretty straightforward: we're referring to samples from elsewhere in our config,
genes by names provided by the HGNC standard and already present as reference data.

You'll note that as we've gone, also, we've built up the relational complexity of the dataset
without doing a lot of work. For instance, each measurement is:

- a value or values representing an instrument reading in the real world, to which some
  kind of data processing was applied.
- of a particular target, a known biological entity, which is a transcript (gene product) derived from a gene
- taken by a particular assay of a particular known technology type
- with certain processing and/or experimental conditions shared by other measurements
  grouped into the same measurement set.
- of a sample that was derived
    - from a patient (subject)
    - at a particular timepoint

Not every data model that uses UnifyBio's tool ecosystem or integrations, or every
use of the Unify CLI for that matter, has to apply this sort of relational complexity.
But this kind of relational complexity exists in many domains, and with minimal declarative effort,
we are able to infer it from a combination of the structure of our data, and the details
of our Unify schema and metamodel.

### clinical.tsv

The last data we have to import is our clinical data. A view of it is below:

| os  | patient             | timepoint |
|-----|---------------------|-----------|
| 98  | subject-group-A-860 | eos       |
| 39  | subject-group-B-478 | eos       |
| 153 | subject-group-A-437 | eos       |

We have the overall survival data (as os), an ID for our patients, and a timepoint.
In this case, all the ref targets (timepoints and patients) have been supplied,
so the mapping is straightforward. Here it is in the context of the
entire (and now complete) import:

```yaml title="complete tutorial-config.yaml" hl_lines="34-40"
unify/import:
  user: "some.user@gmail.com"
  mappings: "mappings.yaml"
dataset:
  name: "my-first-import"
  subjects:
    - unify/input-tsv-file: "data/raw/patients.tsv"
      id: "id"
      sex: "sex"
      age: "age"
  samples:
    - unify/input-tsv-file: "data/raw/samples.tsv"
      id: "id"
      subject: "patient-id"
      freetext-anatomic-site: "anatomic-location"
      timepoint: "timepoint"
  timepoints:
    - id: "baseline"
      relative-order: 1
      type: ":timepoint.type/baseline"
    - id: "eos"
      relative-order: 2
      type: ":timepoint.type/eos"
  assays:
    - name: "RNAseq"
      technology: ":assay.technology/RNA-seq"
      measurement-sets:
        - name: "standard fpkm"
          measurements:
            - unify/input-tsv-file: "data/raw/measurements.tsv"
              sample: "sample"
              fpkm: "fpkm"
              gene-product: "hugo"
  clinical-observation-sets:
    - name: "clinical observations"
      clinical-observations:
        - unify/input-tsv-file: "data/raw/clinical.tsv"
          subject: "patient"
          os: "os"
          timepoint: "timepoint"
```

You can refer to the [clinical observations schema](http://rcrf-data-commons-dashboard--env.eba-t2nvd7ac.us-east-1.elasticbeanstalk.com/schema/1.3.1/clinical-observation.html)
to see what other information can be encoded in clinical observations. At present, they play a similar role to measurements,
being typed implicitly through the presence or lack of certain attributes. Entities can be grouped arbitrarily within
clinical observation sets, representing different sites, contexts within a study or other medical interactions, labs,
and so on.

## Running Unify CLI import steps with your dataset

You can now run all the same steps you ran in the [quickstart](quickstart.md) to transact your
data into a database. Because this is a new, unique dataset, you can transact it either into
an existing dev database you already created, or a new one. You should probably make sure it
passes validations first, though, before you consider making it available to others!

The steps are:

```
bin/unify prepare --import-config PATH/TO/example-import/tutorial-config.yaml --working-directory TEMP-DIR/tutorial-attempt-1
bin/unify request-db --database my-first-db
bin/unify transact --working-directory TEMP-DIR/tutorial-attempt-1 --database my-first-db
bin/unify validate --database my-first-db
```
_Note_: when you run validate without a `--dataset` arg, it defaults to the most recent dataset
in the database.

If your file contains typos or misaligned columns and attributes, you might encounter errors in
a number of places:

- the config file may fail to parse with an error
- while data is being prepared, it might encounter an invalid data value or file vs. mapping situation,
  e.g. a column specified in the config might not exist in the file.
- while transacting data, you might find that some values that are supposed to be unique
  conflict with each other, or some reference data specified doesn't actually exist. E.g.
  you might have a gene name that comes from a different standard, or a different version of the HGNC standard even.
- while validating data, you might find that you created measurements with a nonsensical combination of
  attributes, like a `:measurement/fpkm` attribute with a `:measurement/epitope` protein target. Or you
  might find that you had a measurement that referred to a sample ID that didn't actually exist
  in your sample table.

Given these situations, it's completely normal and expected that you will hit hiccups and need to debug
them. The Unify CLI tries to provide error messages that are as specific and direct as possible to
make this as painless as possible. It can't magically provide the missing information from
the bogus xlsx file the vendor put in your Box folder, but it will do its best to identify
any issues those sorts of things introduce.

## Further Steps

To see most of what's possible in a Unify import, refer to the
[template dataset](https://github.com/vendekagon-labs/unify/blob/main/test/resources/systems/candel/template-dataset/config.yaml)
and the [import config docs](../import-config.md). In addition,
RCRF intends to make several curated imports and datasets public. To learn more,
[get in touch!](https://rarecancer.org/initiatives).

