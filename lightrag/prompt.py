from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

# All delimiters must be formatted as "<|UPPER_CASE_STRING|>"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|#|>"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["entity_extraction_system_prompt"] = """---Role---
You are a Knowledge Graph Specialist responsible for extracting entities and relationships from the input text.

---Instructions---
1.  **Entity Extraction & Output:**
    *   **Identification:** Identify clearly defined and meaningful entities in the input text.
    *   **Entity Details:** For each identified entity, extract the following information:
        *   `entity_name`: The name of the entity. If the entity name is case-insensitive, capitalize the first letter of each significant word (title case). Ensure **consistent naming** across the entire extraction process.
        *   `entity_type`: Categorize the entity using one of the following types: `{entity_types}`. If none of the provided entity types apply, do not add new entity type and classify it as `Other`.
        *   `entity_description`: Provide a concise yet comprehensive description of the entity's attributes and activities, based *solely* on the information present in the input text.
    *   **Output Format - Entities:** Output a total of 4 fields for each entity, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `entity`.
        *   Format: `entity{tuple_delimiter}entity_name{tuple_delimiter}entity_type{tuple_delimiter}entity_description`

2.  **Relationship Extraction & Output:**
    *   **Identification:** Identify direct, clearly stated, and meaningful relationships between previously extracted entities.
    *   **N-ary Relationship Decomposition:** If a single statement describes a relationship involving more than two entities (an N-ary relationship), decompose it into multiple binary (two-entity) relationship pairs for separate description.
        *   **Example:** For "Alice, Bob, and Carol collaborated on Project X," extract binary relationships such as "Alice collaborated with Project X," "Bob collaborated with Project X," and "Carol collaborated with Project X," or "Alice collaborated with Bob," based on the most reasonable binary interpretations.
    *   **Relationship Details:** For each binary relationship, extract the following fields:
        *   `source_entity`: The name of the source entity. Ensure **consistent naming** with entity extraction. Capitalize the first letter of each significant word (title case) if the name is case-insensitive.
        *   `target_entity`: The name of the target entity. Ensure **consistent naming** with entity extraction. Capitalize the first letter of each significant word (title case) if the name is case-insensitive.
        *   `relationship_keywords`: One or more high-level keywords summarizing the overarching nature, concepts, or themes of the relationship. Multiple keywords within this field must be separated by a comma `,`. **DO NOT use `{tuple_delimiter}` for separating multiple keywords within this field.**
        *   `relationship_description`: A concise explanation of the nature of the relationship between the source and target entities, providing a clear rationale for their connection.
    *   **Output Format - Relationships:** Output a total of 5 fields for each relationship, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `relation`.
        *   Format: `relation{tuple_delimiter}source_entity{tuple_delimiter}target_entity{tuple_delimiter}relationship_keywords{tuple_delimiter}relationship_description`

3.  **Delimiter Usage Protocol:**
    *   The `{tuple_delimiter}` is a complete, atomic marker and **must not be filled with content**. It serves strictly as a field separator.
    *   **Incorrect Example:** `entity{tuple_delimiter}Tokyo<|location|>Tokyo is the capital of Japan.`
    *   **Correct Example:** `entity{tuple_delimiter}Tokyo{tuple_delimiter}location{tuple_delimiter}Tokyo is the capital of Japan.`

4.  **Relationship Direction & Duplication:**
    *   Treat all relationships as **undirected** unless explicitly stated otherwise. Swapping the source and target entities for an undirected relationship does not constitute a new relationship.
    *   Avoid outputting duplicate relationships.

5.  **Output Order & Prioritization:**
    *   Output all extracted entities first, followed by all extracted relationships.
    *   Within the list of relationships, prioritize and output those relationships that are **most significant** to the core meaning of the input text first.

6.  **Context & Objectivity:**
    *   Ensure all entity names and descriptions are written in the **third person**.
    *   Explicitly name the subject or object; **avoid using pronouns** such as `this article`, `this paper`, `our company`, `I`, `you`, and `he/she`.

7.  **Language & Proper Nouns:**
    *   The entire output (entity names, keywords, and descriptions) must be written in `{language}`.
    *   Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

8.  **Completion Signal:** Output the literal string `{completion_delimiter}` only after all entities and relationships, following all criteria, have been completely extracted and outputted.

---Examples---
{examples}

---Real Data to be Processed---
<Input>
Entity_types: [{entity_types}]
Text:
```
{input_text}
```
"""

PROMPTS["entity_extraction_user_prompt"] = """---Task---
Extract entities and relationships from the input text to be processed.

---Instructions---
1.  **Strict Adherence to Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system prompt.
2.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
3.  **Completion Signal:** Output `{completion_delimiter}` as the final line after all relevant entities and relationships have been extracted and presented.
4.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""

PROMPTS["entity_continue_extraction_user_prompt"] = """---Task---
Based on the last extraction task, identify and extract any **missed or incorrectly formatted** entities and relationships from the input text.

---Instructions---
1.  **Strict Adherence to System Format:** Strictly adhere to all format requirements for entity and relationship lists, including output order, field delimiters, and proper noun handling, as specified in the system instructions.
2.  **Focus on Corrections/Additions:**
    *   **Do NOT** re-output entities and relationships that were **correctly and fully** extracted in the last task.
    *   If an entity or relationship was **missed** in the last task, extract and output it now according to the system format.
    *   If an entity or relationship was **truncated, had missing fields, or was otherwise incorrectly formatted** in the last task, re-output the *corrected and complete* version in the specified format.
3.  **Output Format - Entities:** Output a total of 4 fields for each entity, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `entity`.
4.  **Output Format - Relationships:** Output a total of 5 fields for each relationship, delimited by `{tuple_delimiter}`, on a single line. The first field *must* be the literal string `relation`.
5.  **Output Content Only:** Output *only* the extracted list of entities and relationships. Do not include any introductory or concluding remarks, explanations, or additional text before or after the list.
6.  **Completion Signal:** Output `{completion_delimiter}` as the final line after all relevant missing or corrected entities and relationships have been extracted and presented.
7.  **Output Language:** Ensure the output language is {language}. Proper nouns (e.g., personal names, place names, organization names) must be kept in their original language and not translated.

<Output>
"""

PROMPTS["entity_extraction_examples"] = [
    """<Input Text>
```
#### 金银花
本品为忍冬科植物忍冬的干燥花蕾或带初开的花。本品气清香,味淡、微苦。以花蕾多、色黄白、气清香者为佳。生用,炒用或制成露剂使用。
【药性】甘,寒。归肺、心、胃经。
【功效】清热解毒,疏散风热。
【应用】
1. 风热感冒,温病发热 本品甘寒质轻,芳香疏透,既能清热解毒,又能疏散风热,适用于外感风热,温热病。
治温病初起,身热头痛,咽痛口渴,常与连翘、薄荷、牛蒡子等同用,如银翘散(《温病条辨》);
治温病气分热盛,壮热烦渴,可与石膏、知母等药同用;
```

<Output>
entity{tuple_delimiter}金银花{tuple_delimiter}中药{tuple_delimiter}金银花为忍冬科植物忍冬的干燥花蕾或带初开的花，性甘寒，归肺、心、胃经，具有清热解毒、疏散风热等功效。
entity{tuple_delimiter}风热感冒{tuple_delimiter}症候{tuple_delimiter}风热感冒属于外感风热引起的疾病症候，可表现为身热头痛、咽痛口渴。
entity{tuple_delimiter}温病发热{tuple_delimiter}症候{tuple_delimiter}温病发热为外感温热病初期症候，表现为身热头痛、咽痛口渴等。
entity{tuple_delimiter}温病气分热盛{tuple_delimiter}症候{tuple_delimiter}温病气分热盛表现为壮热烦渴。
entity{tuple_delimiter}温病初起{tuple_delimiter}症候{tuple_delimiter}温病初起表现为身热头痛、咽痛口渴。
entity{tuple_delimiter}热入营分{tuple_delimiter}症候{tuple_delimiter}热入营分表现为身热夜甚、神烦少寐。
entity{tuple_delimiter}清热解毒{tuple_delimiter}治则治法{tuple_delimiter}清热解毒为金银花的主要治则，用于外感风热及热毒痢疾。
entity{tuple_delimiter}疏散风热{tuple_delimiter}治则治法{tuple_delimiter}疏散风热为金银花的治法，用于治疗风热感冒和温病发热。
entity{tuple_delimiter}连翘{tuple_delimiter}中药{tuple_delimiter}连翘为中药，可与金银花配伍治疗温病初起。
entity{tuple_delimiter}薄荷{tuple_delimiter}中药{tuple_delimiter}薄荷为中药，可与金银花配伍治疗温病初起。
entity{tuple_delimiter}牛蒡子{tuple_delimiter}中药{tuple_delimiter}牛蒡子为中药，可与金银花配伍治疗温病初起。
entity{tuple_delimiter}石膏{tuple_delimiter}中药{tuple_delimiter}石膏为中药，可与金银花配伍治疗温病气分热盛。
entity{tuple_delimiter}知母{tuple_delimiter}中药{tuple_delimiter}知母为中药，可与金银花配伍治疗温病气分热盛。
entity{tuple_delimiter}银翘散{tuple_delimiter}方剂{tuple_delimiter}银翘散为方剂，用于治疗风热感冒。
relation{tuple_delimiter}金银花{tuple_delimiter}风热感冒{tuple_delimiter}治疗, 适应症{tuple_delimiter}金银花用于治疗风热感冒。
relation{tuple_delimiter}金银花{tuple_delimiter}温病发热{tuple_delimiter}治疗, 适应症{tuple_delimiter}金银花用于治疗温病发热。
relation{tuple_delimiter}金银花{tuple_delimiter}清热解毒{tuple_delimiter}功效, 治法{tuple_delimiter}金银花发挥清热解毒功效治疗外感风热及热毒血痢。
relation{tuple_delimiter}金银花{tuple_delimiter}疏散风热{tuple_delimiter}功效, 治法{tuple_delimiter}金银花疏散风热，用于风热感冒及温病发热。
relation{tuple_delimiter}金银花{tuple_delimiter}连翘{tuple_delimiter}配伍{tuple_delimiter}金银花与连翘配伍治疗温病初起。
relation{tuple_delimiter}金银花{tuple_delimiter}薄荷{tuple_delimiter}配伍{tuple_delimiter}金银花与薄荷配伍治疗温病初起。
relation{tuple_delimiter}金银花{tuple_delimiter}牛蒡子{tuple_delimiter}配伍{tuple_delimiter}金银花与牛蒡子配伍治疗温病初起。
relation{tuple_delimiter}金银花{tuple_delimiter}石膏{tuple_delimiter}配伍{tuple_delimiter}金银花与石膏配伍治疗温病气分热盛。
relation{tuple_delimiter}金银花{tuple_delimiter}知母{tuple_delimiter}配伍{tuple_delimiter}金银花与知母配伍治疗温病气分热盛。
relation{tuple_delimiter}金银花{tuple_delimiter}生地黄{tuple_delimiter}配伍{tuple_delimiter}金银花与生地黄配伍治疗热入营分。
relation{tuple_delimiter}金银花{tuple_delimiter}玄参{tuple_delimiter}配伍{tuple_delimiter}金银花与玄参配伍治疗热入营分。
relation{tuple_delimiter}银翘散{tuple_delimiter}金银花{tuple_delimiter}配伍{tuple_delimiter}金银花与银翘散配伍，用于治疗风热感冒。
relation{tuple_delimiter}银翘散{tuple_delimiter}连翘{tuple_delimiter}组成{tuple_delimiter}银翘散包含连翘。
relation{tuple_delimiter}银翘散{tuple_delimiter}薄荷{tuple_delimiter}组成{tuple_delimiter}银翘散包含薄荷。
relation{tuple_delimiter}银翘散{tuple_delimiter}牛蒡子{tuple_delimiter}组成{tuple_delimiter}银翘散包含牛蒡子。
{completion_delimiter}
""",
    """<Input Text>
```
### 急性气管-支气管炎
【临床表现】
(一)症状
本病起病较急，常以鼻塞、咽喉疼痛等上呼吸道感染症状先发，全身症状较轻，可有发热。
初为干咳或咳少量黏液痰，随后痰量逐渐增多，有时痰中带血，咳嗽和咳痰可延续2~3周才消失，通常不超过1个月。
如发生支气管痉挛，可出现程度不等的胸闷、气急。全身症状一般不严重，发热常为低至中等度热，多在3~5天降至正常。

<Output>
entity{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}疾病{tuple_delimiter}急性气管-支气管炎是一种起病急、常伴上呼吸道感染症状的呼吸系统疾病。
entity{tuple_delimiter}鼻塞{tuple_delimiter}症状体征{tuple_delimiter}鼻塞为急性气管-支气管炎常见的上呼吸道症状之一。
entity{tuple_delimiter}咽喉疼痛{tuple_delimiter}症状体征{tuple_delimiter}咽喉疼痛为急性气管-支气管炎常见症状。
entity{tuple_delimiter}干咳{tuple_delimiter}症状体征{tuple_delimiter}干咳是急性气管-支气管炎早期症状，随后可咳痰。
entity{tuple_delimiter}咳痰{tuple_delimiter}症状体征{tuple_delimiter}咳痰为急性气管-支气管炎典型症状，痰量可随病程增加。
entity{tuple_delimiter}发热{tuple_delimiter}症状体征{tuple_delimiter}急性气管-支气管炎可伴低至中等度发热，通常3~5天降至正常。
entity{tuple_delimiter}胸闷{tuple_delimiter}症状体征{tuple_delimiter}如发生支气管痉挛，患者可出现不同程度的胸闷。
entity{tuple_delimiter}气急{tuple_delimiter}症状体征{tuple_delimiter}急性气管-支气管炎严重时可出现气急。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}鼻塞{tuple_delimiter}表现, 早期症状{tuple_delimiter}急性气管-支气管炎可表现为鼻塞。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}咽喉疼痛{tuple_delimiter}表现, 早期症状{tuple_delimiter}急性气管-支气管炎可表现为咽喉疼痛。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}干咳{tuple_delimiter}表现, 早期症状{tuple_delimiter}急性气管-支气管炎可表现为干咳。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}咳痰{tuple_delimiter}表现, 典型症状{tuple_delimiter}急性气管-支气管炎可表现为咳痰。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}发热{tuple_delimiter}表现, 伴随症状{tuple_delimiter}急性气管-支气管炎可伴低至中等度发热。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}胸闷{tuple_delimiter}并发症, 体征{tuple_delimiter}急性气管-支气管炎发生支气管痉挛时可出现胸闷。
relation{tuple_delimiter}急性气管-支气管炎{tuple_delimiter}气急{tuple_delimiter}并发症, 体征{tuple_delimiter}急性气管-支气管炎严重时可出现气急。
{completion_delimiter}

""",
    """<Input Text>
```
腹部视诊时，当观察腹部体表蠕动波、脏器轮廓、搏动及包块时，以侧光为宜。视诊主要内容有腹部外形、呼吸运动、腹壁静脉、胃肠型和蠕动波以及腹壁其他情况。
```

<Output>
entity{tuple_delimiter}腹部视诊{tuple_delimiter}诊疗技术{tuple_delimiter}腹部视诊是一种腹部检查方法，通过观察腹部体表蠕动波、脏器轮廓、搏动及包块来评估腹部情况。
entity{tuple_delimiter}腹部体表蠕动波{tuple_delimiter}症状体征{tuple_delimiter}腹部体表蠕动波是腹部视诊时观察的重要体征。
entity{tuple_delimiter}脏器轮廓{tuple_delimiter}症状体征{tuple_delimiter}脏器轮廓是腹部视诊中评估腹部情况的重要指标。
entity{tuple_delimiter}搏动{tuple_delimiter}症状体征{tuple_delimiter}腹部搏动是腹部视诊中需观察的体征。
entity{tuple_delimiter}包块{tuple_delimiter}症状体征{tuple_delimiter}腹部包块是腹部视诊时需注意的体征。
relation{tuple_delimiter}腹部视诊{tuple_delimiter}腹部体表蠕动波{tuple_delimiter}观察, 体征{tuple_delimiter}腹部视诊可用于观察腹部体表蠕动波。
relation{tuple_delimiter}腹部视诊{tuple_delimiter}脏器轮廓{tuple_delimiter}观察, 体征{tuple_delimiter}腹部视诊可用于评估脏器轮廓。
relation{tuple_delimiter}腹部视诊{tuple_delimiter}搏动{tuple_delimiter}观察, 体征{tuple_delimiter}腹部视诊可用于观察腹部搏动。
relation{tuple_delimiter}腹部视诊{tuple_delimiter}包块{tuple_delimiter}观察, 体征{tuple_delimiter}腹部视诊可用于发现腹部包块。
{completion_delimiter}

""",
]

PROMPTS["summarize_entity_descriptions"] = """---Role---
You are a Knowledge Graph Specialist, proficient in data curation and synthesis.

---Task---
Your task is to synthesize a list of descriptions of a given entity or relation into a single, comprehensive, and cohesive summary.

---Instructions---
1. Input Format: The description list is provided in JSON format. Each JSON object (representing a single description) appears on a new line within the `Description List` section.
2. Output Format: The merged description will be returned as plain text, presented in multiple paragraphs, without any additional formatting or extraneous comments before or after the summary.
3. Comprehensiveness: The summary must integrate all key information from *every* provided description. Do not omit any important facts or details.
4. Context: Ensure the summary is written from an objective, third-person perspective; explicitly mention the name of the entity or relation for full clarity and context.
5. Context & Objectivity:
  - Write the summary from an objective, third-person perspective.
  - Explicitly mention the full name of the entity or relation at the beginning of the summary to ensure immediate clarity and context.
6. Conflict Handling:
  - In cases of conflicting or inconsistent descriptions, first determine if these conflicts arise from multiple, distinct entities or relationships that share the same name.
  - If distinct entities/relations are identified, summarize each one *separately* within the overall output.
  - If conflicts within a single entity/relation (e.g., historical discrepancies) exist, attempt to reconcile them or present both viewpoints with noted uncertainty.
7. Length Constraint:The summary's total length must not exceed {summary_length} tokens, while still maintaining depth and completeness.
8. Language: The entire output must be written in {language}. Proper nouns (e.g., personal names, place names, organization names) may in their original language if proper translation is not available.
  - The entire output must be written in {language}.
  - Proper nouns (e.g., personal names, place names, organization names) should be retained in their original language if a proper, widely accepted translation is not available or would cause ambiguity.

---Input---
{description_type} Name: {description_name}

Description List:

```
{description_list}
```

---Output---
"""

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Knowledge Graph and Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

1. Step-by-Step Instruction:
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize both `Knowledge Graph Data` and `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a references section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

2. Content & Grounding:
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

3. Formatting & Language:
  - The response MUST be in the same language as the user query.
  - The response MUST utilize Markdown formatting for enhanced clarity and structure (e.g., headings, bold text, bullet points).
  - The response should be presented in {response_type}.

4. References Section Format:
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any comment, summary, or explanation after the references.

5. Reference Section Example:
```
### References

- [1] Document Title One
- [2] Document Title Two
- [3] Document Title Three
```

6. Additional Instructions: {user_prompt}


---Context---

{context_data}
"""

PROMPTS["naive_rag_response"] = """---Role---

You are an expert AI assistant specializing in synthesizing information from a provided knowledge base. Your primary function is to answer user queries accurately by ONLY using the information within the provided **Context**.

---Goal---

Generate a comprehensive, well-structured answer to the user query.
The answer must integrate relevant facts from the Document Chunks found in the **Context**.
Consider the conversation history if provided to maintain conversational flow and avoid repeating information.

---Instructions---

1. Step-by-Step Instruction:
  - Carefully determine the user's query intent in the context of the conversation history to fully understand the user's information need.
  - Scrutinize `Document Chunks` in the **Context**. Identify and extract all pieces of information that are directly relevant to answering the user query.
  - Weave the extracted facts into a coherent and logical response. Your own knowledge must ONLY be used to formulate fluent sentences and connect ideas, NOT to introduce any external information.
  - Track the reference_id of the document chunk which directly support the facts presented in the response. Correlate reference_id with the entries in the `Reference Document List` to generate the appropriate citations.
  - Generate a **References** section at the end of the response. Each reference document must directly support the facts presented in the response.
  - Do not generate anything after the reference section.

2. Content & Grounding:
  - Strictly adhere to the provided context from the **Context**; DO NOT invent, assume, or infer any information not explicitly stated.
  - If the answer cannot be found in the **Context**, state that you do not have enough information to answer. Do not attempt to guess.

3. Formatting & Language:
  - The response MUST be in the same language as the user query.
  - The response MUST utilize Markdown formatting for enhanced clarity and structure (e.g., headings, bold text, bullet points).
  - The response should be presented in {response_type}.

4. References Section Format:
  - The References section should be under heading: `### References`
  - Reference list entries should adhere to the format: `* [n] Document Title`. Do not include a caret (`^`) after opening square bracket (`[`).
  - The Document Title in the citation must retain its original language.
  - Output each citation on an individual line
  - Provide maximum of 5 most relevant citations.
  - Do not generate footnotes section or any comment, summary, or explanation after the references.

5. Reference Section Example:
```
### References

- [1] Document Title One
- [2] Document Title Two
- [3] Document Title Three
```

6. Additional Instructions: {user_prompt}


---Context---

{content_data}
"""

PROMPTS["kg_query_context"] = """
Knowledge Graph Data (Entity):

```json
{entities_str}
```

Knowledge Graph Data (Relationship):

```json
{relations_str}
```

Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```
{reference_list_str}
```

"""

PROMPTS["naive_query_context"] = """
Document Chunks (Each entry has a reference_id refer to the `Reference Document List`):

```json
{text_chunks_str}
```

Reference Document List (Each entry starts with a [reference_id] that corresponds to entries in the Document Chunks):

```
{reference_list_str}
```

"""

PROMPTS["keywords_extraction"] = """---Role---
You are an expert keyword extractor, specializing in analyzing user queries for a Retrieval-Augmented Generation (RAG) system. Your purpose is to identify both high-level and low-level keywords in the user's query that will be used for effective document retrieval.

---Goal---
Given a user query, your task is to extract two distinct types of keywords:
1. **high_level_keywords**: for overarching concepts or themes, capturing user's core intent, the subject area, or the type of question being asked.
2. **low_level_keywords**: for specific entities or details, identifying the specific entities, proper nouns, technical jargon, product names, or concrete items.

---Instructions & Constraints---
1. **Output Format**: Your output MUST be a valid JSON object and nothing else. Do not include any explanatory text, markdown code fences (like ```json), or any other text before or after the JSON. It will be parsed directly by a JSON parser.
2. **Source of Truth**: All keywords must be explicitly derived from the user query, with both high-level and low-level keyword categories are required to contain content.
3. **Concise & Meaningful**: Keywords should be concise words or meaningful phrases. Prioritize multi-word phrases when they represent a single concept. For example, from "latest financial report of Apple Inc.", you should extract "latest financial report" and "Apple Inc." rather than "latest", "financial", "report", and "Apple".
4. **Handle Edge Cases**: For queries that are too simple, vague, or nonsensical (e.g., "hello", "ok", "asdfghjkl"), you must return a JSON object with empty lists for both keyword types.

---Examples---
{examples}

---Real Data---
User Query: {query}

---Output---
Output:"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "金银花的药性、功效及临床应用有哪些？"

Output:
{
  "high_level_keywords": ["金银花", "药性", "功效", "临床应用"],
  "low_level_keywords": ["药性", "功效", "临床应用"]
}

""",
    """Example 2:

Query: "急性气管-支气管炎的症状和体征有哪些？"

Output:
{
  "high_level_keywords": ["急性气管-支气管炎", "症状", "体征"],
  "low_level_keywords": ["症状", "体征"]
}

""",
    """Example 3:

Query: "腹部视诊的操作要点及观察指标有哪些？"

Output:
{
  "high_level_keywords": ["腹部视诊", "操作要点", "观察指标"],
  "low_level_keywords": ["操作要点", "观察指标"]
}

""",
]
