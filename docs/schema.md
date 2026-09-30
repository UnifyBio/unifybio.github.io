# Schema

UnifyBio's core data model consists of an extended and annotated Datomic schema.
You should refer to the
[official Datomic docs](https://docs.datomic.com/schema/schema-reference.html) to
understand the available primitive data types, attribute organization and cardinalities,
and how references between entities are handled.

## Unify's Metamodel

Unify expects and enforces the convention, common in most Datomic schemas in practice, that
related attributes are grouped by entity type, termed _kinds_, to disambiguate 
semantic information encoded in the data model from the use of programming language type systems
and their constraints. In this convention, the type information is encoded in the name
of the attribute by its namespace. For instance, in the attribute `:measurement/fpkm`,
the `kind` information is encoded in the namespace portion, `measurement`.

### Reference Attributes

Datomic's data model enforces no constraints and grants no affordances to this convention
out of the box, so the [Unify](https://github.com/vendekagon-labs/unify/)
[metamodel](https://github.com/vendekagon-labs/unify/blob/main/resources/unify-schema.edn#L71-L159)
adds annotations to the database schema which provide additional constraints and affordances
around the representation and use of kinds in the data model. Specifically, it specifies
that certain reference attributes point from one kind to another, that certain
kinds are children of other kinds (and inversely, some kinds are therefore parents to others)
in the dataset tree.

### Identity

The Unify metamodel also specifies different ways that entities may be uniquely identified.
Either an identification is assumed to be globally unique at import time, whether through
a single attribute or composite ID, or the entity's identity must be scoped to its
context in the dataset. Unfortunately, it is all too common that various public and
proprietary datasets only supply weak identifiers, such as integer keys, or string composites of
type and integer, possibly with small string codes, e.g. "trial-bcc-subject-1". These
keys do not provide the strong uniqueness guarantees that keys like UUIDs do, so on import,
Unify will prefix these with context, into a tuple of dataset and the context scope from
the dataset tree, e.g. `["dataset-name" "trial-bcc-subject-1"]` or, with measurements, when
the tree context and synthetic composite IDs are combined.
`["dataset-name" "rna-seq/processing-method-1/sample-id--subject-id--BRCA"]`
