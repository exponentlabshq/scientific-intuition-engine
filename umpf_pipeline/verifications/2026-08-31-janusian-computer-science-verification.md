# Verification: Janusian — Computer science — compiler instruction scheduling

**Verifies**: `hypotheses/2026-08-31-janusian-computer-science.md`
**Verified**: 2026-08-31 · **Method**: OpenAI web_search (gpt-4o-mini) + classification, single call (`verify_hypothesis.py`, unattended)

## Verdict: **ADJACENT_ACTIVE**

## Queries
- `instruction scheduling theory in compiler design`
- `research on compiler optimization techniques`
- `instruction scheduling algorithms performance evaluation`
- `compiler instruction scheduling frameworks`
- `instruction scheduling paradox in compiler theory`

## What was found
1. **Instruction Scheduling Across Control Flow**: This 1993 paper introduces SHACOOF, a method that suppresses selected instruction subsequences to enable scheduling beyond basic blocks, aiming to reduce run-time delays. ([research.ibm.com](https://research.ibm.com/publications/instruction-scheduling-across-control-flow?utm_source=openai))

2. **Instruction Scheduling**: A chapter from "Engineering a Compiler" (Third Edition) discusses instruction scheduling as a compile-time activity that reorders operations to improve code quality, emphasizing the importance of this process for modern processors. ([sciencedirect.com](https://www.sciencedirect.com/topics/computer-science/instruction-scheduling?utm_source=openai))

3. **Instruction Scheduling Across Control Flow**: An article from Scientific Programming elaborates on instruction scheduling algorithms used in compilers to reduce run-time delays by reordering program statements, highlighting the significance of scheduling beyond basic blocks. ([researchgate.net](https://www.researchgate.net/publication/220060844_Instruction_Scheduling_Across_Control_Flow?utm_source=openai))

4. **Instruction Scheduling**: An overview from ScienceDirect Topics explains instruction scheduling as a compiler optimization technique aimed at improving instruction-level parallelism by reordering instructions to avoid pipeline stalls and illegal operations. ([sciencedirect.com](https://www.sciencedirect.com/topics/computer-science/instruction-scheduling?utm_source=openai))

## Reasoning
The provided sources detail instruction scheduling techniques in compiler design, including methods like SHACOOF for scheduling beyond basic blocks and general strategies for reordering instructions to enhance performance. These insights support the hypothesis that instruction scheduling can both improve and degrade performance, depending on the context.
