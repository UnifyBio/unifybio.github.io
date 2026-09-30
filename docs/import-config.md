# Import Config

An import config file specifies a mapping from ad hoc tables and their contents to
a UnifyBio schema's data model.

## Writing import config files

The template dataset showcases most of the functionality of UnifyBio.
The config file is available in both [yaml](https://github.com/vendekagon-labs/unify/blob/main/test/resources/systems/candel/template-dataset/config.yaml)
and [edn](https://github.com/vendekagon-labs/unify/blob/main/test/resources/systems/candel/template-dataset/config.edn)
forms. If you're new to UnifyBio, we recommend you start with yaml
since Unify is able to generate JSON schema that editors can use to provide autocompletion and static analysis for
import config files.

### Configuring JSON Schema for Editor Assistance with YAML config files

If you are using the Pattern distribution, `pattern-import-config-schema.json` has been pre-generated and provided
for you. If you are not, you can generate a JSON schema for your own Unify schema with:

```
bin/unify infer-json-schema --json-schema YOUR-FILE-NAME.json
```

Most editors support applying json schema to YAML files as you edit; we provide links for the docs and plugins on how to do so below:

* VSCode
    - RedHat [YAML extension](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)
    - Go to settings (Code > Settings > Settings on Mac) and add a path to the JSON schema file under the key "yaml.schemas".
        * More detailed instructions [here](https://dev.to/brpaz/how-to-create-your-own-auto-completion-for-json-and-yaml-files-on-vs-code-with-the-help-of-json-schema-k1i).
* JetBrains products (e.g. IntelliJ, PyCharm, etc.)
    - [Method 1](https://www.jetbrains.com/help/idea/yaml.html#select-schema-for-file): provide configuration via the JSON Schema Mappings setting.
    - [Method 2](https://www.jetbrains.com/help/idea/yaml.html#use-schema-keyword): annotate the YAML file with a path to the spec in a comment.


## General config file structure

The nesting of the different objects in the config file mirrors
the relationship between the corresponding entities in the database. The top level import section, for instance,
contains information about the data import. Keys that begin with `unify/` (i.e., that are in the unify namespace)
usually specify metadata about the import or directives (special commands or syntax) for performing transforms
that require more than parsing a data literal in a TSV file into an expected type.

Data that is not nested under the `dataset` entity is reference data, and refers to
data from ontologies or standards, or other cases for which identifiers
should always be valid across datasets. The following examples conform to the Pattern
schema.

```yaml title="yaml import config structure"
unify/import:
dataset:
  assays:
    - measurement-sets:
      - measurements:
  samples:
  subjects:
  clinical-observations:
  treatment-regimens:
  timepoints:
genomic-coordinate:
variant:
cnv:
```

```clojure title="edn import config structure"
{:unify/import 
 :dataset
 {:assays
  [:measurement-sets
   [:measurements]]}
  :samples []
  :subjects []
  :clinical-observations []
  :treatment-regimens []
  :timepoints []}
 :genomic-coordinate []
 :variant []
 :cnv []}
```

## Data specifications

Now let's look into specific sections to understand how data mapping with unify works. 

### Literal data

The data below is literal data; it will be input into the database as is.
The name of the dataset will be `template-dataset`, the doi will be `10.1126/science.aaa1348` etc.
This is as opposed to data that is input from a file -- see below for many examples of this.

```yaml title="yaml dataset literal"
dataset:
  name: template-dataset
  description: "Description of your dataset, ie title of paper, title of clinical trial, or description of conglomerate dataset"
  doi: "10.1126/science.aaa1348"
  url: "http://science.sciencemag.org/content/suppl/2015/03/11/science.aaa1348.DC1"
```

```clojure title="edn dataset literal"
:dataset {:name         "template-dataset"
          :description  "Description of your dataset, ie title of paper, title of clinical trial, or description of conglomerate dataset"
          :doi          "10.1126/science.aaa1348"
          :url          "http://science.sciencemag.org/content/suppl/2015/03/11/science.aaa1348.DC1"}
```

### Loading data from input TSV files
To load data from input files (which must be in TSV format), we use the `:unify/input-tsv-file` key (see below).
Note that the input file path is relative to the `config.edn` or `config.yaml` file location.

#### Static attributes (standard table / wide format)

This is the simplest type of data. Each column corresponds to an attribute and each row to an entity.
The mappings between columns in the original data and attributes in Unify are specified as follows:

```yaml title="yaml measurements file directive"
measurements:
  - unify/input-tsv-file: 'processed/nanostring.txt'
    gene-product: variable
    sample: sample
    nanostring-count: value
```

```clojure title="edn measurements file directive"
:measurements [{:unify/input-tsv-file  "processed/nanostring.txt"
                :gene-product     "variable"
                :sample           "sample"
                :nanostring-count "value"}]
```

This is what the corresponding `nanostring.txt` file looks like:

|sample|	variable|	value|
|------|----------|------|
|TCGA-06-5416-01A-01D-1486-08|	ACO2|	9.795|
|TCGA-06-5416-01A-01D-1486-08|	ACTB|	15.25|
|TCGA-06-5416-01A-01D-1486-08|	ACVR1C|	5.603|
|TCGA-06-5416-01A-01D-1486-08|	ACVR2A|	7.545|
|TCGA-06-5416-01A-01D-1486-08|	ACVR2B|	6.173|
|TCGA-06-5416-01A-01D-1486-08|	ADA	| 6.532|

#### Dynamic attributes (molten format)

When data is in a melted or similar sparse format there will be a column in the output file
that specifies the attribute type of each row, and another column with the actual value
(i.e. similar to the output of the `melt` function in the `reshape` R package or 
melt in the Python pandas package). Molten data can be imported using the special
form below. Note that as is often the case, this contains a mixture of wide and molten data.

The molten import syntax is demonstrated in the highlighted code block examples below.
The column specified by `unify/variable` contains the attribute name, and the column
specified by `unify/value` indicates which column contains the value that corresponds
to said attribute. The mapping in `unify/variables` specifies how each variable name
that appears in the file maps into the Unify schema. E.g., the variable `t.depth`
corresponds to the measurement attribute `:measurement/t-depth`.

```yaml title="yaml dynamic attributes" hl_lines="5-10"
measurements:
  - unify/input-tsv-file: "processed/variant_measurements.txt"
    sample: "sample.id"
    variant: "var.id"
    unify/variable: "variable"
    unify/value: "value"
    unify/variables:
      t.depth: ":measurement/t-depth"
      n.depth: ":measurement/n-depth"
      vaf: ":measurement/vaf"
```

```clojure title="edn dynamic attributes" hl_lines="4-8"
:measurements [{:unify/input-tsv-file "processed/variant_measurements.txt"
                :sample               "sample.id"
                :variant              "var.id"
                :unify/variable       "variable"
                :unify/value          "value"
                :unify/variables      {"t.depth" :measurement/t-depth
                                       "n.depth" :measurement/n-depth
                                       "vaf"     :measurement/vaf}}]}
```

For reference, this is what the corresponding `variant_measurements.txt` file looks like:


|sample.id|var.id|variable|value|
|---------|-------|---------|--------|
|AL4602_T|	GRCh38:chr1:+:27023633:27023633/G/A|	n.depth|	11|
|AL4602_T|	GRCh38:chr1:+:159898129:159898129/G/A|	n.depth	|32   |
|AL4602_T|	GRCh38:chr1:+:237024557:237024557/G/T|	n.depth	|158|
|MA7027_T|	GRCh38:chr9:+:101797386:101797386/G/A|	t.depth	|144|
|MA7027_T|	GRCh38:chr9:+:130213074:130213074/C/A|	t.depth	|10|
|MA7027_T|	GRCh38:chr9:+:131587312:131587312/T/A|	t.depth	|9|
|FR9547_T|	GRCh38:chr2:+:103090441:103090441/C/A|	vaf	|0.32|
|FR9547_T|	GRCh38:chr2:+:172967053:172967053/G/T|	vaf	|0.23|
|FR9547_T|	GRCh38:chr2:+:207176120:207176120/C/T|	vaf	|0.3|

#### Processing multiple files at once

You can use a series of files as input if you specify them as a glob. The example below would process each file matching the regular expression:

```yaml
measurements:
  - input-tsv-file:
    unify.glob/directory: "processed/"
    unify.glob/pattern: "variant_meas_*.tsv"
```

```clojure
measurements [{:unify/input-tsv-file #glob["processed/" "variant_meas_*.tsv"]}]
         
```

## Dealing with missing values

The `:unify/na` key tells unify what to treat as NA in the input file.
Attributes containing a value specified as `na` will be ignored and not input into the database.
The `:unify/omit-if-na` lists a set of attributes that will cause the entire entity to be omitted
if any of these attributes is NA. This is usually applicable to measurements.

```yaml title="yaml NA example" hl_lines="3-8"
measurements:
  - unify/input-tsv-file: "processed/variant_meas_1.tsv"
    unify/na:
    - ""
    - "NA"
    unify/omit-if-na:
      - ":measurement/t-ref-count"
      - ":measurement/t-alt-count"
    sample: Tumor_Sample_Barcode
    variant: var.id
    unify/variable: variable
    unify/value: value
    unify/variables:
      t_ref_count: ":measurement/t-ref-count"
      t_alt_count: ":measurement/t-alt-count"
```

```clojure title="edn NA example" hl_lines="2-4"
:measurements [{:unify/input-tsv-file "processed/variant_meas_1.tsv"
                :unify/na         ""
                :unify/omit-if-na [:measurement/t-ref-count
                                  :measurement/t-alt-count]
                :sample          "Tumor_Sample_Barcode"
                :variant          "var.id"
                :unify/variable    "variable"
                :unify/value       "value"
                :unify/variables  {"t_ref_count" :measurement/t-ref-count
                                   "t_alt_count" :measurement/t-alt-count}}]
```

Below is what the corresponding data files look like. 

As you can see, the 4th row is missing a value. Because of the usage of `:unify/omit-if-na` the entity generated by this row will be discarded.
If you had not used `:unify/omit-if-na` this would have generated a measurement entity with `:measurement/sample` and `:measurement/variant` attributes, but no value.
This is an invalid entity and would have failed validation.

|Tumor_Sample_Barcode|	var.id|	variable|	value|
|--------------------|--------|---------|--------|
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr1:+:19232629:19232629/C/T|	t_ref_count|	77|
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr1:+:91708723:91708723/G/A|	t_ref_count|	45|
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr2:+:46380261:46380261/C/T|	t_ref_count|	81|
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr1:+:19232629:19232629/C/T|	t_alt_count|	  |
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr1:+:91708723:91708723/G/A|	t_alt_count|	11|
|TCGA-WB-A814-01A-11D-A35I-08|	GRCh38:chr2:+:46380261:46380261/C/T|	t_alt_count|	37|


## Mapping of categorical variables

Most categorical attributes are represented in the database as enums as opposed to strings (e.g. sex is represented by the enums `:sex/female` and `:sex/male`).
The `mappings.edn` or `mappings.yaml` file (specified in the config in `[:unify/import :mappings]`)
dictates how unify will map string values from TSV files in your data to enums. The following snippet is an example from the template dataset:

The `:unify/mappings` section of the file defines a set of mappings.
The left side is the name of the mapping and these names can be re-used in mappings files.
The right side defines the mapping, where the keys are valid data literals or enums in the schema, and the right is
a vector (or array or list) of string values that remap to the key.
The `:unify/variables` top level key in the file specifies which attributes (keys)
each of the provided mappings (values) will apply to.


```yaml title="yaml mappings example"
unify/mappings:
  enum/metastasis:
    true:
      - "Met"
      - "T"
    false:
      - "Primary"
      - "N/A"
      - "F"
      - ""
  enum/sex:
    sex/female:
    - "F"
    sex/male:
    - "M"
unify/variables:
  sample/metastasis: "enum/metastasis"
  subject/sex: "enum/sex"
```

```clojure title="edn mappings example"
{:unify/mappings {:enum/metastasis {true ["Met" "T"]
                                    false ["Primary" "N/A" "F" ""]}
                  :enum/sex {:sex/female ["F"]
                             :sex/male ["M"]}}

 :unify/variables {:sample/metastasis :enum/metastasis
                   :subject/sex :enum/sex}}

```

## Reverse references

In some cases you may have to specify a reference between two entities `A -> B` but the entity type B does not have a unique identifier while A does.
The only part of the schema where this currently happens is when you are specifying therapies for subjects.
Subjects refer to therapies but, while subjects have an id, therapies do not. To handle such cases unify
provides the option to specify references in reverse.

`:unify/rev-variable` specifies which column in the therapies file (`subject.id` in this case) refers back to the subject id in the subject file.
`:unify/rev-attr` specifies which attribute in the parent entity (i.e. the subject) this reference should be attached to (`:subject/therapies` in this case).

```yaml title="yaml reverse ref example" hl_lines="11-13"
subjects:
  - unify/input-tsv-file: "processed/rizvi-subjects.txt"
    id: "subject.id"
    sex: gender
    meddra-disease: disease
    smoker: smoker
    therapies:
    - unify/input-tsv-file: "processed/rizvi-therapies.txt"
      treatment-regimen: "regimen"
      line: "line"
      unify/reverse:
        unify/rev-variable: "subject.id"
        unify/rev-attr: ":subject/therapies"
```

```clojure title="edn reverse ref example" hl_lines="9-10"
:subjects [{:unify/input-tsv-file "processed/rizvi-subjects.txt"
            :id              "subject.id"
            :sex             "gender"   
            :meddra-disease  "disease"
            :smoker          "smoker"
            :therapies       {:unify/input-tsv-file   "processed/rizvi-therapies.txt"
                              :treatment-regimen "regimen"
                              :line              "line"
                              :unify/reverse      {:unify/rev-variable "subject.id"
                                                   :unify/rev-attr     :subject/therapies}}}
```

This is what the subjects file looks like:

|subject.id	|disease|	gender|	smoker|
|-----------|-------|---------|-------|
|AL4602|	Lung adenocarcinoma	|M|	Former|
|AU5884|	Lung adenocarcinoma	|M|	Former|
|BL3403|	Lung adenocarcinoma	|F|	Former|
|CA9903|	Lung adenocarcinoma	|M|	Former|

and this is the therapies file

|subject.id	|line|	regimen|
|-----------|----|---------|
|AL4602|	1|	Pembrolizumab-3wk|
|AU5884|	3|	Pembrolizumab-2wk|
|BL3403|	2|	Pembrolizumab-2wk|
|CA9903|	4|	Pembrolizumab-3wk|

## Data fields with multiple values

If your data has multiple values for an attribute in a single cell of the input table, you can tell unify
to split the content of the cell into individual values. For instance in the following example we have a single
`Genes` column that contains multiple genes separated by `;`. `:cnv/genes` is a cardinality-many attribute,
and therefore the set of genes in each cell will all be associated with a single entity.

This snippet shows how to direct Unify to handle these cases:

```yaml title="yaml multiple value example" hl_lines="6-7"
cnv:
  - unify/input-tsv-file: "processed/cnv_ref_3.tsv"
    genomic-coordinates: "gc.id"
    id: "gc.id"
    genes:
      unify/many-delimiter: ";"
      unify/many-variable: "Genes"
```

```clojure title="edn multiple value example" hl_lines="4-5"
:cnv {:unify/input-tsv-file "processed/cnv_ref_3.tsv"]
      :genomic-coordinates "gc.id"
      :id  "gc.id"
      :genes {:unify/many-delimiter ";"
              :unify/many-variable "Genes"}}
```

This is what the corresponding data table looks like:

|gc.id|	Genes|
|-----|------|
|GRCh38:1:+:74450881:74911796	|CRYZ;ERICH3;ERICH3-AS1;TYW3|
|GRCh38:2:+:120251789:120441226	|INHBB;RALB|
|GRCh38:2:+:125852095:126987310	|GYPC;LINC01941;TEX51|

## Constant values

You can use the `:unify/constants` directive to specify values that you want to be constant across all the entities in a file.
For instance in the following example all the measurement entities generated by pret will have a `:measurement/epitope` attribute with value `LDHA`.

```yaml title="yaml constants example" hl_lines="5-6"
:measurements
  - unify/input-tsv-file: "processed/ldh_meas_and_samples.txt"
    sample: "sample.id"
    measurement/ng-mL: "LDH @ Baseline"
    unify/constants
      - measurement/epitope: "LDHA"
```

```clojure title="edn constants example" hl_lines="4"
:measurements {:unify/input-tsv-file   "processed/ldh_meas_and_samples.txt"
               :sample                "sample.id"
               :measurement/ng-mL     "LDH @ Baseline"
               :unify/constants        {:measurement/epitope "LDHA"}}}]}
```

